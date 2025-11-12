# Ship Maintenance Draft Generator - Cursor Build Guide

## 🎯 Project Overview

A mobile-first web application for standardizing ship maintenance work item documentation. Crew members fill out forms on their phones, upload photos, and the system generates professionally formatted .docx files for the Port Engineer.

### Key Features
- ✅ Single login for crew with name selection dropdown
- ✅ Mobile-optimized form with photo upload
- ✅ Auto-resizes photos to 4" width for emailing
- ✅ Generates .docx files matching official template
- ✅ Admin dashboard for review and batch download
- ✅ Status tracking: Submitted → Reviewed → Sent to PE
- ✅ Works on iPhone and Android

---

## 📋 Technical Decisions

Based on your requirements:

1. **Item Numbers**: Start from DRAFT_0020 (you have 0001-0019 already)
2. **Crew Access**: Single password, dropdown to select name from list
3. **Location Field**: Open text input (not dropdown)
4. **NS Equipment Field**: Open text input (not dropdown)
5. **Photo Captions**: Required for each photo (minimum 2 photos)
6. **Batch Download**: Creates .zip file with multiple .docx files
7. **Notifications**: None - admin checks dashboard regularly

---

## 🏗️ Tech Stack

### Backend
- **Python 3.9+** - Core language
- **Flask 3.0** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **python-docx** - Word document generation
- **Pillow** - Image processing and resizing
- **Werkzeug** - Password hashing & security

### Frontend
- **Bootstrap 5.3** - Responsive UI framework
- **Vanilla JavaScript** - No framework needed
- **HTML5** - Camera integration for mobile

### Database
- **SQLite** - Simple, serverless database

### Deployment
- **Railway.app** or **Render.com** - Cloud hosting

---

## 📁 Project Structure

```
ship-maintenance-tracker/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models.py                # Database models
│   ├── auth.py                  # Authentication routes
│   ├── crew.py                  # Crew submission routes
│   ├── admin.py                 # Admin dashboard routes
│   ├── docx_generator.py        # Document generation logic
│   ├── utils.py                 # Helper functions (photo resize, etc.)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Custom styles
│   │   ├── js/
│   │   │   └── main.js          # Client-side JS
│   │   └── uploads/             # Uploaded photos (temp)
│   └── templates/
│       ├── base.html            # Base template
│       ├── login.html           # Login page
│       ├── crew_form.html       # Submission form
│       ├── crew_success.html    # Success message
│       ├── admin_login.html     # Admin login
│       └── admin_dashboard.html # Admin interface
├── migrations/                   # Database migrations (if using Flask-Migrate)
├── uploads/                      # Persistent photo storage
├── generated_docs/               # Generated .docx files
├── config.py                     # Configuration
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore file
├── run.py                        # Application entry point
└── README.md                     # Setup instructions
```

---

## 🚀 Step-by-Step Implementation

### Phase 1: Initial Setup (30 min)

#### 1. Create Project Directory
```bash
mkdir ship-maintenance-tracker
cd ship-maintenance-tracker
```

#### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
```

#### 3. Create requirements.txt
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
python-docx==1.1.0
Pillow==10.1.0
Werkzeug==3.0.1
python-dotenv==1.0.0
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Create Directory Structure
```bash
mkdir -p app/static/{css,js,uploads}
mkdir -p app/templates
mkdir uploads generated_docs
```

---

### Phase 2: Configuration & Models (45 min)

#### Create `config.py`
```python
import os
from datetime import timedelta

class Config:
    # Secret key for sessions (change in production!)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///maintenance.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File uploads
    UPLOAD_FOLDER = 'uploads'
    GENERATED_DOCS_FOLDER = 'generated_docs'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Photo settings
    PHOTO_MAX_WIDTH = 576  # 4 inches at 144 DPI (576 pixels)
    PHOTO_MIN_COUNT = 2
    PHOTO_MAX_COUNT = 6
    
    # Crew access
    CREW_PASSWORD = os.environ.get('CREW_PASSWORD') or 'crew2026'
    
    # Admin access
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin2026'
    
    # Crew members (can be moved to database later)
    CREW_MEMBERS = [
        'Derek',
        'Mark',
        'Kaitlyn',
        'Maverick',
        'Zach',
        'Art',
        'Al'
    ]
    
    # Session timeout
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
```

#### Create `app/__init__.py`
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Ensure upload folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['GENERATED_DOCS_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'uploads'), exist_ok=True)
    
    # Register blueprints
    from app import auth, crew, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(crew.bp)
    app.register_blueprint(admin.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
```

