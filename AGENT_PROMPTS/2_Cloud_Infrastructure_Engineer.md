# Agent 2: Cloud Infrastructure Engineer

## Branch Information
**Branch Name:** `claude/cloudinary-file-storage`
**Estimated Time:** 3-5 hours
**Priority:** CRITICAL

## Role & Responsibilities
You are the Cloud Infrastructure Engineer responsible for migrating the application's file storage from the local filesystem to cloud storage (Cloudinary). This is CRITICAL because Railway uses ephemeral filesystems, meaning all uploaded photos and generated documents are **lost on application restart**.

## Mission Objective
Migrate photo uploads and generated documents from local filesystem to Cloudinary, ensuring persistent storage across application restarts and enabling horizontal scaling.

## Current Problem

**Railway Ephemeral Filesystem Issue:**
- Photos saved to `/uploads` folder - LOST on restart
- Generated docs saved to `/generated_docs` folder - LOST on restart
- This is a **production blocker** - users lose all uploaded photos on deployment

**Current Implementation:**
- `app/utils.py` - Saves photos to local disk
- `app/crew.py` - Handles photo upload to local disk
- `app/admin.py` - Serves photos from local disk
- `app/docx_generator.py` - Reads photos from local disk

## Step-by-Step Tasks

### Phase 1: Cloudinary Setup (30 minutes)

1. **Sign up for Cloudinary account:**
   - Go to https://cloudinary.com/users/register/free
   - Free tier: 25GB storage, 25GB bandwidth/month (sufficient for this project)
   - Note your credentials: Cloud Name, API Key, API Secret

2. **Install Cloudinary SDK:**
   ```bash
   pip install cloudinary
   ```

3. **Update `requirements.txt`:**
   ```
   cloudinary==1.36.0
   ```

4. **Add environment variables to config:**
   In `config.py`, add:
   ```python
   # Cloudinary Configuration
   CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
   CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
   CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

   # Feature flag for cloud storage (allows gradual rollout)
   USE_CLOUD_STORAGE = os.environ.get('USE_CLOUD_STORAGE', 'False').lower() == 'true'
   ```

5. **Set environment variables locally (.env file):**
   ```
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   USE_CLOUD_STORAGE=True
   ```

### Phase 2: Create Cloud Storage Module (1-2 hours)

1. **Create `app/cloud_storage.py`:**

This module should provide an abstraction layer for cloud storage operations.

**Required Functions:**
```python
def init_cloudinary():
    """Initialize Cloudinary configuration."""
    pass

def upload_photo(file_obj, filename: str) -> dict:
    """
    Upload photo to Cloudinary.

    Args:
        file_obj: File object or file path
        filename: Original filename

    Returns:
        dict: {
            'public_id': str,  # Cloudinary public ID
            'secure_url': str,  # HTTPS URL
            'format': str,      # Image format
            'width': int,
            'height': int,
            'bytes': int
        }
    """
    pass

def delete_photo(public_id: str) -> bool:
    """Delete photo from Cloudinary by public ID."""
    pass

def get_photo_url(public_id: str, transformations: dict = None) -> str:
    """
    Get photo URL with optional transformations.

    Args:
        public_id: Cloudinary public ID
        transformations: Optional dict like {'width': 300, 'crop': 'fill'}

    Returns:
        str: HTTPS URL to photo
    """
    pass

def upload_document(file_path: str, filename: str) -> dict:
    """Upload generated DOCX document to Cloudinary."""
    pass

def get_document_url(public_id: str) -> str:
    """Get download URL for a document."""
    pass
```

**Implementation Tips:**
- Use `cloudinary.uploader.upload()` for uploads
- Store photos in folder: `ship-maintenance/photos/`
- Store documents in folder: `ship-maintenance/documents/`
- Use `public_id` format: `photos/{item_number}_{uuid}`
- Enable automatic format optimization
- Set quality to 'auto' for automatic compression

### Phase 3: Update Utilities (1 hour)

1. **Modify `app/utils.py`:**

Update the `resize_image()` function to:
- Accept file object instead of file path (optional)
- Return cloudinary URL instead of local path when cloud storage enabled
- Handle HEIC conversion before upload
- Maintain backward compatibility with local storage

```python
def resize_image(file_obj, max_width: int = 576, use_cloud: bool = None) -> tuple:
    """
    Resize image and optionally upload to cloud storage.

    Returns:
        tuple: (width, height, url_or_path, public_id_or_none)
    """
    # Implementation here
```

2. **Create storage abstraction:**

