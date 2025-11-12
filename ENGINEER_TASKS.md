# Engineer Tasks - Ship Maintenance Tracking Application

## Overview
This document provides a structured breakdown of tasks for junior engineers working on the Ship Maintenance Tracking Application. Tasks are organized by priority and complexity level.

**Legend:**
- 🟢 **Easy** - Can be completed in 1-4 hours, minimal complexity
- 🟡 **Medium** - Requires 4-8 hours, moderate complexity
- 🔴 **Hard** - Requires 8+ hours, high complexity or multiple systems

---

## Priority 1: Critical Features (Must Complete Before Production)

### Task 1.1: Implement SMS Notifications with Twilio 🔴
**Priority:** CRITICAL
**Estimated Time:** 8-12 hours
**Prerequisites:** Twilio account, phone numbers configured

**Description:**
Implement SMS notifications to alert crew members when work items are assigned to them. Currently, notification code is commented out in `app/admin.py:215-217`.

**Files to Modify:**
- `app/admin.py`
- `config.py`
- Create new file: `app/notifications.py`

**Requirements:**
1. Create `send_assignment_notification()` function in `app/notifications.py`
2. Integrate Twilio SMS API
3. Send SMS when work item is assigned (status changed to "Needs Revision" or "Awaiting Photos")
4. SMS should include:
   - Item number
   - Status
   - Revision notes (if present)
   - Link to login page
