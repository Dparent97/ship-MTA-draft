from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file, send_from_directory, current_app
from app import db, limiter
from app.models import WorkItem, StatusHistory, Comment
from app.docx_generator import generate_docx, generate_multiple_docx
from app.utils import format_datetime, allowed_file, generate_unique_filename, resize_image
from app.cloudinary_utils import upload_image_to_cloudinary, delete_image_from_cloudinary, is_cloudinary_enabled
from app.notifications import send_assignment_notification
from app.security import (
    sanitize_text_input, validate_text_field, validate_status,
    validate_crew_member, validate_file_upload, escape_sql_like, validate_search_query
)
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
    import requests
    import tempfile

    photo = Photo.query.get_or_404(photo_id)

    # Verify photo belongs to the work item
    if photo.work_item_id != item_id:
        flash('Invalid photo', 'danger')
        return redirect(url_for('admin.view_item', item_id=item_id))

    if photo.cloudinary_url:
        # Download from Cloudinary and serve
        try:
            response = requests.get(photo.cloudinary_url, timeout=10)
            response.raise_for_status()

            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(response.content)
            temp_file.close()

            return send_file(
                temp_file.name,
                as_attachment=True,
                download_name=f"photo_{photo_id}_{photo.filename}"
            )
        except Exception as e:
            flash(f'Error downloading photo: {str(e)}', 'danger')
            return redirect(url_for('admin.view_item', item_id=item_id))
    else:
        # Serve from local storage
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
        # Delete file from Cloudinary or local storage
        if photo.cloudinary_public_id:
            delete_image_from_cloudinary(photo.cloudinary_public_id)
        else:
            # Local storage fallback
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
    """Admin dashboard showing all work items with search validation."""
    # Get filter parameters
    status_filter = sanitize_text_input(request.args.get('status', 'all'), max_length=50)
    sort_by = sanitize_text_input(request.args.get('sort', 'date_desc'), max_length=50)
    search_query = request.args.get('search', '').strip()

    # Base query
    query = WorkItem.query

    # Validate and apply status filter
    if status_filter != 'all':
        allowed_statuses = current_app.config.get('STATUS_OPTIONS', [])
        if status_filter in allowed_statuses:
            query = query.filter_by(status=status_filter)

    # Validate and apply search filter
    if search_query:
        is_valid, sanitized_query, error = validate_search_query(search_query, max_length=200)
        if not is_valid:
            flash(error, 'warning')
            sanitized_query = ''

        if sanitized_query:
            # Escape special characters for SQL LIKE
            safe_query = escape_sql_like(sanitized_query)
            search_pattern = f'%{safe_query}%'
            query = query.filter(
                db.or_(
                    WorkItem.item_number.ilike(search_pattern),
                    WorkItem.description.ilike(search_pattern),
                    WorkItem.location.ilike(search_pattern),
                    WorkItem.submitter_name.ilike(search_pattern),
                    WorkItem.detail.ilike(search_pattern)
                )
            )

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
                         search_query=search_query,
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
@limiter.limit("30 per hour")
def edit_item(item_id):
    """Edit work item details with input validation."""
    work_item = WorkItem.query.get_or_404(item_id)

    try:
        # Get and sanitize input
        item_number = sanitize_text_input(request.form.get('item_number'), max_length=50)
        location = sanitize_text_input(request.form.get('location'), max_length=200)
        description = sanitize_text_input(request.form.get('description'), max_length=500)
        detail = sanitize_text_input(request.form.get('detail'), max_length=5000)
        references = sanitize_text_input(request.form.get('references', ''), max_length=1000)

        # Validate fields
        from app.security import validate_item_number
        is_valid, error = validate_item_number(item_number)
        if not is_valid:
            flash(error, 'danger')
            return redirect(url_for('admin.view_item', item_id=item_id))

        is_valid, error = validate_text_field(location, 'Location', min_length=2, max_length=200)
        if not is_valid:
            flash(error, 'danger')
            return redirect(url_for('admin.view_item', item_id=item_id))

        is_valid, error = validate_text_field(description, 'Description', min_length=10, max_length=500)
        if not is_valid:
            flash(error, 'danger')
            return redirect(url_for('admin.view_item', item_id=item_id))

        is_valid, error = validate_text_field(detail, 'Detail', min_length=10, max_length=5000)
        if not is_valid:
            flash(error, 'danger')
            return redirect(url_for('admin.view_item', item_id=item_id))

        # Update basic fields
        work_item.item_number = item_number
        work_item.location = location
        work_item.description = description
        work_item.detail = detail
        work_item.references = references
        
        # Update photo captions
        photo_ids = request.form.getlist('photo_ids[]')
        photo_captions = request.form.getlist('photo_captions[]')

        for photo_id, caption in zip(photo_ids, photo_captions):
            from app.models import Photo
            photo = Photo.query.get(int(photo_id))
            if photo and photo.work_item_id == work_item.id:
                photo.caption = sanitize_text_input(caption, max_length=500)

        # Handle new photo uploads
        new_photo_files = request.files.getlist('new_photos[]')
        new_photo_captions = request.form.getlist('new_photo_captions[]')

        for photo_file, caption in zip(new_photo_files, new_photo_captions):
            if photo_file and photo_file.filename:
                # Validate file upload
                is_valid, error = validate_file_upload(photo_file)
                if not is_valid:
                    flash(f'Photo validation error: {error}', 'danger')
                    return redirect(url_for('admin.view_item', item_id=item_id))

                if allowed_file(photo_file.filename):
                    from app.models import Photo
                    if is_cloudinary_enabled():
                        # Upload to Cloudinary with security validation
                        upload_result = upload_image_to_cloudinary(photo_file)
                        new_photo = Photo(
                            filename=upload_result['public_id'].split('/')[-1],
                            caption=sanitize_text_input(caption, max_length=500) or '',
                            work_item_id=work_item.id,
                            cloudinary_public_id=upload_result['public_id'],
                            cloudinary_url=upload_result['secure_url']
                        )
                        db.session.add(new_photo)
                    else:
                        # Local storage (fallback) with security validation
                        filename = generate_unique_filename(photo_file.filename)
                        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        photo_file.save(filepath)
                        _, _, final_path = resize_image(filepath, current_app.config['PHOTO_MAX_WIDTH'])
                        final_filename = os.path.basename(final_path)

                        new_photo = Photo(
                            filename=final_filename,
                            caption=sanitize_text_input(caption, max_length=500) or '',
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
@limiter.limit("50 per hour")
def assign_item(item_id):
    """Assign work item to crew member with revision notes and validation."""
    work_item = WorkItem.query.get_or_404(item_id)

    old_status = work_item.status
    new_status = sanitize_text_input(request.form.get('status'), max_length=50)
    assigned_to = sanitize_text_input(request.form.get('assigned_to'), max_length=100)
    revision_notes = sanitize_text_input(request.form.get('revision_notes'), max_length=2000)
    admin_name = session.get('crew_name', 'admin')

    # Validate status
    is_valid, error = validate_status(new_status)
    if not is_valid:
        flash(error, 'danger')
        return redirect(url_for('admin.view_item', item_id=item_id))

    # Validate crew member if assigned
    if assigned_to:
        is_valid, error = validate_crew_member(assigned_to)
        if not is_valid:
            flash(error, 'danger')
            return redirect(url_for('admin.view_item', item_id=item_id))
    
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

        # Send SMS notification if enabled and crew member is assigned
        if assigned_to and current_app.config.get('ENABLE_NOTIFICATIONS'):
            send_assignment_notification(work_item, assigned_to, revision_notes)

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
@limiter.limit("50 per hour")
def save_admin_notes(item_id):
    """Save admin notes for a work item (admin only) with validation."""
    work_item = WorkItem.query.get_or_404(item_id)

    try:
        # Sanitize admin notes
        admin_notes = sanitize_text_input(request.form.get('admin_notes', ''), max_length=5000)

        # Validate if provided
        if admin_notes:
            is_valid, error = validate_text_field(admin_notes, 'Admin notes', min_length=1, max_length=5000, required=False)
            if not is_valid:
                flash(error, 'danger')
                return redirect(url_for('admin.view_item', item_id=item_id))

        work_item.admin_notes = admin_notes
        work_item.admin_notes_updated_at = datetime.utcnow()

        db.session.commit()
        flash('Admin notes saved successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving admin notes: {str(e)}', 'danger')

    return redirect(url_for('admin.view_item', item_id=item_id))
