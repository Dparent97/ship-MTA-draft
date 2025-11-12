from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, jsonify
from app import db
from app.models import WorkItem, Photo, Comment
from app.utils import allowed_file, generate_unique_filename, resize_image, get_next_draft_number
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
def submit_form():
    """Crew submission form."""
    if request.method == 'POST':
        # Get form data
        item_number = request.form.get('item_number') or get_next_draft_number()
        location = request.form.get('location')
        description = request.form.get('description')
        detail = request.form.get('detail')
        references = request.form.get('references', '')
        submitter_name = session.get('crew_name')

        # Validate required fields
        if not all([location, description, detail]):
            flash('All required fields must be filled out', 'danger')
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
                original_submitter=submitter_name
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
        
        # Filter out empty photo uploads
        valid_photos = [f for f in photo_files if f and f.filename]

        if len(valid_photos) > current_app.config['PHOTO_MAX_COUNT']:
            flash(f'Maximum {current_app.config["PHOTO_MAX_COUNT"]} photos allowed', 'danger')
            return redirect(url_for('crew.submit_form'))

        try:
            db.session.add(work_item)
            db.session.flush()  # Get the ID without committing

            # Process photos
            for idx, photo_file in enumerate(valid_photos):
                if photo_file and allowed_file(photo_file.filename):
                    # Generate unique filename
                    filename = generate_unique_filename(photo_file.filename)
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

                    # Save file
                    photo_file.save(filepath)

                    # Resize image (returns new path if HEIC was converted)
                    _, _, final_path = resize_image(filepath, current_app.config['PHOTO_MAX_WIDTH'])
                    final_filename = os.path.basename(final_path)

                    # Get caption if provided, otherwise use empty string
                    caption = photo_captions[idx] if idx < len(photo_captions) else ''

                    # Create photo record
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
        ).filter(WorkItem.status.in_(['Needs Revision', 'Awaiting Photos'])).all()
    except Exception as e:
        print(f"Error querying assigned items: {e}")
        assigned_items = []
    
    # Get dynamic approved items for draft dropdown
    try:
        approved_items = WorkItem.query.filter_by(
            status='Completed Review'
        ).order_by(WorkItem.item_number).all()
    except Exception as e:
        print(f"Error querying approved items: {e}")
        approved_items = []
    
    # Combine static and dynamic items
    all_draft_items = current_app.config['DRAFT_ITEMS'].copy()
    for item in approved_items:
        item_entry = f"{item.item_number} - {item.description[:50]}"
        if item_entry not in all_draft_items:
            all_draft_items.append(item_entry)
    
    return render_template('crew_form.html', 
                         next_item_number=next_item_number,
                         crew_name=crew_name,
                         min_photos=current_app.config['PHOTO_MIN_COUNT'],
                         max_photos=current_app.config['PHOTO_MAX_COUNT'],
                         ev_yard_items=current_app.config['EV_YARD_ITEMS'],
                         draft_items=all_draft_items,
                         assigned_items=assigned_items)


@bp.route('/load-assignment/<int:item_id>')
@crew_required
def load_assignment(item_id):
    """Load an assigned work item for editing."""
    crew_name = session.get('crew_name')
    work_item = WorkItem.query.get_or_404(item_id)
    
    # Verify this item is assigned to them
    if work_item.assigned_to != crew_name:
        return jsonify({'error': 'This item is not assigned to you'}), 403
    
    # Return as JSON for JavaScript to populate form
    return jsonify({
        'item_number': work_item.item_number,
        'location': work_item.location,
        'description': work_item.description,
        'detail': work_item.detail,
        'references': work_item.references or '',
        'revision_notes': work_item.revision_notes or '',
        'photos': [{'id': p.id, 'caption': p.caption, 'filename': p.filename} for p in work_item.photos]
    })


@bp.route('/success')
@crew_required
def success():
    """Success page after submission."""
    item_number = request.args.get('item_number', 'Unknown')
    return render_template('crew_success.html', item_number=item_number)
