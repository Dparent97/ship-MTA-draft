# Engineer Tasks - Ship MTA Deployment

This document breaks down all tasks needed to complete, test, and deploy the Ship Maintenance Tracking Application. Tasks are organized by priority and complexity to help junior engineers contribute effectively.

## Task Priority Legend

- 🔴 **Critical**: Must be done before deployment
- 🟡 **High**: Important for production readiness
- 🟢 **Medium**: Nice to have, improves UX
- 🔵 **Low**: Future enhancements

## Task Complexity Legend

- ⭐ **Easy**: 1-2 hours, minimal complexity
- ⭐⭐ **Medium**: 3-6 hours, moderate complexity
- ⭐⭐⭐ **Hard**: 1-2 days, significant complexity

---

## Phase 1: Core Development (Pre-Testing)

### 1.1 Database Setup 🔴 ⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 2 hours

**Description**: Set up the SQLite database with all required tables.

**Tasks**:
- [ ] Create `database.py` with SQLAlchemy models
- [ ] Define models: WorkItem, CrewMember, Photo, AdminNote
- [ ] Create relationships between models
- [ ] Write database initialization script
- [ ] Test database creation locally
- [ ] Verify all foreign key relationships work

**Files to create/modify**:
- `models/database.py`
- `scripts/init_db.py`

**Testing**:
- Run `python scripts/init_db.py`
- Verify `ship_mta.db` is created
- Check all tables exist using SQLite browser

**Documentation**: See `DATABASE_SCHEMA.md`

---

### 1.2 User Authentication System 🔴 ⭐⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 4 hours

**Description**: Implement basic login system with crew member and admin roles.

**Tasks**:
- [ ] Create User model with role field (crew/admin)
- [ ] Implement login endpoint (`/login`)
- [ ] Implement logout endpoint (`/logout`)
- [ ] Add session management (Flask-Login or similar)
- [ ] Create login page template
- [ ] Add password hashing (bcrypt)
- [ ] Seed initial users from `crew_data.csv`

**Files to create/modify**:
- `routes/auth.py`
- `templates/login.html`
- `scripts/seed_users.py`

**Testing**:
- Test login with valid credentials
- Test login with invalid credentials
- Verify session persists across pages
- Test logout functionality

**Security considerations**:
- Hash passwords before storing
- Implement CSRF protection on login form
- Add rate limiting to prevent brute force (optional)

---

### 1.3 Work Item CRUD Operations 🔴 ⭐⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 6 hours

**Description**: Build core functionality for creating, reading, updating, and deleting work items.

**Tasks**:
- [ ] Create `/work-items` route (list view)
- [ ] Create `/work-items/new` route (create form)
- [ ] Create `/work-items/<id>` route (detail view)
- [ ] Create `/work-items/<id>/edit` route (edit form)
- [ ] Implement form validation
- [ ] Add status field (Assigned, In Progress, Completed)
- [ ] Add priority field (High, Medium, Low)
- [ ] Implement assignment to crew members

**Files to create/modify**:
- `routes/work_items.py`
- `templates/work_items/list.html`
- `templates/work_items/detail.html`
- `templates/work_items/form.html`

**Testing**:
- Create 5 test work items
- Edit each work item
- Verify data persists
- Test form validation

---

### 1.4 Photo Upload System 🔴 ⭐⭐⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 8 hours

**Description**: Implement photo upload with mobile camera support.

**Tasks**:
- [ ] Create photo upload endpoint (`/api/photos/upload`)
- [ ] Configure file storage directory
- [ ] Add file type validation (jpg, png, heic)
- [ ] Implement image compression (target 200-500KB per photo)
- [ ] Create photo gallery UI component
- [ ] Add mobile camera input (`<input type="file" accept="image/*" capture="camera">`)
- [ ] Implement photo deletion
- [ ] Link photos to work items

**Files to create/modify**:
- `routes/photos.py`
- `utils/image_processing.py`
- `templates/components/photo_upload.html`
- `static/js/photo_upload.js`

**Testing**:
- Test upload from iPhone Safari
- Test upload from Android Chrome
- Test upload of 4 photos to single work item
- Verify photos are compressed appropriately
- Test photo display in work item detail

**Technical notes**:
- Use Pillow for image processing
- Store photos in `static/uploads/` directory
- Generate unique filenames (UUID)
- Store photo metadata in database

---

### 1.5 SMS Notification System 🔴 ⭐⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 4 hours

**Description**: Integrate Twilio to send SMS notifications when work is assigned.

