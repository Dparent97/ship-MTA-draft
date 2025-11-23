from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app import db, limiter
from app.models import WorkItem, Photo, Comment
from app.utils import allowed_file, generate_unique_filename, resize_image, get_next_draft_number
from app.security import (
    sanitize_text_input, validate_item_number, validate_text_field,
    validate_file_upload, sanitize_filename
)
from app.cloudinary_utils import upload_image_to_cloudinary, delete_image_from_cloudinary, is_cloudinary_enabled
from datetime import datetime
import os


bp = Blueprint('crew', __name__, url_prefix='/crew')


def crew_required(f):
    """Decorator to require crew authentication."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('crew_authenticated'):
            return redirect(url_for('auth.crew_login'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/submit', methods=['GET', 'POST'])
@crew_required
@limiter.limit("20 per hour")
def submit_form():
    """Crew submission form with input validation."""
    if request.method == 'POST':
        # Get and sanitize form data
        item_number = sanitize_text_input(request.form.get('item_number'), max_length=50) or get_next_draft_number()
        location = sanitize_text_input(request.form.get('location'), max_length=200)
        description = sanitize_text_input(request.form.get('description'), max_length=500)
        detail = sanitize_text_input(request.form.get('detail'), max_length=5000)
        references = sanitize_text_input(request.form.get('references', ''), max_length=1000)
        submitter_name = session.get('crew_name')

        # Validate item number
        is_valid, error = validate_item_number(item_number)
        if not is_valid:
            flash(error, 'danger')
            return redirect(url_for('crew.submit_form'))

        # Validate required fields
        is_valid, error = validate_text_field(location, 'Location', min_length=2, max_length=200)
        if not is_valid:
            flash(error, 'danger')
            return redirect(url_for('crew.submit_form'))

        is_valid, error = validate_text_field(description, 'Description', min_length=10, max_length=500)
        if not is_valid:
            flash(error, 'danger')
            return redirect(url_for('crew.submit_form'))

        is_valid, error = validate_text_field(detail, 'Detail', min_length=10, max_length=5000)
        if not is_valid:
            flash(error, 'danger')
            return redirect(url_for('crew.submit_form'))

        # Check if item already exists (duplicate handling)
        existing_item = WorkItem.query.filter_by(item_number=item_number).first()
        
        if existing_item:
            # Handle existing item
            if existing_item.status == 'Completed Review':
                flash(f'Item {item_number} has already been approved. Contact admin to modify.', 'warning')
                return redirect(url_for('crew.submit_form'))
            
            # This is an UPDATE to existing item
            is_update = True
            work_item = existing_item
            work_item.last_modified_by = session.get('crew_name')
            work_item.last_modified_at = datetime.utcnow()
        else:
            # This is a NEW item
            is_update = False
            work_item = WorkItem(
                item_number=item_number,
                submitter_name=submitter_name,
                original_submitter=submitter_name,
                assigned_to=submitter_name  # Auto-assign to submitter
            )

        # Update/set all fields
        work_item.location = location
        work_item.ns_equipment = 'N/A'  # Keep for database compatibility
        work_item.description = description
        work_item.detail = detail
        work_item.references = references
        if not is_update:
            work_item.submitter_name = submitter_name

        # Validate photos (now optional)
        photo_files = request.files.getlist('photos')
        photo_captions = request.form.getlist('photo_captions')

        # Sanitize photo captions
        sanitized_captions = [sanitize_text_input(cap, max_length=500) for cap in photo_captions]

        # Filter photos and captions together, keeping them synchronized
        # This ensures each photo file is paired with its correct caption
        valid_photo_pairs = []
        for photo, caption in zip(photo_files, sanitized_captions):
            if photo and photo.filename:
                # Validate file upload
                is_valid, error = validate_file_upload(photo)
                if not is_valid:
                    flash(f'Photo validation error: {error}', 'danger')
                    return redirect(url_for('crew.submit_form'))
                valid_photo_pairs.append((photo, caption))

        if len(valid_photo_pairs) > current_app.config['PHOTO_MAX_COUNT']:
            flash(f'Maximum {current_app.config["PHOTO_MAX_COUNT"]} photos allowed', 'danger')
            return redirect(url_for('crew.submit_form'))

        try:
            db.session.add(work_item)
            db.session.flush()  # Get the ID without committing

            # Process photos with their correct captions
            for idx, (photo_file, caption) in enumerate(valid_photo_pairs):
                if photo_file and allowed_file(photo_file.filename):
                    if is_cloudinary_enabled():
                        # Upload to Cloudinary
                        try:
                            upload_result = upload_image_to_cloudinary(photo_file)
                            photo = Photo(
                                filename=upload_result['public_id'].split('/')[-1],  # Use last part as filename
                                caption=caption or '',
                                work_item_id=work_item.id,
                                cloudinary_public_id=upload_result['public_id'],
                                cloudinary_url=upload_result['secure_url']
                            )
                            db.session.add(photo)
                        except Exception as e:
                            raise ValueError(f'Error uploading photo {idx + 1} to Cloudinary: {str(e)}')
                    else:
                        # Local storage (fallback)
                        filename = generate_unique_filename(photo_file.filename)
                        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        photo_file.save(filepath)
                        _, _, final_path = resize_image(filepath, current_app.config['PHOTO_MAX_WIDTH'])
                        final_filename = os.path.basename(final_path)
                        photo = Photo(
                            filename=final_filename,
                            caption=caption or '',
                            work_item_id=work_item.id
                        )
                        db.session.add(photo)
                else:
                    raise ValueError(f'Invalid file type for photo {idx + 1}')

            db.session.commit()
            
            if is_update:
                flash(f'Work item {item_number} updated successfully!', 'success')
            else:
                flash(f'Work item {item_number} submitted successfully!', 'success')
            
            return redirect(url_for('crew.success', item_number=item_number))

        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting form: {str(e)}', 'danger')
            return redirect(url_for('crew.submit_form'))

    # GET request - show form
    next_item_number = get_next_draft_number()
    crew_name = session.get('crew_name')
    
    # Get items assigned to this crew member
    try:
        assigned_items = WorkItem.query.filter_by(
            assigned_to=crew_name
        ).filter(WorkItem.status.in_(['Submitted', 'Needs Revision', 'Awaiting Photos'])).all()
    except Exception as e:
        print(f"Error querying assigned items: {e}")
        assigned_items = []
    
    # Get all in-progress items (all statuses except Completed Review)
    try:
        in_progress_items = WorkItem.query.filter(
            WorkItem.status != 'Completed Review'
        ).order_by(WorkItem.submitted_at.desc()).all()
    except Exception as e:
        print(f"Error querying in progress items: {e}")
        in_progress_items = []
    
    # Get all completed items
    try:
        completed_items = WorkItem.query.filter_by(
            status='Completed Review'
        ).order_by(WorkItem.item_number).all()
    except Exception as e:
        print(f"Error querying completed items: {e}")
        completed_items = []
    
    return render_template('crew_form.html', 
                         next_item_number=next_item_number,
                         crew_name=crew_name,
                         min_photos=current_app.config['PHOTO_MIN_COUNT'],
                         max_photos=current_app.config['PHOTO_MAX_COUNT'],
                         assigned_items=assigned_items,
                         in_progress_items=in_progress_items,
                         completed_items=completed_items,
                         ev_yard_items=current_app.config['EV_YARD_ITEMS'],
                         draft_items=current_app.config['DRAFT_ITEMS'])


@bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@crew_required
@limiter.limit("30 per hour")
def edit_assigned_item(item_id):
    """Edit an assigned work item (crew member must be assigned to it)."""
    crew_name = session.get('crew_name')
    work_item = WorkItem.query.get_or_404(item_id)

    # Permission check: Verify this item is assigned to the current crew member OR they are the original submitter
    if work_item.submitter_name != crew_name and work_item.assigned_to != crew_name:
        flash('You do not have permission to edit this item. Only the original submitter or assigned crew member can edit.', 'danger')
        return redirect(url_for('crew.submit_form'))

    # Only allow editing if status is "Submitted", "Needs Revision" or "Awaiting Photos"
    if work_item.status not in ['Submitted', 'Needs Revision', 'Awaiting Photos']:
        flash(f'This item cannot be edited. Current status: {work_item.status}', 'warning')
        return redirect(url_for('crew.submit_form'))

    if request.method == 'POST':
        try:
            # Get and validate input
            description = sanitize_text_input(request.form.get('description'), max_length=500)
            detail = sanitize_text_input(request.form.get('detail'), max_length=5000)
            references = sanitize_text_input(request.form.get('references', ''), max_length=1000)

            # Validate fields
            is_valid, error = validate_text_field(description, 'Description', min_length=10, max_length=500)
            if not is_valid:
                flash(error, 'danger')
                return redirect(url_for('crew.edit_assigned_item', item_id=item_id))

            is_valid, error = validate_text_field(detail, 'Detail', min_length=10, max_length=5000)
            if not is_valid:
                flash(error, 'danger')
                return redirect(url_for('crew.edit_assigned_item', item_id=item_id))

            # Update allowed fields only
            work_item.description = description
            work_item.detail = detail
            work_item.references = references

            # Auto-update tracking fields
            work_item.last_modified_by = crew_name
            work_item.last_modified_at = datetime.utcnow()

            # Change status from "Needs Revision" to "Submitted" on save
            old_status = work_item.status
            work_item.status = 'Submitted'
            work_item.needs_revision = False

            # Clear revision notes after addressing them
            work_item.revision_notes = None

            # Update existing photo captions
            photo_ids = request.form.getlist('photo_ids[]')
            photo_captions = request.form.getlist('photo_captions[]')

            for photo_id, caption in zip(photo_ids, photo_captions):
                photo = Photo.query.get(int(photo_id))
                if photo and photo.work_item_id == work_item.id:
                    # Sanitize caption
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
                        return redirect(url_for('crew.edit_assigned_item', item_id=item_id))

                    if allowed_file(photo_file.filename):
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
            flash(f'Work item {work_item.item_number} updated successfully! Status changed from "{old_status}" to "Submitted".', 'success')
            return redirect(url_for('crew.success', item_number=work_item.item_number))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating work item: {str(e)}', 'danger')
            return redirect(url_for('crew.edit_assigned_item', item_id=item_id))

    # GET request - show edit form
    return render_template('crew_edit.html',
                         work_item=work_item,
                         crew_name=crew_name,
                         max_photos=current_app.config['PHOTO_MAX_COUNT'])


@bp.route('/delete-photo/<int:item_id>/<int:photo_id>')
@crew_required
def delete_assigned_photo(item_id, photo_id):
    """Delete a photo from an assigned work item."""
    crew_name = session.get('crew_name')
    work_item = WorkItem.query.get_or_404(item_id)

    # Permission check
    if work_item.assigned_to != crew_name:
        flash('You do not have permission to modify this item.', 'danger')
        return redirect(url_for('crew.submit_form'))

    photo = Photo.query.get_or_404(photo_id)

    # Verify photo belongs to the work item
    if photo.work_item_id != item_id:
        flash('Invalid photo', 'danger')
        return redirect(url_for('crew.edit_assigned_item', item_id=item_id))

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

    return redirect(url_for('crew.edit_assigned_item', item_id=item_id))


@bp.route('/view/<int:item_id>')
@crew_required
def view_item(item_id):
    """View a work item (read-only)."""
    work_item = WorkItem.query.get_or_404(item_id)
    crew_name = session.get('crew_name')
    
    # Determine if this user can edit (must match edit_assigned_item permissions)
    can_edit = (work_item.submitter_name == crew_name or work_item.assigned_to == crew_name) and \
               (work_item.status in ['Submitted', 'Needs Revision', 'Awaiting Photos'])
    
    return render_template('crew_view.html',
                         work_item=work_item,
                         crew_name=crew_name,
                         can_edit=can_edit)


@bp.route('/success')
@crew_required
def success():
    """Success page after submission."""
    item_number = request.args.get('item_number', 'Unknown')
    return render_template('crew_success.html', item_number=item_number)