Add a function to handle both local and cloud storage transparently:
```python
def save_photo(file_obj, filename: str) -> dict:
    """
    Save photo using configured storage backend.

    Returns:
        dict: {
            'filename': str,     # Filename or public_id
            'url': str,          # Full URL
            'width': int,
            'height': int,
            'storage_type': str  # 'local' or 'cloudinary'
        }
    """
    if current_app.config['USE_CLOUD_STORAGE']:
        return save_to_cloudinary(file_obj, filename)
    else:
        return save_to_local(file_obj, filename)
```

### Phase 4: Update Photo Upload Logic (1-2 hours)

1. **Modify `app/crew.py` - `submit_form()` route:**

Update photo upload logic (around line 94-115):
```python
# OLD:
photo_file.save(filepath)
_, _, final_path = resize_image(filepath, ...)
final_filename = os.path.basename(final_path)

# NEW:
photo_result = save_photo(photo_file, filename)
photo = Photo(
    filename=photo_result['public_id'] if USE_CLOUD_STORAGE else photo_result['filename'],
    caption=caption or '',
    work_item_id=work_item.id,
    cloud_url=photo_result.get('url'),  # Add this field to model
    storage_type=photo_result['storage_type']
)
```

2. **Update Photo model in `app/models.py`:**

Add new fields:
```python
class Photo(db.Model):
    # ... existing fields ...
    cloud_url = db.Column(db.String(500))  # Cloudinary URL
    storage_type = db.Column(db.String(20), default='local')  # 'local' or 'cloudinary'
    public_id = db.Column(db.String(200))  # Cloudinary public_id
```

3. **Create database migration:**

Create `migrate_add_cloud_fields.py`:
```python
"""Add cloud storage fields to Photo model."""
from app import db
from app.models import Photo

# Add columns to existing Photo table
db.session.execute('ALTER TABLE photos ADD COLUMN cloud_url VARCHAR(500)')
db.session.execute('ALTER TABLE photos ADD COLUMN storage_type VARCHAR(20) DEFAULT "local"')
db.session.execute('ALTER TABLE photos ADD COLUMN public_id VARCHAR(200)')
db.session.commit()
```

### Phase 5: Update Photo Serving Routes (1 hour)

1. **Modify `app/admin.py` - `serve_upload()` route:**

Update to serve from cloud or local:
```python
@bp.route('/uploads/<filename>')
@admin_required
def serve_upload(filename):
    """Serve uploaded photos from cloud or local storage."""
    # Try to find photo in database
    photo = Photo.query.filter_by(filename=filename).first()

    if photo and photo.storage_type == 'cloudinary':
        # Redirect to Cloudinary URL
        return redirect(photo.cloud_url)
    else:
        # Serve from local filesystem
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
```

2. **Update `download_photo()` route:**

Similar logic to serve from cloud or local.

3. **Update `delete_photo()` route:**

Delete from cloud storage:
```python
if photo.storage_type == 'cloudinary':
    from app.cloud_storage import delete_photo
    delete_photo(photo.public_id)
else:
    # Delete from local filesystem
    os.remove(photo_path)
```

### Phase 6: Update Document Generation (1 hour)

1. **Modify `app/docx_generator.py`:**

Update photo retrieval to work with cloud URLs:
```python
def generate_docx(work_item):
    # ...
    for photo in work_item.photos:
        if photo.storage_type == 'cloudinary':
            # Download photo from Cloudinary URL
            import requests
            response = requests.get(photo.cloud_url)
            img_bytes = BytesIO(response.content)
            # Add to document
            doc.add_picture(img_bytes, width=Inches(4))
        else:
            # Use local file path
            photo_path = os.path.join(UPLOAD_FOLDER, photo.filename)
            doc.add_picture(photo_path, width=Inches(4))
```

2. **Optional: Upload generated documents to cloud:**

Store generated DOCX files in Cloudinary instead of local filesystem:
```python
# After generating document
if USE_CLOUD_STORAGE:
    doc_result = upload_document(doc_path, filename)
    # Return cloud URL instead of local file
```

### Phase 7: Templates Update (30 minutes)

1. **Update `app/templates/admin_view_item.html`:**

Photo URLs should work with both cloud and local:
```html
<!-- OLD: -->
<img src="{{ url_for('admin.serve_upload', filename=photo.filename) }}">

<!-- NEW (works with both): -->
{% if photo.storage_type == 'cloudinary' %}
    <img src="{{ photo.cloud_url }}">
{% else %}
    <img src="{{ url_for('admin.serve_upload', filename=photo.filename) }}">
{% endif %}
```

