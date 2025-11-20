# Cloudinary Storage Migration

## Overview

This migration adds cloud-based file storage using Cloudinary to solve Railway's ephemeral filesystem limitations. Photos are now stored in Cloudinary instead of the local filesystem, ensuring they persist across deployments.

## Changes Made

### 1. Dependencies
- Added `cloudinary==1.41.0` to `requirements.txt`

### 2. Configuration (`config.py`)
Added Cloudinary configuration with environment variable support:
```python
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
USE_CLOUDINARY = bool(CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET)
```

### 3. Database Schema
Added two new fields to the `Photo` model:
- `cloudinary_public_id` (VARCHAR 300) - Stores the Cloudinary public ID
- `cloudinary_url` (VARCHAR 500) - Caches the Cloudinary URL

### 4. New Utilities (`app/cloudinary_utils.py`)
Created comprehensive Cloudinary utility functions:
- `configure_cloudinary()` - Initialize Cloudinary with credentials
- `process_image()` - Process images (resize, convert HEIC to JPEG)
- `upload_image_to_cloudinary()` - Upload and process images
- `delete_image_from_cloudinary()` - Delete images from Cloudinary
- `get_cloudinary_url()` - Generate Cloudinary URLs
- `download_image_from_cloudinary()` - Download images for DOCX generation
- `is_cloudinary_enabled()` - Check if Cloudinary is configured

### 5. Updated Routes
Modified photo upload and deletion logic in:
- `app/crew.py` - Crew photo uploads and deletions
- `app/admin.py` - Admin photo management

Both routes now support:
- Cloudinary storage when credentials are configured
- Fallback to local storage when Cloudinary is not configured
- Backward compatibility with existing local photos

### 6. Template Updates
Updated all photo display templates to use `photo.get_url()` method:
- `app/templates/admin_dashboard.html`
- `app/templates/admin_view_item.html`
- `app/templates/crew_view.html`
- `app/templates/crew_edit.html`

### 7. DOCX Generation
Updated `app/docx_generator.py` to handle both Cloudinary and local photos:
- Downloads Cloudinary photos to temporary files
- Embeds them in generated DOCX documents
- Cleans up temporary files after use

## Setup Instructions

### 1. Run Database Migration

Before deploying, run the migration script to add the new database fields:

```bash
python migrate_add_cloudinary_fields.py
```

This will add `cloudinary_public_id` and `cloudinary_url` columns to the `photos` table.

### 2. Configure Cloudinary Credentials

#### Option A: Railway Environment Variables
Set these environment variables in your Railway project:

```
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here
```

#### Option B: Local Development (.env file)
Add to your `.env` file:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here
```

### 3. Get Cloudinary Credentials

1. Sign up for a free Cloudinary account at https://cloudinary.com/
2. Navigate to the Dashboard
3. Copy your credentials:
   - Cloud Name
   - API Key
   - API Secret

Free tier includes:
- 25 GB storage
- 25 GB monthly bandwidth
- Perfect for this application's needs

### 4. Deploy

After setting environment variables:
1. Push code to Railway
2. Railway will automatically redeploy
3. New photos will be stored in Cloudinary
4. Existing local photos remain accessible (backward compatible)

## How It Works

### Photo Upload Flow
1. User uploads a photo via the web interface
2. Backend checks if Cloudinary is configured (`USE_CLOUDINARY`)
3. If Cloudinary is enabled:
   - Image is processed (resized, HEIC → JPEG conversion)
   - Uploaded to Cloudinary folder `work_items/`
   - Database stores `cloudinary_public_id` and `cloudinary_url`
4. If Cloudinary is NOT enabled:
   - Falls back to local filesystem storage
   - Maintains backward compatibility

### Photo Retrieval Flow
1. Templates call `photo.get_url()` method
2. Method returns:
   - `cloudinary_url` if photo is in Cloudinary
   - Local URL via `url_for('serve_upload', filename=...)` if local
3. Browser loads image from appropriate source

### DOCX Generation Flow
1. When generating DOCX documents:
   - Cloudinary photos are downloaded to temporary files
   - Embedded in the document
   - Temporary files are cleaned up
2. Local photos are used directly from filesystem

## Testing

### Test Cloudinary Upload
1. Set Cloudinary environment variables
2. Restart the application
3. Submit a new work item with photos
4. Verify in Cloudinary dashboard that photos appear in `work_items/` folder
5. Check database that `cloudinary_public_id` and `cloudinary_url` are populated

### Test Backward Compatibility
1. Ensure existing work items with local photos still display correctly
2. Generate DOCX for old items - photos should embed properly
3. Test photo deletion for both Cloudinary and local photos

### Test Fallback Mode
1. Remove Cloudinary environment variables
2. Restart application
3. Upload new photos - should save to local filesystem
4. Verify photos display and DOCX generation works

## Rollback Plan

If issues arise, you can rollback:

1. Remove Cloudinary environment variables
2. Application automatically falls back to local storage
3. Existing photos (both Cloudinary and local) remain accessible

To fully remove Cloudinary:
1. Revert the code changes
2. Optionally remove the new database columns (not required for functionality)

## Benefits

✅ **Persistence**: Photos survive Railway redeployments
✅ **Scalability**: Cloudinary CDN for fast global delivery
✅ **Automatic Optimization**: Cloudinary optimizes images automatically
✅ **Backward Compatible**: Existing local photos continue to work
✅ **Fallback Support**: Works without Cloudinary if needed
✅ **Cost Effective**: Free tier sufficient for typical usage

## Monitoring

### Check Cloudinary Usage
1. Log into Cloudinary dashboard
2. View Storage & Bandwidth usage
3. Monitor the `work_items/` folder

### Verify Photo Storage
Check database to see storage distribution:
```sql
SELECT
  COUNT(*) as total_photos,
  COUNT(cloudinary_public_id) as cloudinary_photos,
  COUNT(*) - COUNT(cloudinary_public_id) as local_photos
FROM photos;
```

## Troubleshooting

### Photos Not Uploading
- Check Cloudinary credentials are set correctly
- Verify environment variables are loaded (check Railway logs)
- Check Cloudinary dashboard for API errors

### DOCX Generation Fails
- Ensure network connectivity to Cloudinary
- Check temporary file permissions
- Verify Cloudinary URLs are accessible

### Old Photos Not Displaying
- Verify backward compatibility is maintained
- Check local `uploads/` folder exists for development
- Ensure `photo.get_url()` method is used in templates

## Future Enhancements

Potential improvements:
- Migrate existing local photos to Cloudinary
- Implement image transformations (thumbnails, watermarks)
- Add video support
- Implement automatic backup to Cloudinary