**Tasks**:
- [ ] Install Twilio SDK (`pip install twilio`)
- [ ] Create SMS service module
- [ ] Implement `send_assignment_notification()` function
- [ ] Add Twilio credentials to environment variables
- [ ] Hook SMS sending into work item assignment
- [ ] Add error handling for failed SMS
- [ ] Log all SMS attempts

**Files to create/modify**:
- `services/sms.py`
- `routes/work_items.py` (add SMS trigger)
- `.env.example` (document required variables)

**Environment variables needed**:
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

**Testing**:
- Test SMS to your personal phone first
- Test SMS to all 6 crew member numbers
- Test failure handling with invalid number
- Verify SMS content format

**Twilio setup**:
- Create Twilio account (free trial available)
- Get phone number ($1-2/month for production)
- Verify all recipient numbers

---

### 1.6 Admin Notes System 🟡 ⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 3 hours

**Description**: Allow admins to add notes to work items.

**Tasks**:
- [ ] Create AdminNote model
- [ ] Create `/work-items/<id>/notes/add` endpoint
- [ ] Create `/work-items/<id>/notes/<note_id>/edit` endpoint
- [ ] Add notes display section to work item detail page
- [ ] Implement real-time note updates (or page refresh)
- [ ] Add timestamp and author to each note

**Files to create/modify**:
- `models/database.py` (add AdminNote model)
- `routes/notes.py`
- `templates/work_items/detail.html` (add notes section)

**Testing**:
- Add 3 notes to a work item
- Edit existing note
- Verify notes display chronologically
- Check notes are visible to both admin and crew

---

## Phase 2: Mobile UI Optimization

### 2.1 Responsive Layout 🔴 ⭐⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 6 hours

**Description**: Ensure UI works well on mobile devices (iPhone and Android).

**Tasks**:
- [ ] Add viewport meta tag to all pages
- [ ] Implement mobile-first CSS
- [ ] Test layouts on 320px, 375px, 768px widths
- [ ] Ensure buttons are min 44x44px (iOS guideline)
- [ ] Fix any horizontal scrolling issues
- [ ] Test in Chrome DevTools device emulation
- [ ] Optimize font sizes for mobile readability

**Files to create/modify**:
- `static/css/mobile.css`
- `templates/base.html` (add meta tags)
- All template files (test and adjust)

**Testing checklist**:
- [ ] Test on actual iPhone (Safari)
- [ ] Test on actual Android device (Chrome)
- [ ] Test in landscape and portrait
- [ ] Verify all forms are usable
- [ ] Check photo galleries are scrollable

**Key breakpoints**:
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

---

### 2.2 Mobile Photo Upload UX 🟡 ⭐⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 4 hours

**Description**: Optimize photo upload experience for mobile users.

**Tasks**:
- [ ] Add "Take Photo" button with camera icon
- [ ] Implement photo preview before upload
- [ ] Add upload progress indicator
- [ ] Show success/error messages
- [ ] Allow multiple photo selection
- [ ] Add photo rotation controls (if needed)
- [ ] Optimize for slow 3G connections

**Files to create/modify**:
- `static/js/photo_upload.js`
- `templates/components/photo_upload.html`
- `static/css/photo_upload.css`

**Testing**:
- Test camera access permission flow
- Test on iPhone Safari
- Test on Android Chrome
- Test with 3G throttling in DevTools
- Verify upload progress shows correctly

---

### 2.3 Touch-Friendly Navigation 🟢 ⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 2 hours

**Description**: Make navigation easier on touch devices.

**Tasks**:
- [ ] Increase button padding (min 44x44px)
- [ ] Add touch feedback (active states)
- [ ] Implement swipe gestures (optional)
- [ ] Fix any double-tap zoom issues
- [ ] Test all interactive elements
- [ ] Add "back to top" button for long pages

**Files to create/modify**:
- `static/css/mobile.css`
- `static/js/mobile.js`

**Testing**:
- Test all buttons are tappable
- Verify no accidental taps
- Check scrolling is smooth
- Test on both iOS and Android

---

## Phase 3: Document Generation

### 3.1 PDF Work Order Generator 🟡 ⭐⭐⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 8 hours

**Description**: Generate PDF documents for completed work items.

**Tasks**:
- [ ] Choose PDF library (ReportLab or WeasyPrint)
- [ ] Create PDF template design
- [ ] Implement photo embedding (3-4 photos per document)
- [ ] Add work item details (number, description, dates)
- [ ] Include admin notes and completion notes
- [ ] Generate filename: `WORKITEM-XXX-YYYYMMDD.pdf`
- [ ] Add download endpoint
- [ ] Optimize PDF file size