#### Create `app/models.py`
```python
from app import db
from datetime import datetime

class WorkItem(db.Model):
    __tablename__ = 'work_items'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Item information
    item_number = db.Column(db.String(50), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    ns_equipment = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    detail = db.Column(db.Text, nullable=False)
    references = db.Column(db.Text)  # Optional
    
    # Metadata
    submitter_name = db.Column(db.String(100), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Submitted')  # Submitted, Reviewed, Sent to PE
    
    # Relationships
    photos = db.relationship('Photo', backref='work_item', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<WorkItem {self.item_number}>'

class Photo(db.Model):
    __tablename__ = 'photos'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500), nullable=False)
    work_item_id = db.Column(db.Integer, db.ForeignKey('work_items.id'), nullable=False)
    
    def __repr__(self):
        return f'<Photo {self.filename}>'
```

---

### Phase 3: Utilities (30 min)

#### Create `app/utils.py`
```python
from PIL import Image
import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(original_filename):
    """Generate unique filename while preserving extension"""
    ext = original_filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return unique_name

def resize_image(image_path, max_width=576):
    """
    Resize image to max_width (4 inches at 144 DPI = 576 pixels)
    Maintains aspect ratio
    """
    with Image.open(image_path) as img:
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        # Calculate new dimensions
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Save optimized image
        img.save(image_path, 'JPEG', quality=85, optimize=True)
        
        return img.width, img.height

def get_next_draft_number():
    """Get the next available DRAFT number (starting from DRAFT_0020)"""
    from app.models import WorkItem
    
    # Get all existing draft numbers
    existing_items = WorkItem.query.filter(
        WorkItem.item_number.like('DRAFT_%')
    ).all()
    
    if not existing_items:
        return 'DRAFT_0020'
    
    # Extract numbers
    numbers = []
    for item in existing_items:
        try:
            num = int(item.item_number.replace('DRAFT_', ''))
            numbers.append(num)
        except ValueError:
            continue
    
    # Get next number
    if numbers:
        next_num = max(numbers) + 1
    else:
        next_num = 20
    
    return f'DRAFT_{next_num:04d}'

def format_datetime(dt):
    """Format datetime for display"""
    if dt:
        return dt.strftime('%Y-%m-%d %H:%M')
    return ''
```

---

### Phase 4: Authentication Routes (30 min)

#### Create `app/auth.py`
```python
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app

bp = Blueprint('auth', __name__)

@bp.route('/')
def index():
    """Landing page - redirect to crew login"""
    if session.get('is_admin'):
        return redirect(url_for('admin.dashboard'))
    elif session.get('crew_authenticated'):
        return redirect(url_for('crew.submit_form'))
    return redirect(url_for('auth.crew_login'))

@bp.route('/crew-login', methods=['GET', 'POST'])
def crew_login():
    """Crew member login"""
    if request.method == 'POST':
        password = request.form.get('password')
        crew_name = request.form.get('crew_name')
        
        if password == current_app.config['CREW_PASSWORD'] and crew_name:
            session['crew_authenticated'] = True
            session['crew_name'] = crew_name
            session.permanent = True
            return redirect(url_for('crew.submit_form'))
        else:
            flash('Invalid password or crew name not selected', 'danger')
    
    crew_members = current_app.config['CREW_MEMBERS']
    return render_template('login.html', crew_members=crew_members)

@bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if (username == current_app.config['ADMIN_USERNAME'] and 
            password == current_app.config['ADMIN_PASSWORD']):
            session['is_admin'] = True
            session.permanent = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')
    
    return render_template('admin_login.html')

@bp.route('/logout')
def logout():
    """Logout (crew or admin)"""
    is_admin = session.get('is_admin', False)
    session.clear()
    
    if is_admin:
        return redirect(url_for('auth.admin_login'))
    return redirect(url_for('auth.crew_login'))
```

---

### Phase 5: Crew Routes (45 min)