5. Handle errors gracefully (log failures, don't crash)
6. Add phone numbers for all 6 crew members in config
7. Test with all crew members

**Environment Variables Needed:**
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

**Crew Phone Numbers to Add:**
```python
CREW_PHONES = {
    'DP': os.environ.get('DP_PHONE'),
    'AL': os.environ.get('AL_PHONE'),
    'Kaitlyn': os.environ.get('KAITLYN_PHONE'),
    'Mark': os.environ.get('MARK_PHONE'),
    'Art': os.environ.get('ART_PHONE'),
    'D2': os.environ.get('D2_PHONE'),
}
```

**Testing Checklist:**
- [ ] SMS sent when item assigned to crew member
- [ ] SMS contains correct information
- [ ] All 6 crew members can receive SMS
- [ ] Error handling works (invalid phone number)
- [ ] SMS not sent when ENABLE_NOTIFICATIONS=False

**Reference:**
- Twilio Python SDK: https://www.twilio.com/docs/sms/quickstart/python
- See `app/admin.py:215` for commented TODO

---

### Task 1.2: Update Default Credentials 🟢
**Priority:** CRITICAL
**Estimated Time:** 30 minutes
**Security Risk:** HIGH

**Description:**
Change default passwords before production deployment. Current defaults are publicly visible in `config.py`.

**Files to Modify:**
- `config.py`

**Current Default Credentials (MUST CHANGE):**
```python
CREW_PASSWORD = 'crew350'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin350'
```

**Requirements:**
1. Read credentials from environment variables
2. Keep defaults only for local development
3. Force strong passwords in production
4. Update Railway environment variables

**Example Implementation:**
```python
CREW_PASSWORD = os.environ.get('CREW_PASSWORD', 'crew350')  # Change in production!
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin350')  # Change in production!
```

**Testing Checklist:**
- [ ] Set environment variables in Railway
- [ ] Test login with new credentials
- [ ] Verify old credentials no longer work
- [ ] Document new credentials securely (password manager)

---

### Task 1.3: Add SECRET_KEY Environment Variable 🟢
**Priority:** CRITICAL
**Estimated Time:** 30 minutes
**Security Risk:** HIGH

**Description:**
Move Flask SECRET_KEY to environment variable instead of hardcoded value.

**Files to Modify:**
- `config.py`
- Railway environment variables

**Current Code (line ~11):**
```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_change_in_production')
```

**Requirements:**
1. Generate strong random secret key for production
2. Set in Railway environment variables
3. Keep dev key for local development

**Generate Secret Key:**
```python
import secrets
print(secrets.token_hex(32))
```

**Testing Checklist:**
- [ ] SECRET_KEY set in Railway
- [ ] Sessions work correctly with new key
- [ ] Login/logout functionality works

---

### Task 1.4: Configure PostgreSQL for Production 🟡
**Priority:** CRITICAL
**Estimated Time:** 2-4 hours

**Description:**
Migrate from SQLite to PostgreSQL for Railway production deployment.

**Files to Modify:**
- `config.py` (already configured, just need to verify)
- `requirements.txt` (add psycopg2-binary)
- Railway database setup

**Current Code:**
```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///maintenance.db')
```

**Requirements:**
1. Add PostgreSQL dependency to requirements.txt
2. Create PostgreSQL database in Railway
3. Set DATABASE_URL environment variable
4. Verify tables auto-create on first run
5. Test database persistence

**Add to requirements.txt:**
```
psycopg2-binary==2.9.9
```

**Testing Checklist:**
- [ ] PostgreSQL provisioned in Railway
- [ ] DATABASE_URL environment variable set
- [ ] Tables created automatically (db.create_all())
- [ ] Create test work item in production
- [ ] Verify data persists after restart
- [ ] Upload photo and verify persistence

---

### Task 1.5: Implement File Storage for Production 🔴
**Priority:** CRITICAL
**Estimated Time:** 8-12 hours

**Description:**
Railway ephemeral filesystem means uploaded photos are lost on restart. Implement persistent storage using Railway volumes or cloud storage (S3, Cloudinary).

**Current Issue:**
- Photos saved to `/uploads` folder
- Generated docs saved to `/generated_docs` folder
- Both lost on Railway container restart

**Solution Options:**

**Option A: Railway Volumes (Recommended for simplicity)**
1. Create persistent volume in Railway
2. Mount to `/uploads` and `/generated_docs`
3. No code changes required

**Option B: AWS S3 / Cloudinary (Recommended for scalability)**
1. Sign up for cloud storage service
2. Install SDK (boto3 for S3, cloudinary for Cloudinary)
3. Modify file upload/retrieval logic
4. Store files in cloud instead of local filesystem

**Files to Modify (if using S3/Cloudinary):**
- `app/utils.py` - Update `save_photo()` and `resize_image()`
- `app/crew.py` - Update photo upload logic
- `app/admin.py` - Update `serve_upload()`, `download_photo()`
- `app/docx_generator.py` - Update photo retrieval
- `requirements.txt` - Add SDK

**Testing Checklist:**
- [ ] Upload photo in production
- [ ] Restart Railway app
- [ ] Verify photo still accessible after restart
- [ ] Test document generation with uploaded photos
- [ ] Test photo deletion (verify removed from storage)

**Resources:**
- Railway Volumes: https://docs.railway.app/reference/volumes
- AWS S3 Python SDK: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3.html
- Cloudinary: https://cloudinary.com/documentation/python_integration

---

## Priority 2: Important Features (Complete Before Full Launch)

### Task 2.1: Add Pagination to Admin Dashboard 🟡
**Priority:** HIGH
**Estimated Time:** 4-6 hours

**Description:**
With 100+ work items, the dashboard becomes slow. Add pagination to display 25 items per page.

**Files to Modify:**
- `app/admin.py` - Update `dashboard()` route
- `app/templates/admin_dashboard.html` - Add pagination UI

**Requirements:**
1. Show 25 items per page (configurable)
2. Add page navigation (Previous, 1, 2, 3... Next)
3. Maintain filters and sorting across pages
4. Show total item count
5. Highlight current page

**Implementation Tips:**
```python
# In app/admin.py
from flask import request

page = request.args.get('page', 1, type=int)
per_page = 25

work_items = WorkItem.query.paginate(page=page, per_page=per_page)
```

**Testing Checklist:**
- [ ] Create 50+ test work items
- [ ] Verify pagination displays correctly
- [ ] Test navigation between pages
- [ ] Verify filters work with pagination
- [ ] Verify sorting works with pagination
- [ ] Test edge cases (empty results, single page)

---

### Task 2.2: Add Search Functionality 🟡
**Priority:** HIGH
**Estimated Time:** 4-6 hours

**Description:**
Add search box to admin dashboard to filter work items by item number, location, description, or submitter.

**Files to Modify:**
- `app/admin.py` - Update `dashboard()` route
- `app/templates/admin_dashboard.html` - Add search input

**Requirements:**
1. Search box in dashboard header
2. Search across multiple fields:
   - Item number
   - Location
   - Description
   - Submitter name
3. Real-time search (optional: JavaScript live search)
4. Combine with existing filters
5. Highlight search terms in results (optional)

**Implementation Tips:**
```python
# In app/admin.py
search_term = request.args.get('search', '')

if search_term:
    query = query.filter(
        db.or_(
            WorkItem.item_number.ilike(f'%{search_term}%'),
            WorkItem.location.ilike(f'%{search_term}%'),
            WorkItem.description.ilike(f'%{search_term}%'),
            WorkItem.submitter_name.ilike(f'%{search_term}%')
        )
    )
```

**Testing Checklist:**
- [ ] Search by item number - returns correct results
- [ ] Search by location - returns correct results
- [ ] Search by description - returns correct results
- [ ] Search by submitter name - returns correct results
- [ ] Search with filters applied - works correctly
- [ ] Search with no results - shows appropriate message
- [ ] Clear search - returns to all items

---

### Task 2.3: Implement Status History Display 🟢
**Priority:** MEDIUM
**Estimated Time:** 2-3 hours

**Description:**
The StatusHistory model exists but isn't displayed in the UI. Add a timeline view showing all status changes.

**Files to Modify:**
- `app/templates/admin_view_item.html`

**Requirements:**
1. Display status history below work item details
2. Show timeline format:
   - Status change (old → new)
   - Changed by (user)
   - Date/time
   - Notes (if any)
3. Sort by most recent first
4. Format dates nicely

**UI Example:**
```
Status History:
─────────────────────────────────────
✓ Needs Revision → Submitted
  By: Mark | 2025-11-12 14:30
  Notes: Added 2 additional photos as requested

✓ In Review by DP → Needs Revision
  By: admin | 2025-11-11 09:15
  Notes: Please add 2 more photos showing damaged area

✓ Submitted → In Review by DP
  By: admin | 2025-11-10 16:00
```

**Testing Checklist:**
- [ ] Create work item and change status multiple times
- [ ] Verify all status changes appear in history
- [ ] Verify correct chronological order
- [ ] Verify notes display when present
- [ ] Verify formatting is readable

---

### Task 2.4: Add Comment System 🟡
**Priority:** MEDIUM
**Estimated Time:** 6-8 hours

**Description:**
The Comment model exists but isn't implemented. Add commenting functionality for admins and crew to communicate.

**Files to Modify:**
- `app/admin.py` - Add comment routes
- `app/crew.py` - Add crew comment functionality
- `app/templates/admin_view_item.html` - Add comment UI
- `app/templates/crew_form.html` - Add comment UI (optional)

**Requirements:**
1. Admins can add comments on work items
2. Crew can view comments on assigned items
3. Display comment author, timestamp, and text
4. Show admin comments differently (badge, icon)
5. Sort by newest first
6. Optional: Crew can reply to comments

**Implementation:**
```python
# In app/admin.py
@admin_bp.route('/comment/<int:item_id>', methods=['POST'])
@admin_required
def add_comment(item_id):
    work_item = WorkItem.query.get_or_404(item_id)
    comment_text = request.form.get('comment_text')

    comment = Comment(
        work_item_id=item_id,
        author_name=session.get('admin_username'),
        comment_text=comment_text,
        is_admin=True
    )
    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('admin.view_item', item_id=item_id))
```

**Testing Checklist:**
- [ ] Admin can add comment
- [ ] Comments display correctly
- [ ] Admin badge shows on admin comments
- [ ] Crew can view comments on assigned items
- [ ] Comments persist across page reloads
- [ ] Delete comment functionality works (optional)

---

### Task 2.5: Add Email Notifications (Alternative to SMS) 🟡
**Priority:** MEDIUM
**Estimated Time:** 4-6 hours

**Description:**
Implement email notifications as alternative/backup to SMS. Use SMTP configuration already in config.py.

**Files to Modify:**
- `app/notifications.py` (create if doesn't exist)
- `app/admin.py`
- `config.py`

**Requirements:**
1. Send email when work item assigned
2. Email includes:
   - Item number and description
   - Status
   - Revision notes
   - Link to login page
3. Use HTML email template
4. Handle SMTP errors gracefully
5. Support both Gmail and custom SMTP servers

**Email Template Example:**
```html
Subject: Work Item Assigned: {item_number}

Hello {crew_member},

You have been assigned a work item:

Item Number: {item_number}
Location: {location}
Status: {status}

Revision Notes:
{revision_notes}

Please log in to view and update this item:
{login_url}

- Arrowhead MTA 2026 System
```

**Testing Checklist:**
- [ ] Email sent when item assigned
- [ ] Email contains correct information
- [ ] HTML formatting displays correctly
- [ ] Test with Gmail SMTP
- [ ] Test with custom SMTP server
- [ ] Error handling works (invalid email)
- [ ] Emails not sent when ENABLE_NOTIFICATIONS=False

---

## Priority 3: Enhancements (Nice to Have)

### Task 3.1: Add Dark Mode Toggle 🟢
**Priority:** LOW
**Estimated Time:** 2-3 hours

**Description:**
Add dark mode option for users who prefer dark UI, especially useful on mobile at night.

**Files to Modify:**
- `app/static/css/style.css`
- `app/templates/base.html`

**Requirements:**
1. Toggle button in header
2. Persist preference in localStorage
3. Dark mode color scheme:
   - Background: #1a1a1a
   - Text: #e0e0e0
   - Cards: #2d2d2d
   - Borders: #404040
4. Smooth transition between modes

**Implementation Tips:**
```javascript
// In base.html or main.js
const darkModeToggle = document.getElementById('dark-mode-toggle');
darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
});

// Load preference on page load
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}
```

**Testing Checklist:**
- [ ] Toggle button switches modes correctly
- [ ] Preference persists across page reloads
- [ ] All pages support dark mode
- [ ] Text remains readable in dark mode
- [ ] Photos display correctly in dark mode

---

### Task 3.2: Add Export to Excel 🟡
**Priority:** LOW
**Estimated Time:** 4-6 hours

**Description:**
Add ability to export work items to Excel spreadsheet for reporting and analysis.

**Files to Modify:**
- `app/admin.py` - Add export route
- `requirements.txt` - Add openpyxl
- `app/templates/admin_dashboard.html` - Add export button

**Requirements:**
1. Export all work items to .xlsx file
2. Include columns:
   - Item Number
   - Location
   - NS Equipment
   - Description
   - Status
   - Assigned To
   - Submitted By
   - Submitted Date
   - Photo Count
3. Apply filters before export
4. Format as table with headers
5. Auto-size columns

**Add to requirements.txt:**
```
openpyxl==3.1.2
```

**Implementation Tips:**
```python
from openpyxl import Workbook
from flask import send_file

@admin_bp.route('/export-excel')
@admin_required
def export_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Work Items"

    # Headers
    headers = ['Item Number', 'Location', 'Description', ...]
    ws.append(headers)

    # Data
    work_items = WorkItem.query.all()
    for item in work_items:
        ws.append([item.item_number, item.location, ...])

    # Save and return
    filename = 'work_items_export.xlsx'
    wb.save(filename)
    return send_file(filename, as_attachment=True)
```

**Testing Checklist:**
- [ ] Export button generates .xlsx file
- [ ] File opens correctly in Excel/Google Sheets
- [ ] All columns present and correct
- [ ] Data matches dashboard display
- [ ] Filters apply to export
- [ ] Date formatting correct

---

### Task 3.3: Add Photo Gallery View 🟡
**Priority:** LOW
**Estimated Time:** 4-6 hours

**Description:**
Add modal gallery view for photos with lightbox effect, zoom, and navigation.

**Files to Modify:**
- `app/templates/admin_view_item.html`
- `app/static/css/style.css`
- `app/static/js/main.js`

**Requirements:**
1. Click photo to open in lightbox modal
2. Navigate between photos (prev/next arrows)
3. Zoom in/out functionality
4. Close with X button or ESC key
5. Display photo caption below image
6. Show photo number (e.g., "Photo 2 of 4")

**Implementation Options:**
- Use lightbox library (Lightbox2, PhotoSwipe)
- Or build custom with Bootstrap modal

**Testing Checklist:**
- [ ] Click photo opens lightbox
- [ ] Navigate between photos works
- [ ] Zoom in/out works
- [ ] Close button works
- [ ] ESC key closes lightbox
- [ ] Works on mobile (touch gestures)
- [ ] Captions display correctly

---

### Task 3.4: Add User Activity Log 🔴
**Priority:** LOW
**Estimated Time:** 8-10 hours

**Description:**
Track all user actions (create, edit, delete, assign, status change) in an audit log.

**Files to Create:**
- `app/models.py` - Add ActivityLog model
- `app/admin.py` - Add logging route

**Requirements:**
1. Log all significant actions:
   - Work item created/updated/deleted
   - Photo uploaded/deleted
   - Status changed
   - Item assigned
   - Document generated
   - User login/logout
2. Store:
   - User (crew or admin)
   - Action type
   - Target (work item ID)
   - Timestamp
   - IP address (optional)
3. Admin view to browse activity log
4. Filter by user, action type, date range

**ActivityLog Model:**
```python
class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'crew' or 'admin'
    action_type = db.Column(db.String(50), nullable=False)
    target_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
```

**Testing Checklist:**
- [ ] Actions logged correctly
- [ ] Activity log view displays all actions
- [ ] Filters work correctly
- [ ] Performance acceptable with 1000+ log entries
- [ ] Old logs can be archived/deleted

---

### Task 3.5: Add Mobile PWA Support 🔴
**Priority:** LOW
**Estimated Time:** 8-12 hours

**Description:**
Convert application to Progressive Web App (PWA) to allow installation on mobile devices and offline functionality.

**Files to Create:**
- `app/static/manifest.json` - PWA manifest
- `app/static/service-worker.js` - Service worker for offline
- `app/static/icons/` - Various icon sizes

**Requirements:**
1. Create web app manifest
2. Implement service worker for offline caching
3. Add "Add to Home Screen" prompt
4. Cache critical assets (CSS, JS, images)
5. Offline mode shows cached pages
6. Background sync for form submissions (optional)

**manifest.json Example:**
```json
{
  "name": "Ship Maintenance Tracker",
  "short_name": "MTA 2026",
  "description": "Arrowhead Maintenance Availability 2026",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0d6efd",
  "icons": [
    {
      "src": "/static/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

**Testing Checklist:**
- [ ] Manifest detected by browser
- [ ] Install prompt appears on mobile
- [ ] App installs on home screen
- [ ] Offline mode works (cached pages load)
- [ ] Service worker updates correctly
- [ ] Works on iPhone and Android

**Resources:**
- PWA Guide: https://web.dev/progressive-web-apps/
- Service Worker API: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API

---

## Priority 4: Bug Fixes & Improvements

### Task 4.1: Fix Photo Upload Feedback 🟢
**Priority:** MEDIUM
**Estimated Time:** 1-2 hours

**Description:**
Add visual feedback when uploading photos (loading spinner, progress bar, preview).

**Files to Modify:**
- `app/templates/crew_form.html`
- `app/static/css/style.css`
- `app/static/js/main.js`

**Requirements:**
1. Show loading spinner during upload
2. Display thumbnail preview after selection
3. Show file size validation errors
4. Disable submit button during upload

**Testing Checklist:**
- [ ] Loading spinner appears during upload
- [ ] Preview shows after file selection
- [ ] Error messages display correctly
- [ ] Submit button disabled during upload

---

### Task 4.2: Improve Error Messages 🟢
**Priority:** MEDIUM
**Estimated Time:** 2-3 hours

**Description:**
Replace generic error messages with specific, user-friendly messages.

**Files to Modify:**
- All route files (auth.py, crew.py, admin.py)
- All templates (add error display sections)

**Requirements:**
1. Specific validation errors for each field
2. User-friendly language (not technical)
3. Suggest corrections
4. Format errors nicely in UI

**Example Improvements:**
```
Bad:  "Invalid input"
Good: "Description must be between 10 and 500 characters"

Bad:  "File error"
Good: "Photo file size exceeds 16MB limit. Please compress the image and try again."

Bad:  "Not found"
Good: "Work item #DRAFT_0123 not found. It may have been deleted."
```

**Testing Checklist:**
- [ ] All validation errors have clear messages
- [ ] Errors display prominently in UI
- [ ] Errors are helpful and actionable
- [ ] No generic error messages remain

---

### Task 4.3: Add Loading States 🟢
**Priority:** LOW
**Estimated Time:** 2-3 hours

**Description:**
Add loading indicators for slow operations (document generation, batch download, large form submissions).

**Files to Modify:**
- All templates with forms/downloads
- `app/static/css/style.css`
- `app/static/js/main.js`

**Requirements:**
1. Spinner during document generation
2. Progress indicator for batch download
3. Loading overlay for form submission
4. Disable buttons during processing

**Testing Checklist:**
- [ ] Loading indicator shows during slow operations
- [ ] Buttons disabled during processing
- [ ] User cannot double-submit forms
- [ ] Loading state clears after completion

---

### Task 4.4: Optimize Image Processing 🟡
**Priority:** MEDIUM
**Estimated Time:** 4-6 hours

**Description:**
Improve image processing performance and quality. Currently uses basic Pillow resizing.

**Files to Modify:**
- `app/utils.py`

**Requirements:**
1. Use better resizing algorithm (LANCZOS)
2. Optimize JPEG quality (test different levels)
3. Add image compression
4. Process images asynchronously (optional: Celery)
5. Add progress feedback

**Current Code:**
```python
# app/utils.py:20-57
def resize_image(image_path):
    # ... current implementation
```

**Improvements:**
- Use `Image.LANCZOS` for better quality
- Adjust JPEG quality based on file size
- Consider WebP format for smaller file sizes
- Add error handling for corrupted images

**Testing Checklist:**
- [ ] Resized images maintain quality
- [ ] File sizes reduced appropriately
- [ ] Processing time acceptable (<5 seconds)
- [ ] HEIC conversion still works
- [ ] No memory issues with multiple uploads

---

## Task Templates

Use this template for new tasks:

```markdown
### Task X.X: [Task Title] [Difficulty Emoji]
**Priority:** [CRITICAL/HIGH/MEDIUM/LOW]
**Estimated Time:** [X-Y hours]

**Description:**
[Detailed description of what needs to be done and why]

**Files to Modify:**
- file1.py
- file2.html

**Requirements:**
1. Requirement 1
2. Requirement 2
3. Requirement 3

**Implementation Tips:**
[Code snippets, pseudocode, or approach suggestions]

**Testing Checklist:**
- [ ] Test case 1
- [ ] Test case 2
- [ ] Test case 3

**Resources:**
- [Link to documentation]
- [Link to tutorial]
```

---

## How to Use This Document

### For Junior Engineers:
1. **Start with Priority 1 tasks** - These are critical for production
2. **Read the entire task** before starting
3. **Ask questions** if requirements are unclear
4. **Test thoroughly** using the testing checklist
5. **Update this document** if you find issues or have suggestions
6. **Commit frequently** with clear messages
7. **Create pull requests** for review before merging

### For Senior Engineers / Project Leads:
1. **Assign tasks** based on engineer skill level
2. **Review pull requests** before merging
3. **Update priorities** as project needs change
4. **Add new tasks** using the template
5. **Provide code review** and mentorship

### General Workflow:
```
1. Pick a task from Priority 1 or 2
2. Create a new branch: git checkout -b feature/task-name
3. Read task requirements thoroughly
4. Implement the feature
5. Test using the testing checklist
6. Commit changes: git commit -m "feat: description"
7. Push branch: git push origin feature/task-name
8. Create pull request for review
9. Address review feedback
10. Merge after approval
11. Mark task as complete in this document
```

---

## Task Tracking

Use this table to track task completion:

| Task | Assigned To | Status | Started | Completed | Notes |
|------|-------------|--------|---------|-----------|-------|
| 1.1 SMS Notifications | | ⏳ Not Started | - | - | |
| 1.2 Default Credentials | | ⏳ Not Started | - | - | |
| 1.3 SECRET_KEY | | ⏳ Not Started | - | - | |
| 1.4 PostgreSQL | | ⏳ Not Started | - | - | |
| 1.5 File Storage | | ⏳ Not Started | - | - | |
| 2.1 Pagination | | ⏳ Not Started | - | - | |
| 2.2 Search | | ⏳ Not Started | - | - | |
| 2.3 Status History | | ⏳ Not Started | - | - | |
| 2.4 Comment System | | ⏳ Not Started | - | - | |
| 2.5 Email Notifications | | ⏳ Not Started | - | - | |

**Status Legend:**
- ⏳ Not Started
- 🏗️ In Progress
- 👀 In Review
- ✅ Completed
- ❌ Blocked

---

## Additional Resources

### Development Setup
- See README.md for local setup instructions
- See TESTING_CHECKLIST.md for comprehensive testing guide

### Code Style Guidelines
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic
- Keep functions small and focused

### Git Commit Messages
Follow conventional commits:
```
feat: Add SMS notification functionality
fix: Resolve photo upload error on mobile
docs: Update README with deployment instructions
style: Format code with black
refactor: Simplify image processing logic
test: Add tests for assignment workflow
```

### Helpful Commands
```bash
# Run application locally
python run.py

# Create database tables
python -c "from app import db; db.create_all()"

# Install dependencies
pip install -r requirements.txt

# Run tests (when added)
pytest

# Check code style
flake8 app/

# Format code
black app/
```

---

## Questions & Support

**Questions about a task?**
- Ask in team chat/Slack
- Review related code in codebase
- Check Flask documentation: https://flask.palletsprojects.com/

**Found a bug?**
- Document it in TESTING_CHECKLIST.md
- Create GitHub issue with reproduction steps
- Fix it if you can, or escalate to senior engineer

**Have suggestions?**
- Add new tasks to this document
- Propose improvements in team meetings
- Update documentation as you learn

---

**Last Updated:** 2025-11-12
**Maintainer:** Project Lead
**Version:** 1.0