**Files to create/modify**:
- `services/pdf_generator.py`
- `templates/pdf/work_order.html` (if using WeasyPrint)
- `routes/documents.py`

**Packages to install**:
```bash
pip install reportlab  # OR
pip install WeasyPrint
```

**Testing**:
- Generate PDF with 3 photos
- Generate PDF with 4 photos
- Verify photos are clear and properly sized
- Test PDF opens on mobile device
- Check file size (should be < 5MB)

**PDF should include**:
- Work item number and description
- Location and priority
- Assigned crew member
- Assignment date and completion date
- All photos (3-4 per item)
- Admin notes
- Completion notes
- Generated date/timestamp

---

### 3.2 Bulk Document Export 🟢 ⭐⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 4 hours

**Description**: Allow exporting multiple work items at once.

**Tasks**:
- [ ] Add checkboxes to work item list
- [ ] Create "Export Selected" button
- [ ] Generate ZIP file with multiple PDFs
- [ ] Add "Export All Completed" option
- [ ] Implement progress indicator for large exports

**Files to create/modify**:
- `routes/documents.py`
- `templates/work_items/list.html`
- `static/js/bulk_export.js`

**Testing**:
- Select 5 work items and export
- Verify ZIP contains all PDFs
- Test with 20+ work items
- Check file naming is consistent

---

## Phase 4: Testing

### 4.1 Execute Manual Testing 🔴 ⭐⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 12 hours

**Description**: Run through complete testing checklist.

**Tasks**:
- [ ] Follow `TESTING_CHECKLIST.md` step-by-step
- [ ] Document all issues found
- [ ] Create GitHub issues for bugs
- [ ] Re-test after fixes
- [ ] Get sign-off on test completion

**Files needed**:
- `TESTING_CHECKLIST.md`
- Test device access (iPhone, Android)

**Deliverables**:
- Completed testing checklist
- List of all issues found
- Test coverage summary
- Screenshots of key features working

---

### 4.2 SMS Integration Testing 🔴 ⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 2 hours

**Description**: Verify SMS delivery to all 6 crew members.

**Tasks**:
- [ ] Verify all phone numbers in `crew_data.csv`
- [ ] Send test SMS to each crew member
- [ ] Document any delivery failures
- [ ] Verify SMS content format
- [ ] Check Twilio logs for issues

**Coordination needed**:
- Get confirmation from all crew members they received SMS
- Note any phone numbers that need correction

---

### 4.3 Mobile Device Testing 🔴 ⭐⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 6 hours

**Description**: Test on real iPhone and Android devices.

**Tasks**:
- [ ] Test on iPhone (Safari) - all features
- [ ] Test on Android (Chrome) - all features
- [ ] Test camera photo upload on both
- [ ] Verify UI is usable on small screens
- [ ] Test slow network conditions
- [ ] Document any device-specific issues

**Devices needed**:
- iPhone 8 or newer (iOS 13+)
- Android device (Android 8+)

**Focus areas**:
- Photo upload from camera
- Touch interaction
- Form input and keyboard
- Page navigation
- Photo viewing

---

## Phase 5: Deployment

### 5.1 Railway Setup 🔴 ⭐⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 3 hours

**Description**: Set up Railway hosting and deploy application.

**Tasks**:
- [ ] Create Railway account
- [ ] Connect GitHub repository
- [ ] Configure environment variables
- [ ] Set up start command
- [ ] Configure build settings
- [ ] Deploy application
- [ ] Verify deployment success

**Environment variables to set**:
```
SECRET_KEY=<generate-random-key>
DATABASE_URL=<railway-will-provide-if-using-postgres>
TWILIO_ACCOUNT_SID=<from-twilio>
TWILIO_AUTH_TOKEN=<from-twilio>
TWILIO_PHONE_NUMBER=<from-twilio>
```

**Railway configuration**:
- Start command: `gunicorn app:app` (if using Flask)
- Python version: 3.9+
- Region: US West (or closest to ship location)

**Documentation**:
- See `README.md` deployment section
- Railway docs: https://docs.railway.app/

---

### 5.2 Production Database Setup 🔴 ⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 2 hours

**Description**: Initialize production database with crew data.

**Tasks**:
- [ ] Deploy database schema to production
- [ ] Load crew member data from CSV
- [ ] Create admin account
- [ ] Create crew member accounts (6 total)
- [ ] Verify all logins work
- [ ] Document all credentials securely

**Security**:
- Use strong admin password
- Use simple but unique crew passwords
- Document passwords in secure location (not in code!)