#### Create `app/crew.py`
```python
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app import db
from app.models import WorkItem, Photo
from app.utils import allowed_file, generate_unique_filename, resize_image, get_next_draft_number
import os

bp = Blueprint('crew', __name__, url_prefix='/crew')

def crew_required(f):
    """Decorator to require crew authentication"""
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
    """Crew submission form"""
    if request.method == 'POST':
        # Get form data
        item_number = request.form.get('item_number') or get_next_draft_number()
        location = request.form.get('location')
        ns_equipment = request.form.get('ns_equipment')
        description = request.form.get('description')
        detail = request.form.get('detail')
        references = request.form.get('references', '')
        submitter_name = session.get('crew_name')
        
        # Validate required fields
        if not all([location, ns_equipment, description, detail]):
            flash('All required fields must be filled out', 'danger')
            return redirect(url_for('crew.submit_form'))
        
        # Validate photos
        photo_files = request.files.getlist('photos')
        photo_captions = request.form.getlist('photo_captions')
        
        if len(photo_files) < current_app.config['PHOTO_MIN_COUNT']:
            flash(f'Minimum {current_app.config["PHOTO_MIN_COUNT"]} photos required', 'danger')
            return redirect(url_for('crew.submit_form'))
        
        if len(photo_files) > current_app.config['PHOTO_MAX_COUNT']:
            flash(f'Maximum {current_app.config["PHOTO_MAX_COUNT"]} photos allowed', 'danger')
            return redirect(url_for('crew.submit_form'))
        
        # Validate all photos have captions
        valid_photos = [f for f in photo_files if f and f.filename]
        if len(photo_captions) != len(valid_photos):
            flash('Each photo must have a caption', 'danger')
            return redirect(url_for('crew.submit_form'))
        
        for caption in photo_captions:
            if not caption.strip():
                flash('All photo captions must be filled out', 'danger')
                return redirect(url_for('crew.submit_form'))
        
        # Create work item
        work_item = WorkItem(
            item_number=item_number,
            location=location,
            ns_equipment=ns_equipment,
            description=description,
            detail=detail,
            references=references,
            submitter_name=submitter_name
        )
        
        try:
            db.session.add(work_item)
            db.session.flush()  # Get the ID without committing
            
            # Process photos
            for idx, (photo_file, caption) in enumerate(zip(valid_photos, photo_captions)):
                if photo_file and allowed_file(photo_file.filename):
                    # Generate unique filename
                    filename = generate_unique_filename(photo_file.filename)
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    
                    # Save file
                    photo_file.save(filepath)
                    
                    # Resize image
                    resize_image(filepath, current_app.config['PHOTO_MAX_WIDTH'])
                    
                    # Create photo record
                    photo = Photo(
                        filename=filename,
                        caption=caption,
                        work_item_id=work_item.id
                    )
                    db.session.add(photo)
                else:
                    raise ValueError(f'Invalid file type for photo {idx + 1}')
            
            db.session.commit()
            flash(f'Work item {item_number} submitted successfully!', 'success')
            return redirect(url_for('crew.success', item_number=item_number))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting form: {str(e)}', 'danger')
            return redirect(url_for('crew.submit_form'))
    
    # GET request - show form
    next_item_number = get_next_draft_number()
    crew_name = session.get('crew_name')
    return render_template('crew_form.html', 
                         next_item_number=next_item_number,
                         crew_name=crew_name,
                         min_photos=current_app.config['PHOTO_MIN_COUNT'],
                         max_photos=current_app.config['PHOTO_MAX_COUNT'])

@bp.route('/success')
@crew_required
def success():
    """Success page after submission"""
    item_number = request.args.get('item_number', 'Unknown')
    return render_template('crew_success.html', item_number=item_number)
```

---

### Phase 6: Document Generation (60 min)

