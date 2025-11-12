from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file, send_from_directory, current_app
from app import db
from app.models import WorkItem, StatusHistory, Comment
from app.docx_generator import generate_docx, generate_multiple_docx
from app.utils import format_datetime, allowed_file, generate_unique_filename, resize_image
from datetime import datetime
import os
import zipfile
from io import BytesIO


bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to require admin authentication."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/uploads/<filename>')
@admin_required
def serve_upload(filename):
    """Serve uploaded photos."""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@bp.route('/download-photo/<int:item_id>/<int:photo_id>')
@admin_required
def download_photo(item_id, photo_id):
    """Download a single photo."""
    from app.models import Photo
    photo = Photo.query.get_or_404(photo_id)
    
    # Verify photo belongs to the work item
    if photo.work_item_id != item_id:
        flash('Invalid photo', 'danger')
        return redirect(url_for('admin.view_item', item_id=item_id))
    
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'], 
        photo.filename,
        as_attachment=True,
        download_name=f"photo_{photo_id}_{photo.filename}"
    )


@bp.route('/delete-photo/<int:item_id>/<int:photo_id>')
@admin_required
def delete_photo(item_id, photo_id):
    """Delete a photo from work item."""
    from app.models import Photo
    photo = Photo.query.get_or_404(photo_id)
    
    # Verify photo belongs to the work item
    if photo.work_item_id != item_id:
        flash('Invalid photo', 'danger')
        return redirect(url_for('admin.view_item', item_id=item_id))
    
    try:
        # Delete file from disk
        photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], photo.filename)
        if os.path.exists(photo_path):
            os.remove(photo_path)
        
        # Delete from database
        db.session.delete(photo)
        db.session.commit()
        flash('Photo deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting photo: {str(e)}', 'danger')
    
    return redirect(url_for('admin.view_item', item_id=item_id))


@bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard showing all work items."""
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    sort_by = request.args.get('sort', 'date_desc')

    # Base query
    query = WorkItem.query

    # Apply filters
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)

    # Apply sorting
    if sort_by == 'date_asc':
        query = query.order_by(WorkItem.submitted_at.asc())
    elif sort_by == 'date_desc':
        query = query.order_by(WorkItem.submitted_at.desc())
    elif sort_by == 'item_number':
        query = query.order_by(WorkItem.item_number)
    elif sort_by == 'submitter':
        query = query.order_by(WorkItem.submitter_name)

    work_items = query.all()

    return render_template('admin_dashboard.html', 
                         work_items=work_items,
                         status_filter=status_filter,
                         sort_by=sort_by,
                         format_datetime=format_datetime)


@bp.route('/view/<int:item_id>')
@admin_required
def view_item(item_id):
    """View full details of a work item."""
    work_item = WorkItem.query.get_or_404(item_id)
    return render_template('admin_view_item.html', 
                         work_item=work_item,
                         format_datetime=format_datetime)


@bp.route('/edit/<int:item_id>', methods=['POST'])
@admin_required
def edit_item(item_id):
    """Edit work item details."""
    work_item = WorkItem.query.get_or_404(item_id)
    
    try:
        # Update basic fields
        work_item.item_number = request.form.get('item_number')
        work_item.location = request.form.get('location')
        work_item.description = request.form.get('description')
        work_item.detail = request.form.get('detail')
        work_item.references = request.form.get('references', '')
        
        # Update photo captions
        photo_ids = request.form.getlist('photo_ids[]')
        photo_captions = request.form.getlist('photo_captions[]')
        
        for photo_id, caption in zip(photo_ids, photo_captions):
            from app.models import Photo
            photo = Photo.query.get(int(photo_id))
            if photo and photo.work_item_id == work_item.id:
                photo.caption = caption
        
        # Handle new photo uploads
        new_photo_files = request.files.getlist('new_photos[]')
        new_photo_captions = request.form.getlist('new_photo_captions[]')
        
        for photo_file, caption in zip(new_photo_files, new_photo_captions):
            if photo_file and photo_file.filename and allowed_file(photo_file.filename):
                filename = generate_unique_filename(photo_file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                photo_file.save(filepath)
                _, _, final_path = resize_image(filepath, current_app.config['PHOTO_MAX_WIDTH'])
                final_filename = os.path.basename(final_path)
                
                from app.models import Photo
                new_photo = Photo(
                    filename=final_filename,
                    caption=caption or '',
                    work_item_id=work_item.id
                )
                db.session.add(new_photo)
        
        db.session.commit()
        flash('Work item updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating work item: {str(e)}', 'danger')
    
    return redirect(url_for('admin.view_item', item_id=item_id))


@bp.route('/assign/<int:item_id>', methods=['POST'])
@admin_required
def assign_item(item_id):
    """Assign work item to crew member with revision notes."""
    work_item = WorkItem.query.get_or_404(item_id)
    
    old_status = work_item.status
    new_status = request.form.get('status')
    assigned_to = request.form.get('assigned_to')
    revision_notes = request.form.get('revision_notes')
    admin_name = session.get('crew_name', 'Admin')
    
    try:
        # Update work item
        work_item.status = new_status
        work_item.assigned_to = assigned_to if assigned_to else None
        work_item.revision_notes = revision_notes
        work_item.last_modified_by = admin_name
        work_item.last_modified_at = datetime.utcnow()
        
        # Set needs_revision flag
        work_item.needs_revision = (new_status in ['Needs Revision', 'Awaiting Photos'])
        
        # Record status change in history
        if old_status != new_status:
            history = StatusHistory(
                work_item_id=work_item.id,
                old_status=old_status,
                new_status=new_status,
                changed_by=admin_name,
                notes=revision_notes
            )
            db.session.add(history)
        
        db.session.commit()
        
        # TODO: Send notification if enabled
        # if assigned_to and current_app.config.get('ENABLE_NOTIFICATIONS'):
        #     send_assignment_notification(work_item, assigned_to, revision_notes)
        
        flash(f'Assignment updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating assignment: {str(e)}', 'danger')
    
    return redirect(url_for('admin.view_item', item_id=item_id))


@bp.route('/update-status/<int:item_id>', methods=['POST'])
@admin_required
def update_status(item_id):
    """Update the status of a work item."""
    work_item = WorkItem.query.get_or_404(item_id)
    new_status = request.form.get('status')

    valid_statuses = current_app.config.get('STATUS_OPTIONS', [
        'Submitted', 'In Review by DP', 'In Review by AL', 'Completed Review'
    ])
    
    if new_status in valid_statuses:
        work_item.status = new_status
        db.session.commit()
        flash(f'Status updated to: {new_status}', 'success')
    else:
        flash('Invalid status', 'danger')

    return redirect(url_for('admin.view_item', item_id=item_id))


@bp.route('/download/<int:item_id>')
@admin_required
def download_single(item_id):
    """Download a single work item as .docx."""
    try:
        filepath = generate_docx(item_id)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        flash(f'Error generating document: {str(e)}', 'danger')
        return redirect(url_for('admin.dashboard'))


@bp.route('/download-batch', methods=['POST'])
@admin_required
def download_batch():
    """Download multiple work items as a .zip file."""
    item_ids = request.form.getlist('item_ids[]')

    if not item_ids:
        flash('No items selected', 'warning')
        return redirect(url_for('admin.dashboard'))

    try:
        # Convert to integers
        item_ids = [int(id) for id in item_ids]

        # Generate all documents
        filepaths = generate_multiple_docx(item_ids)

        if not filepaths:
            flash('No documents generated', 'danger')
            return redirect(url_for('admin.dashboard'))

        # Create zip file in memory
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filepath in filepaths:
                if os.path.exists(filepath):
                    zf.write(filepath, os.path.basename(filepath))

        memory_file.seek(0)

        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name='work_items_batch.zip'
        )

    except Exception as e:
        flash(f'Error creating batch download: {str(e)}', 'danger')
        return redirect(url_for('admin.dashboard'))


@bp.route('/delete/<int:item_id>', methods=['POST'])
@admin_required
def delete_item(item_id):
    """Delete a work item (use with caution)."""
    work_item = WorkItem.query.get_or_404(item_id)

    # Delete associated photos from disk
    for photo in work_item.photos:
        photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], photo.filename)
        if os.path.exists(photo_path):
            os.remove(photo_path)

    # Delete from database
    db.session.delete(work_item)
    db.session.commit()

    flash(f'Work item {work_item.item_number} deleted', 'success')
    return redirect(url_for('admin.dashboard'))


@bp.route('/save-admin-notes/<int:item_id>', methods=['POST'])
@admin_required
def save_admin_notes(item_id):
    """Save admin notes for a work item (admin only)."""
    work_item = WorkItem.query.get_or_404(item_id)

    try:
        admin_notes = request.form.get('admin_notes', '')
        work_item.admin_notes = admin_notes
        work_item.admin_notes_updated_at = datetime.utcnow()

        db.session.commit()
        flash('Admin notes saved successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving admin notes: {str(e)}', 'danger')

    return redirect(url_for('admin.view_item', item_id=item_id))