2. **Update `app/templates/admin_dashboard.html`:**

Similar changes for photo thumbnails.

3. **Update `app/templates/crew_form.html`:**

No changes needed (upload form stays the same).

### Phase 8: Testing & Validation (1 hour)

1. **Test photo upload workflow:**
   - Submit new work item with photos
   - Verify photos uploaded to Cloudinary (check dashboard)
   - Verify photos display correctly in admin view
   - Test photo download
   - Test photo deletion

2. **Test document generation:**
   - Generate DOCX with cloud photos
   - Verify photos appear in document
   - Test batch download

3. **Test edge cases:**
   - Large photos (>10MB)
   - HEIC conversion with cloud storage
   - Network errors (Cloudinary unavailable)
   - Fallback to local storage if cloud fails

4. **Performance testing:**
   - Measure upload time vs local
   - Check photo loading speed
   - Verify no timeouts

## Files You MUST Modify/Create

### Create:
- `app/cloud_storage.py` - Cloud storage abstraction
- `migrate_add_cloud_fields.py` - Database migration script

### Modify:
- `app/utils.py` - Update photo handling
- `app/crew.py` - Update photo upload logic
- `app/admin.py` - Update photo serving routes
- `app/models.py` - Add cloud storage fields to Photo model
- `app/docx_generator.py` - Handle cloud photo URLs
- `config.py` - Add Cloudinary configuration
- `requirements.txt` - Add cloudinary package
- `app/templates/admin_view_item.html` - Update photo URLs
- `app/templates/admin_dashboard.html` - Update photo URLs
- `.env.example` - Document new environment variables

### DO NOT Modify:
- Authentication logic
- Database models (except Photo)
- Crew submission workflow (except photo handling)

## Quality Checklist

### Configuration:
- [ ] Cloudinary account created
- [ ] Environment variables configured
- [ ] SDK installed and imported

### Code Changes:
- [ ] `cloud_storage.py` module created
- [ ] Photo model updated with cloud fields
- [ ] Photo upload updated to use cloud storage
- [ ] Photo serving updated to use cloud URLs
- [ ] Photo deletion updated to delete from cloud
- [ ] Document generation updated to fetch cloud photos
- [ ] Templates updated to display cloud photos

### Testing:
- [ ] Photos upload to Cloudinary successfully
- [ ] Photos display correctly in admin view
- [ ] Photos download correctly
- [ ] Photo deletion removes from Cloudinary
- [ ] Document generation includes cloud photos
- [ ] HEIC conversion works with cloud storage
- [ ] Error handling works (cloud unavailable)

### Migration:
- [ ] Database migration script created
- [ ] Migration tested locally
- [ ] Migration instructions documented

### Documentation:
- [ ] Environment variables documented in .env.example
- [ ] README updated with Cloudinary setup instructions
- [ ] Migration guide created for existing photos (optional)

## Railway Deployment

After implementing, set environment variables in Railway:
```bash
railway variables set CLOUDINARY_CLOUD_NAME=your_cloud_name
railway variables set CLOUDINARY_API_KEY=your_api_key
railway variables set CLOUDINARY_API_SECRET=your_api_secret
railway variables set USE_CLOUD_STORAGE=True
```

## Success Criteria

- ✅ Photos upload to Cloudinary instead of local filesystem
- ✅ Photos persist across Railway restarts/deployments
- ✅ Photos display correctly in all views
- ✅ Photo deletion removes from Cloudinary
- ✅ Document generation works with cloud photos
- ✅ Backward compatibility with existing local photos
- ✅ No performance degradation
- ✅ Error handling for cloud failures

## Deliverables

1. Working `app/cloud_storage.py` module
2. Updated photo upload workflow
3. Updated photo serving routes
4. Updated templates
5. Database migration script
6. Documentation in README
7. All tests passing

## Resources

- [Cloudinary Python SDK](https://cloudinary.com/documentation/python_integration)
- [Cloudinary Image Transformations](https://cloudinary.com/documentation/image_transformations)
- [Flask File Uploads Best Practices](https://flask.palletsprojects.com/en/3.0.x/patterns/fileuploads/)

## Notes

- Cloudinary free tier: 25GB storage, 25GB bandwidth/month
- Photos automatically optimized (format, quality)
- Built-in CDN for fast delivery worldwide
- Automatic backups and versioning
- Consider adding transformations for thumbnails (width=300, crop=fill)

---

**Ready to start?** Begin with Phase 1 (Cloudinary setup) and work through systematically. This will solve the critical production blocker!