---

### 5.3 Post-Deployment Verification 🔴 ⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 2 hours

**Description**: Verify all features work in production.

**Tasks**:
- [ ] Access production URL
- [ ] Test login as admin
- [ ] Test login as crew member
- [ ] Create test work item
- [ ] Upload test photo
- [ ] Send test SMS
- [ ] Generate test PDF
- [ ] Monitor Railway logs for errors

**Smoke test checklist**:
- [ ] Homepage loads
- [ ] Database accessible
- [ ] Photo upload works
- [ ] SMS sends successfully
- [ ] No console errors

---

### 5.4 Monitoring Setup 🟡 ⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 2 hours

**Description**: Set up monitoring and alerts.

**Tasks**:
- [ ] Configure Railway uptime monitoring
- [ ] Set up error alerting (email or SMS)
- [ ] Create health check endpoint (`/health`)
- [ ] Document how to view logs
- [ ] Set up daily backup (if applicable)

**Health check endpoint**:
```python
@app.route('/health')
def health():
    # Check database connection
    # Check file storage
    # Return JSON with status
    return jsonify({"status": "healthy"})
```

---

## Phase 6: Documentation and Handoff

### 6.1 Update README 🔴 ⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 2 hours

**Description**: Complete README with deployment info.

**Tasks**:
- [ ] Add deployment instructions
- [ ] Document environment variables
- [ ] Add troubleshooting section
- [ ] Include contact information
- [ ] Add Railway dashboard links

**See**: Task 6.3 below for specific README updates

---

### 6.2 Create Admin Guide 🟡 ⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 3 hours

**Description**: Write guide for non-technical admin users.

**Tasks**:
- [ ] Create `ADMIN_GUIDE.md`
- [ ] Add screenshots of key features
- [ ] Document common workflows
- [ ] Include troubleshooting tips
- [ ] Add FAQ section

**Guide should cover**:
- How to log in
- How to create work items
- How to assign work to crew
- How to add notes
- How to generate documents
- What to do if SMS fails

---

### 6.3 Create Crew Member Guide 🟡 ⭐
**Status**: Pending
**Assigned to**: ___________
**Estimated time**: 2 hours

**Description**: Write simple guide for crew members.

**Tasks**:
- [ ] Create `CREW_GUIDE.md`
- [ ] Use simple language
- [ ] Add mobile screenshots
- [ ] Document photo upload steps
- [ ] Include login instructions

**Guide should cover**:
- How to log in on mobile
- How to view assignments
- How to upload photos
- How to mark work complete
- Who to contact for help

---

## Phase 7: Optional Enhancements

### 7.1 Email Notifications 🔵 ⭐⭐
**Status**: Optional
**Estimated time**: 4 hours

**Description**: Add email notifications as backup to SMS.

**Tasks**:
- [ ] Choose email service (SendGrid, Mailgun)
- [ ] Implement email sending
- [ ] Create email templates
- [ ] Add email field to crew members
- [ ] Send email + SMS on assignment

---

### 7.2 Real-Time Updates 🔵 ⭐⭐⭐
**Status**: Optional
**Estimated time**: 8 hours

**Description**: Add WebSocket support for real-time updates.

**Tasks**:
- [ ] Install Socket.IO or similar
- [ ] Implement real-time work item updates
- [ ] Add live notification system
- [ ] Test with multiple concurrent users

---

### 7.3 Mobile PWA Support 🔵 ⭐⭐
**Status**: Optional
**Estimated time**: 4 hours

**Description**: Make app installable as Progressive Web App.

**Tasks**:
- [ ] Create `manifest.json`
- [ ] Add service worker for offline support
- [ ] Create app icons
- [ ] Test "Add to Home Screen" on iOS and Android

---

### 7.4 Data Export (CSV/Excel) 🔵 ⭐
**Status**: Optional
**Estimated time**: 2 hours

**Description**: Export work item data to CSV or Excel.

**Tasks**:
- [ ] Create CSV export endpoint
- [ ] Include all work item fields
- [ ] Add date range filter
- [ ] Generate downloadable file

---

## Task Assignment Guidelines for Junior Engineers

### How to Pick a Task

1. **Check prerequisites**: Some tasks depend on others. For example, you can't test photo upload (4.3) until photo upload is implemented (1.4).

2. **Match your skill level**:
   - New to web development? Start with ⭐ tasks
   - Some experience? Try ⭐⭐ tasks
   - Experienced? Take on ⭐⭐⭐ tasks

3. **Consider priority**: Focus on 🔴 Critical and 🟡 High priority tasks first.