#### Create `app/docx_generator.py`
```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from app.models import WorkItem
from flask import current_app
import os

def generate_docx(work_item_id):
    """
    Generate a .docx file matching the template format
    Returns the filepath of the generated document
    """
    from app.models import WorkItem
    
    work_item = WorkItem.query.get_or_404(work_item_id)
    
    # Create document
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    
    # Title
    title = doc.add_paragraph()
    title_run = title.add_run('WORK ITEM DRAFT TEMPLATE')
    title_run.bold = True
    title_run.font.size = Pt(14)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()  # Blank line
    
    # Item NO.
    p = doc.add_paragraph()
    p.add_run('Item NO.: ').bold = True
    p.add_run(work_item.item_number)
    
    # Location
    p = doc.add_paragraph()
    p.add_run('Location: ').bold = True
    p.add_run(work_item.location)
    
    # NS Equipment
    p = doc.add_paragraph()
    p.add_run('NS Equipment: ').bold = True
    p.add_run(work_item.ns_equipment)
    
    doc.add_paragraph()  # Blank line
    
    # Description heading
    heading = doc.add_paragraph()
    heading_run = heading.add_run('Description:')
    heading_run.bold = True
    heading_run.font.size = Pt(12)
    
    # Description content
    doc.add_paragraph(work_item.description)
    
    doc.add_paragraph()  # Blank line
    
    # Detail heading
    heading = doc.add_paragraph()
    heading_run = heading.add_run('Detail:')
    heading_run.bold = True
    heading_run.font.size = Pt(12)
    
    # Detail content
    doc.add_paragraph(work_item.detail)
    
    # References (if provided)
    if work_item.references:
        doc.add_paragraph()  # Blank line
        heading = doc.add_paragraph()
        heading_run = heading.add_run('References/Supporting Documents:')
        heading_run.bold = True
        heading_run.font.size = Pt(12)
        doc.add_paragraph(work_item.references)
    
    # Photos section
    doc.add_paragraph()  # Blank line
    heading = doc.add_paragraph()
    heading_run = heading.add_run('PHOTOS')
    heading_run.bold = True
    heading_run.font.size = Pt(12)
    
    # Add each photo
    for idx, photo in enumerate(work_item.photos, 1):
        doc.add_paragraph()  # Blank line
        
        # Photo
        photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], photo.filename)
        if os.path.exists(photo_path):
            try:
                doc.add_picture(photo_path, width=Inches(4))
            except Exception as e:
                doc.add_paragraph(f'[Error loading photo: {photo.filename}]')
        
        # Caption
        caption_p = doc.add_paragraph()
        caption_p.add_run(f'Photo {idx} Caption: ').italic = True
        caption_p.add_run(photo.caption)
    
    # Metadata footer
    doc.add_paragraph()
    doc.add_paragraph()
    footer = doc.add_paragraph()
    footer_run = footer.add_run(
        f'Submitted by: {work_item.submitter_name} | '
        f'Date: {work_item.submitted_at.strftime("%Y-%m-%d %H:%M")}'
    )
    footer_run.font.size = Pt(9)
    footer_run.font.color.rgb = RGBColor(128, 128, 128)
    
    # Save document
    filename = f"{work_item.item_number}_{work_item.description[:30].replace(' ', '_')}.docx"
    filepath = os.path.join(current_app.config['GENERATED_DOCS_FOLDER'], filename)
    doc.save(filepath)
    
    return filepath

def generate_multiple_docx(work_item_ids):
    """
    Generate multiple .docx files and return list of filepaths
    """
    filepaths = []
    for work_item_id in work_item_ids:
        try:
            filepath = generate_docx(work_item_id)
            filepaths.append(filepath)
        except Exception as e:
            print(f"Error generating document for work item {work_item_id}: {e}")
    return filepaths
```

---

### Phase 7: Admin Routes (60 min)

#### Create `app/admin.py`
```python
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file, current_app
from app import db
from app.models import WorkItem
from app.docx_generator import generate_docx, generate_multiple_docx
from app.utils import format_datetime
import os
import zipfile
from io import BytesIO

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to require admin authentication"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard showing all work items"""
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
    """View full details of a work item"""
    work_item = WorkItem.query.get_or_404(item_id)
    return render_template('admin_view_item.html', 
                         work_item=work_item,
                         format_datetime=format_datetime)

@bp.route('/update-status/<int:item_id>', methods=['POST'])
@admin_required
def update_status(item_id):
    """Update the status of a work item"""
    work_item = WorkItem.query.get_or_404(item_id)
    new_status = request.form.get('status')
    
    if new_status in ['Submitted', 'Reviewed', 'Sent to PE']:
        work_item.status = new_status
        db.session.commit()
        flash(f'Status updated to: {new_status}', 'success')
    else:
        flash('Invalid status', 'danger')
    
    return redirect(url_for('admin.view_item', item_id=item_id))

@bp.route('/download/<int:item_id>')
@admin_required
def download_single(item_id):
    """Download a single work item as .docx"""
    try:
        filepath = generate_docx(item_id)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        flash(f'Error generating document: {str(e)}', 'danger')
        return redirect(url_for('admin.dashboard'))

@bp.route('/download-batch', methods=['POST'])
@admin_required
def download_batch():
    """Download multiple work items as a .zip file"""
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
    """Delete a work item (use with caution)"""
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
```

---

### Phase 8: Templates (90 min)

I'll provide the key templates. You'll need to create these HTML files:

#### `app/templates/base.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Ship Maintenance Tracker{% endblock %}</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-dark bg-primary">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">⚓ Ship Maintenance Tracker</span>
            {% if session.get('crew_authenticated') or session.get('is_admin') %}
            <a href="{{ url_for('auth.logout') }}" class="btn btn-outline-light btn-sm">Logout</a>
            {% endif %}
        </div>
    </nav>

    <!-- Flash Messages -->
    <div class="container mt-3">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    <!-- Main Content -->
    <main class="container my-4">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="text-center text-muted mt-5 py-3">
        <small>&copy; 2026 Ship Maintenance Tracker</small>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JS -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

#### `app/templates/login.html`
```html
{% extends "base.html" %}

{% block title %}Crew Login{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow">
            <div class="card-body">
                <h2 class="card-title text-center mb-4">Crew Login</h2>
                
                <form method="POST">
                    <div class="mb-3">
                        <label for="crew_name" class="form-label">Your Name *</label>
                        <select class="form-select form-select-lg" id="crew_name" name="crew_name" required>
                            <option value="">Select your name...</option>
                            {% for name in crew_members %}
                            <option value="{{ name }}">{{ name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label for="password" class="form-label">Crew Password *</label>
                        <input type="password" class="form-control form-control-lg" 
                               id="password" name="password" required>
                    </div>
                    
                    <button type="submit" class="btn btn-primary btn-lg w-100">
                        Login
                    </button>
                </form>
                
                <hr class="my-4">
                
                <div class="text-center">
                    <a href="{{ url_for('auth.admin_login') }}" class="text-muted small">
                        Admin Login
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

#### `app/templates/crew_form.html`
```html
{% extends "base.html" %}

