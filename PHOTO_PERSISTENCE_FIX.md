# Photo Persistence Fix - Completed

## Problem
Photos were disappearing after Railway container restarts, showing as broken icons. This happened because `UPLOAD_FOLDER` was pointing to ephemeral storage (`/app/uploads`) instead of the persistent volume (`/app/data`).

## Solution Implemented

### 1. Configuration Update
**File:** `config.py` (Line 36)

Changed:
```python
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(BASE_DIR, 'uploads')
```

To:
```python
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(DATA_DIR, 'uploads')
```

**Result:** Photos now save to `data/uploads/` which is on the persistent volume.

### 2. Documentation Updated
**File:** `DEPLOYMENT.md`

- Added prominent warnings about ephemeral filesystem
- Clarified volume mount requirements
- Added troubleshooting section for photo persistence
- Updated deployment checklist with photo persistence testing

### 3. Local Migration
Migrated existing photo from old location to new:
- `d2a724d2d1624006894f977b923a5ed4.jpg` → Copied to `data/uploads/`

## Testing Required

### Local Testing
1. **Restart server** to verify config change:
   ```bash
   # Server should auto-restart due to file change
   # Or manually: Ctrl+C and run again
   ```

2. **Upload a test photo:**
   - Go to http://localhost:5001/crew-login
   - Login and create a new work item with photo
   - Check that photo saves to `data/uploads/` (not `uploads/`)

3. **Test persistence:**
   - Verify photo displays correctly
   - Restart Flask server
   - Reload page and verify photo still displays

### Railway Deployment Steps

1. **Verify Railway volume exists:**
   - Go to Railway dashboard → Your service → Settings → Volumes
   - Confirm volume is mounted at `/app/data`
   - If not, add volume mounted at `/app/data`

2. **Deploy the fix:**
   ```bash
   git add config.py DEPLOYMENT.md PHOTO_PERSISTENCE_FIX.md
   git commit -m "fix: photos now persist to mounted volume (data/uploads)"
   git push origin main
   ```

3. **Test on Railway:**
   - Wait for deployment to complete
   - Upload a test photo to a work item
   - **Trigger a restart:** Railway dashboard → Deployments → Restart
   - Verify photo still displays (not a broken icon)

## What This Fixes

✅ Photos now persist across Railway restarts/deployments
✅ Photos save to mounted volume (`/app/data/uploads/`)
✅ Database and uploaded files both use persistent storage
✅ No more broken image icons after restarts

## Important Notes

### For Railway Production
- **Any photos uploaded BEFORE this fix are lost** (unless they happened to be uploaded to the old `/data/uploads` location)
- Users may need to re-upload photos for older work items
- Once this fix is deployed, all NEW photos will persist correctly

### For Development
- Your local environment now uses `data/uploads/` directory
- Old `uploads/` directory can be deleted after confirming everything works
- The fix is backward compatible - no database changes needed

## Verification Checklist

Local Testing:
- [ ] Config change verified (`UPLOAD_FOLDER` ends with `data/uploads`)
- [ ] Upload test photo - saves to `data/uploads/`
- [ ] Photo displays correctly
- [ ] Restart server - photo still displays

Railway Deployment:
- [ ] Volume exists at `/app/data`
- [ ] Code deployed to Railway
- [ ] Upload test photo on Railway
- [ ] Trigger restart
- [ ] Photo still displays after restart ✓ PERSISTENCE VERIFIED

## Files Changed
- `config.py` - UPLOAD_FOLDER now uses DATA_DIR
- `DEPLOYMENT.md` - Enhanced documentation and warnings
- `PHOTO_PERSISTENCE_FIX.md` - This file

## Next Steps
1. Test locally (see "Testing Required" above)
2. Commit and push changes
3. Verify Railway volume configuration
4. Test photo persistence on Railway
5. Inform users that old photos need re-upload