4. **Pair programming**: If a task seems challenging, pair with another engineer.

### Before Starting a Task

- [ ] Read the task description completely
- [ ] Check all prerequisite tasks are done
- [ ] Review relevant documentation
- [ ] Set up your development environment
- [ ] Create a new branch: `feature/task-name`

### While Working on a Task

- [ ] Update task status to "In Progress"
- [ ] Commit code frequently with clear messages
- [ ] Test your changes locally
- [ ] Ask for help if stuck > 30 minutes
- [ ] Document any decisions or challenges

### After Completing a Task

- [ ] Run relevant tests from `TESTING_CHECKLIST.md`
- [ ] Update task status to "Done"
- [ ] Create pull request
- [ ] Request code review
- [ ] Update any related documentation

## Getting Help

**Stuck on a task?** Here's how to get help:

1. **Check documentation**:
   - `README.md` - Project overview
   - `TESTING_CHECKLIST.md` - Testing procedures
   - `DATABASE_SCHEMA.md` - Database structure (if exists)

2. **Search for errors**:
   - Copy error message to Google
   - Check Stack Overflow
   - Review GitHub issues in similar projects

3. **Ask teammates**:
   - Describe what you're trying to do
   - Share error messages and code
   - Explain what you've already tried

4. **Escalate if needed**:
   - If blocked > 2 hours, notify team lead
   - Document the blocker
   - Move to a different task while waiting

## Development Environment Setup

Before starting any tasks, ensure your environment is set up:

```bash
# Clone repository
git clone <repo-url>
cd ship-MTA-draft

# Create virtual environment (Python)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your values

# Initialize database
python scripts/init_db.py

# Run development server
flask run  # or python app.py
```

## Code Style Guidelines

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused
- Write descriptive commit messages

## Commit Message Format

```
[Task ID] Brief description

- Detailed change 1
- Detailed change 2

Testing: Describe how you tested this
```

Example:
```
[1.4] Implement photo upload system

- Add photo upload endpoint
- Implement image compression
- Create photo gallery UI component

Testing: Uploaded 4 photos from iPhone Safari, verified compression
```

## Questions?

If you have questions about any task:
- Create a GitHub issue with the question
- Tag it with "question" label
- Reference the task number

---

## Progress Tracking

| Task ID | Task Name | Priority | Complexity | Status | Assigned To | Completion Date |
|---------|-----------|----------|------------|--------|-------------|-----------------|
| 1.1 | Database Setup | 🔴 | ⭐ | Pending | | |
| 1.2 | User Authentication | 🔴 | ⭐⭐ | Pending | | |
| 1.3 | Work Item CRUD | 🔴 | ⭐⭐ | Pending | | |
| 1.4 | Photo Upload | 🔴 | ⭐⭐⭐ | Pending | | |
| 1.5 | SMS Notifications | 🔴 | ⭐⭐ | Pending | | |
| 1.6 | Admin Notes | 🟡 | ⭐ | Pending | | |
| 2.1 | Responsive Layout | 🔴 | ⭐⭐ | Pending | | |
| 2.2 | Mobile Photo UX | 🟡 | ⭐⭐ | Pending | | |
| 2.3 | Touch Navigation | 🟢 | ⭐ | Pending | | |
| 3.1 | PDF Generator | 🟡 | ⭐⭐⭐ | Pending | | |
| 3.2 | Bulk Export | 🟢 | ⭐⭐ | Pending | | |
| 4.1 | Manual Testing | 🔴 | ⭐⭐ | Pending | | |
| 4.2 | SMS Testing | 🔴 | ⭐ | Pending | | |
| 4.3 | Mobile Testing | 🔴 | ⭐⭐ | Pending | | |
| 5.1 | Railway Setup | 🔴 | ⭐⭐ | Pending | | |
| 5.2 | Production DB | 🔴 | ⭐ | Pending | | |
| 5.3 | Deploy Verification | 🔴 | ⭐ | Pending | | |
| 5.4 | Monitoring | 🟡 | ⭐ | Pending | | |
| 6.1 | Update README | 🔴 | ⭐ | Pending | | |
| 6.2 | Admin Guide | 🟡 | ⭐ | Pending | | |
| 6.3 | Crew Guide | 🟡 | ⭐ | Pending | | |

**Total Tasks**: 20 (17 core + 3 documentation)
**Estimated Total Time**: ~75 hours
**Team size recommendation**: 2-3 junior engineers
**Timeline**: 2-3 weeks for full development and testing

---

Last updated: [Date]