{% block title %}Submit Work Item{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0">Submit Work Item Draft</h3>
                <small>Submitting as: <strong>{{ crew_name }}</strong></small>
            </div>
            <div class="card-body">
                <form method="POST" enctype="multipart/form-data" id="workItemForm">
                    
                    <!-- Item Number -->
                    <div class="mb-3">
                        <label for="item_number" class="form-label">
                            Item Number
                            <small class="text-muted">(Auto-suggested, or enter your own)</small>
                        </label>
                        <input type="text" class="form-control" id="item_number" 
                               name="item_number" value="{{ next_item_number }}">
                    </div>
                    
                    <!-- Location -->
                    <div class="mb-3">
                        <label for="location" class="form-label">Location *</label>
                        <input type="text" class="form-control" id="location" 
                               name="location" placeholder="e.g., Engine Room, Main Deck, Bridge" required>
                        <small class="form-text text-muted">
                            Examples: Engine Room, Main Deck, Bridge, Pilot House, Magazine, Galley, Crew Quarters
                        </small>
                    </div>
                    
                    <!-- NS Equipment -->
                    <div class="mb-3">
                        <label for="ns_equipment" class="form-label">NS Equipment *</label>
                        <input type="text" class="form-control" id="ns_equipment" 
                               name="ns_equipment" placeholder="e.g., Main Propulsion Prime Movers" required>
                        <small class="form-text text-muted">
                            Examples: Main Propulsion Prime Movers, Electrical Systems, HVAC, Deck Machinery, Navigation Equipment
                        </small>
                    </div>
                    
                    <!-- Description -->
                    <div class="mb-3">
                        <label for="description" class="form-label">Description (Brief Summary) *</label>
                        <textarea class="form-control" id="description" name="description" 
                                  rows="2" maxlength="200" required
                                  placeholder="Brief 1-2 sentence description (max 200 characters)"></textarea>
                        <small class="form-text text-muted">
                            Example: "Port & Stbd ME Exhaust insulation overhaul"
                        </small>
                    </div>
                    
                    <!-- Detail -->
                    <div class="mb-3">
                        <label for="detail" class="form-label">Detail (Complete Description) *</label>
                        <textarea class="form-control" id="detail" name="detail" 
                                  rows="6" required
                                  placeholder="Include: What needs to be done, Why, Scope of work, WO numbers, Equipment specs, Regulatory requirements"></textarea>
                        <small class="form-text text-muted">
                            Provide comprehensive details including what needs to be done, why, scope, WO numbers, equipment specs, and any regulatory requirements.
                        </small>
                    </div>
                    
                    <!-- References -->
                    <div class="mb-3">
                        <label for="references" class="form-label">References/Supporting Documents</label>
                        <textarea class="form-control" id="references" name="references" 
                                  rows="3"
                                  placeholder="Work Order numbers, Previous SOWs, Drawing numbers (optional)"></textarea>
                    </div>
                    
                    <hr class="my-4">
                    
                    <!-- Photos Section -->
                    <h5 class="mb-3">Photos (Minimum {{ min_photos }}, Maximum {{ max_photos }}) *</h5>
                    
                    <div id="photoContainer">
                        <!-- Photo inputs will be added dynamically -->
                    </div>
                    
                    <button type="button" class="btn btn-secondary mb-3" id="addPhotoBtn">
                        + Add Photo
                    </button>
                    
                    <hr class="my-4">
                    
                    <!-- Submit Button -->
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary btn-lg">
                            Submit Work Item
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
let photoCount = 0;
const minPhotos = {{ min_photos }};
const maxPhotos = {{ max_photos }};

function addPhotoInput() {
    if (photoCount >= maxPhotos) {
        alert(`Maximum ${maxPhotos} photos allowed`);
        return;
    }
    
    photoCount++;
    const photoDiv = document.createElement('div');
    photoDiv.className = 'card mb-3 photo-input';
    photoDiv.id = `photo-${photoCount}`;
    photoDiv.innerHTML = `
        <div class="card-body">
            <div class="row">
                <div class="col-md-6 mb-2">
                    <label class="form-label">Photo ${photoCount} *</label>
                    <input type="file" class="form-control" name="photos" 
                           accept="image/jpeg,image/jpg,image/png" required>
                </div>
                <div class="col-md-6 mb-2">
                    <label class="form-label">Photo ${photoCount} Caption *</label>
                    <input type="text" class="form-control" name="photo_captions" 
                           placeholder="Describe what this photo shows" required>
                </div>
            </div>
            ${photoCount > minPhotos ? `
                <button type="button" class="btn btn-sm btn-danger" onclick="removePhoto(${photoCount})">
                    Remove Photo ${photoCount}
                </button>
            ` : ''}
        </div>
    `;
    
    document.getElementById('photoContainer').appendChild(photoDiv);
    updateAddPhotoButton();
}

function removePhoto(num) {
    const photoDiv = document.getElementById(`photo-${num}`);
    if (photoDiv) {
        photoDiv.remove();
        photoCount--;
        updateAddPhotoButton();
    }
}

function updateAddPhotoButton() {
    const btn = document.getElementById('addPhotoBtn');
    if (photoCount >= maxPhotos) {
        btn.disabled = true;
        btn.textContent = `Maximum ${maxPhotos} photos reached`;
    } else {
        btn.disabled = false;
        btn.textContent = '+ Add Photo';
    }
}

// Initialize with minimum photos
for (let i = 0; i < minPhotos; i++) {
    addPhotoInput();
}

// Form validation
document.getElementById('workItemForm').addEventListener('submit', function(e) {
    const photoInputs = document.querySelectorAll('input[type="file"][name="photos"]');
    const validPhotos = Array.from(photoInputs).filter(input => input.files.length > 0);
    
    if (validPhotos.length < minPhotos) {
        e.preventDefault();
        alert(`Please upload at least ${minPhotos} photos`);
        return false;
    }
    
    // Check all photos have captions
    const captions = document.querySelectorAll('input[name="photo_captions"]');
    for (let caption of captions) {
        if (!caption.value.trim()) {
            e.preventDefault();
            alert('All photos must have captions');
            return false;
        }
    }
});
</script>
{% endblock %}
```

#### `app/templates/crew_success.html`
```html
{% extends "base.html" %}

{% block title %}Submission Successful{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow text-center">
            <div class="card-body py-5">
                <div class="mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" fill="green" class="bi bi-check-circle" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                        <path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/>
                    </svg>
                </div>
                
                <h2 class="text-success mb-3">Submission Successful!</h2>
                <p class="lead">Work Item <strong>{{ item_number }}</strong> has been submitted.</p>
                <p class="text-muted">The Chief Engineer will review your submission.</p>
                
                <div class="mt-4">
                    <a href="{{ url_for('crew.submit_form') }}" class="btn btn-primary">
                        Submit Another Item
                    </a>
                    <a href="{{ url_for('auth.logout') }}" class="btn btn-outline-secondary">
                        Logout
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

#### `app/templates/admin_dashboard.html`
```html
{% extends "base.html" %}

{% block title %}Admin Dashboard{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Work Item Dashboard</h2>
    <span class="badge bg-secondary">{{ work_items|length }} Total Items</span>
</div>

<!-- Filters -->
<div class="card mb-4">
    <div class="card-body">
        <form method="GET" class="row g-3">
            <div class="col-md-4">
                <label class="form-label">Status Filter</label>
                <select class="form-select" name="status" onchange="this.form.submit()">
                    <option value="all" {% if status_filter == 'all' %}selected{% endif %}>All Statuses</option>
                    <option value="Submitted" {% if status_filter == 'Submitted' %}selected{% endif %}>Submitted</option>
                    <option value="Reviewed" {% if status_filter == 'Reviewed' %}selected{% endif %}>Reviewed</option>
                    <option value="Sent to PE" {% if status_filter == 'Sent to PE' %}selected{% endif %}>Sent to PE</option>
                </select>
            </div>
            <div class="col-md-4">
                <label class="form-label">Sort By</label>
                <select class="form-select" name="sort" onchange="this.form.submit()">
                    <option value="date_desc" {% if sort_by == 'date_desc' %}selected{% endif %}>Newest First</option>
                    <option value="date_asc" {% if sort_by == 'date_asc' %}selected{% endif %}>Oldest First</option>
                    <option value="item_number" {% if sort_by == 'item_number' %}selected{% endif %}>Item Number</option>
                    <option value="submitter" {% if sort_by == 'submitter' %}selected{% endif %}>Submitter</option>
                </select>
            </div>
        </form>
    </div>
</div>

<!-- Batch Actions -->
<div class="card mb-4">
    <div class="card-body">
        <form method="POST" action="{{ url_for('admin.download_batch') }}" id="batchForm">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <input type="checkbox" id="selectAll" class="form-check-input me-2">
                    <label for="selectAll">Select All</label>
                    <span class="badge bg-info ms-2" id="selectedCount">0 selected</span>
                </div>
                <button type="submit" class="btn btn-success" id="downloadBatchBtn" disabled>
                    Download Selected (.zip)
                </button>
            </div>
        </form>
    </div>
</div>

<!-- Work Items Table -->
<div class="table-responsive">
    <table class="table table-hover">
        <thead class="table-light">
            <tr>
                <th width="40">
                    <input type="checkbox" id="selectAllTable" class="form-check-input">
                </th>
                <th>Item No.</th>
                <th>Description</th>
                <th>Location</th>
                <th>Submitter</th>
                <th>Date</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for item in work_items %}
            <tr>
                <td>
                    <input type="checkbox" class="form-check-input item-checkbox" 
                           value="{{ item.id }}" form="batchForm" name="item_ids[]">
                </td>
                <td><strong>{{ item.item_number }}</strong></td>
                <td>{{ item.description[:50] }}{% if item.description|length > 50 %}...{% endif %}</td>
                <td>{{ item.location }}</td>
                <td>{{ item.submitter_name }}</td>
                <td><small>{{ format_datetime(item.submitted_at) }}</small></td>
                <td>
                    <span class="badge 
                        {% if item.status == 'Submitted' %}bg-primary
                        {% elif item.status == 'Reviewed' %}bg-warning
                        {% else %}bg-success{% endif %}">
                        {{ item.status }}
                    </span>
                </td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <a href="{{ url_for('admin.view_item', item_id=item.id) }}" 
                           class="btn btn-outline-primary" title="View Details">
                            View
                        </a>
                        <a href="{{ url_for('admin.download_single', item_id=item.id) }}" 
                           class="btn btn-outline-success" title="Download .docx">
                            Download
                        </a>
                    </div>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="8" class="text-center text-muted py-4">
                    No work items found
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}

{% block extra_js %}
<script>
// Batch selection logic
const checkboxes = document.querySelectorAll('.item-checkbox');
const selectAll = document.getElementById('selectAllTable');
const selectedCount = document.getElementById('selectedCount');
const downloadBtn = document.getElementById('downloadBatchBtn');

function updateSelectedCount() {
    const checked = document.querySelectorAll('.item-checkbox:checked').length;
    selectedCount.textContent = `${checked} selected`;
    downloadBtn.disabled = checked === 0;
}

selectAll.addEventListener('change', function() {
    checkboxes.forEach(cb => cb.checked = this.checked);
    updateSelectedCount();
});

checkboxes.forEach(cb => {
    cb.addEventListener('change', updateSelectedCount);
});

updateSelectedCount();
</script>
{% endblock %}
```

---

### Phase 9: CSS & Run Script (15 min)

#### `app/static/css/style.css`
```css
/* Mobile-first responsive design */
body {
    font-family: 'Calibri', 'Segoe UI', Tahoma, sans-serif;
    background-color: #f8f9fa;
}

.card {
    border: none;
    border-radius: 8px;
}

.card-header {
    border-radius: 8px 8px 0 0 !important;
}

/* Large touch-friendly buttons for mobile */
@media (max-width: 768px) {
    .btn-lg {
        padding: 1rem;
        font-size: 1.1rem;
    }
    
    .form-control-lg, .form-select-lg {
        padding: 0.75rem;
        font-size: 1.1rem;
    }
}

/* Photo input styling */
.photo-input {
    background-color: #f8f9fa;
    border-left: 4px solid #0d6efd;
}

/* Status badges */
.badge {
    padding: 0.5em 0.75em;
    font-weight: 500;
}

/* Table improvements for mobile */
@media (max-width: 768px) {
    .table-responsive {
        font-size: 0.9rem;
    }
    
    .btn-group-sm .btn {
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
    }
}

/* Loading spinner */
.spinner-border-sm {
    width: 1rem;
    height: 1rem;
}
```

#### Create `run.py`
```python
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5000)
```

#### Create `.env.example`
```env
# Application
SECRET_KEY=change-this-to-random-secret-key-in-production
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///maintenance.db

# Authentication
CREW_PASSWORD=crew2026
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin2026

# Deployment (Railway/Render)
PORT=5000
```

#### Create `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
venv/
env/

# Flask
instance/
.webassets-cache

# Database
*.db
*.sqlite

# Uploads
uploads/
generated_docs/
app/static/uploads/

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## 🚀 Running the Application

### 1. Initial Setup
```bash
cd ship-maintenance-tracker
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

### 2. Run Locally
```bash
python run.py
```

Visit: `http://localhost:5000`

### 3. Test Credentials
- **Crew Login:**
  - Password: `crew2026`
  - Select any crew name from dropdown

- **Admin Login:**
  - Username: `admin`
  - Password: `admin2026`

---

## 🌐 Deployment to Railway

### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

### 2. Initialize Railway Project
```bash
railway login
railway init
```

### 3. Add Environment Variables in Railway Dashboard
- `SECRET_KEY` - Generate random key
- `CREW_PASSWORD` - Set secure password
- `ADMIN_USERNAME` - Set admin username
- `ADMIN_PASSWORD` - Set admin password

### 4. Deploy
```bash
railway up
```

### 5. Create Procfile
```
web: gunicorn run:app
```

Add to requirements.txt:
```
gunicorn==21.2.0
```

---

## 🐛 Troubleshooting

### Photos not uploading?
- Check folder permissions: `chmod 755 uploads/`
- Verify max file size in config

### Database errors?
- Delete `maintenance.db` and restart app
- Check SQLAlchemy URI in config

### .docx generation fails?
- Ensure python-docx is installed: `pip install python-docx`
- Check photo file paths

---

## ✅ Testing Checklist

- [ ] Crew can login with password
- [ ] Crew can select name from dropdown
- [ ] Form validates minimum 2 photos
- [ ] Photo captions are required
- [ ] Photos are resized to 4" width
- [ ] .docx file matches template format
- [ ] Admin can view all submissions
- [ ] Admin can update status
- [ ] Admin can download single .docx
- [ ] Admin can batch download as .zip
- [ ] Works on iPhone Safari
- [ ] Works on Android Chrome

---

## 📚 Next Steps

1. **Test thoroughly** on mobile devices
2. **Customize crew list** in config.py
3. **Set secure passwords** in production
4. **Deploy to Railway** or Render
5. **Share URL** with crew

---

## 🎨 Optional Enhancements

- Add email notifications (using Flask-Mail)
- Allow admin to edit submissions
- Add search functionality
- Export to CSV for tracking
- Add photo gallery view
- Mobile app wrapper (using Capacitor)

---

## 🆘 Need Help?

Common issues and solutions:

1. **Import errors**: Run `pip install -r requirements.txt`
2. **Database not found**: Run `python run.py` to create it
3. **Photos too large**: Adjust `PHOTO_MAX_WIDTH` in config
4. **Port in use**: Change port in `run.py`

---

**Good luck with your build! 🚢⚓**
