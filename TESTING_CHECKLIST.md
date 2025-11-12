# Ship MTA Testing Checklist

This document provides a comprehensive testing checklist for validating the Ship Maintenance Tracking Application before and during the 60-day deployment.

## Pre-Deployment Testing (Development Environment)

### 1. SMS Delivery System

#### 1.1 Test Configuration
- [ ] Verify Twilio credentials are set in environment variables
- [ ] Confirm all 6 crew member phone numbers are correctly formatted in `crew_data.csv`
- [ ] Check phone numbers include country code (e.g., +1 for US)

#### 1.2 SMS Delivery Tests
- [ ] **Test 1: Single Assignment Notification**
  - Assign a work item to one crew member
  - Verify SMS received within 30 seconds
  - Confirm message format: "New work item assigned: [ITEM-XXX] [Description]"

- [ ] **Test 2: Multiple Assignments**
  - Assign 3 different work items to 3 different crew members
  - Verify each crew member receives only their assignment
  - Confirm no duplicate messages

- [ ] **Test 3: All Crew Members**
  - Create 6 work items and assign one to each crew member
  - Verify all 6 crew members receive their SMS
  - Document any phone numbers that fail to receive SMS

- [ ] **Test 4: Reassignment Notification**
  - Assign work item to Crew Member A
  - Reassign same work item to Crew Member B
  - Verify both members receive appropriate notifications

#### 1.3 SMS Failure Handling
- [ ] Test with invalid phone number (expect graceful error)
- [ ] Verify error is logged in application
- [ ] Confirm work item is still created even if SMS fails

### 2. Assignment Workflow

#### 2.1 Create and Assign
- [ ] **Admin Side:**
  - Log in as admin
  - Create new work item with all required fields
  - Upload 1 test photo
  - Assign to crew member
  - Verify work item appears in "Assigned" status

- [ ] **Crew Member Side:**
  - Log in as assigned crew member
  - Verify work item appears in "My Assignments" list
  - Confirm all details are visible (description, location, priority)
  - Check photo is displayed correctly

#### 2.2 Edit Work in Progress
- [ ] Start work on assigned item (click "Start Work")
- [ ] Add progress notes (minimum 10 characters)
- [ ] Upload 2 additional photos
- [ ] Save without completing
- [ ] Verify work item shows as "In Progress"
- [ ] Re-open and confirm notes and photos are saved

#### 2.3 Submit Completion
- [ ] Open "In Progress" work item
- [ ] Add completion notes
- [ ] Upload final photo (total should be 3-4 photos)
- [ ] Mark as complete
- [ ] Verify work item moves to "Completed" status
- [ ] Confirm submission timestamp is recorded

#### 2.4 Workflow Edge Cases
- [ ] Try to access another crew member's assignment (should be denied)
- [ ] Test editing completed work item (should be read-only for crew)
- [ ] Verify admin can view all work items regardless of status

### 3. Admin Notes System

#### 3.1 Create Notes
- [ ] Navigate to any work item as admin
- [ ] Add note with 20+ characters
- [ ] Save note
- [ ] Verify note appears in notes list with timestamp

#### 3.2 Edit Notes
- [ ] Click edit on existing note
- [ ] Modify note content
- [ ] Save changes
- [ ] Verify updated content is displayed
- [ ] Check timestamp shows last edit time

#### 3.3 View Notes History
- [ ] Add 3 notes to a single work item
- [ ] Verify all notes are displayed chronologically
- [ ] Check each note shows author and timestamp
- [ ] Confirm notes are visible on both admin and crew views

#### 3.4 Notes with Special Characters
- [ ] Test note with special characters: `!@#$%^&*()`
- [ ] Test note with line breaks
- [ ] Test note with very long text (500+ characters)
- [ ] Verify all display correctly without breaking UI

### 4. Mobile UI Testing

#### 4.1 iPhone Safari Testing
**Device Requirements:** iPhone 8 or newer, iOS 13+

- [ ] **Login Screen**
  - Verify form fits screen without horizontal scrolling
  - Test username/password input
  - Confirm buttons are tappable (min 44x44px)

- [ ] **Work Item List**
  - Verify list is scrollable
  - Check card layout on small screen
  - Confirm priority badges are visible
  - Test pull-to-refresh (if implemented)

- [ ] **Work Item Detail**
  - Verify all fields are readable
  - Check photo thumbnails display correctly
  - Test photo tap to view full size

- [ ] **Photo Upload**
  - Tap "Upload Photo" button
  - Select "Take Photo" from iOS picker
  - Grant camera permission if prompted
  - Take test photo
  - Verify photo appears in preview
  - Confirm upload progress indicator

- [ ] **Form Inputs**
  - Test text area for notes
  - Verify keyboard doesn't obscure input
  - Check autocorrect behavior
  - Test form submission

#### 4.2 Android Chrome Testing
**Device Requirements:** Android 8+ device

- [ ] **Login Screen**
  - Verify layout on Android screen
  - Test keyboard appearance/dismissal
  - Confirm button spacing

- [ ] **Work Item List**
  - Test scrolling performance
  - Verify touch targets are adequate
  - Check loading states

- [ ] **Work Item Detail**
  - Verify photo gallery layout
  - Test back button navigation

- [ ] **Photo Upload**
  - Tap "Upload Photo" button
  - Select "Camera" from Android picker
  - Grant camera permission if prompted
  - Take test photo
  - Verify photo upload success
  - Test "Choose from Gallery" option

- [ ] **Performance**
  - Test app with 3G throttling
  - Verify loading states are shown
  - Check photo upload on slow connection

#### 4.3 Cross-Browser Mobile Issues
- [ ] Test landscape orientation on both platforms
- [ ] Verify touch gestures (tap, scroll, pinch-zoom on photos)
- [ ] Check form validation messages are visible
- [ ] Test with system dark mode enabled
- [ ] Verify no console errors in mobile browsers (use remote debugging)

### 5. Photo Upload and Management

#### 5.1 Camera Upload
- [ ] **From Mobile Camera (iPhone)**
  - Open work item on iPhone
  - Click "Upload Photo"
  - Select "Take Photo"
  - Capture photo
  - Verify upload completes
  - Check photo appears in work item

- [ ] **From Mobile Camera (Android)**
  - Repeat above steps on Android device
  - Verify consistent behavior

#### 5.2 Photo Gallery Upload
- [ ] Upload existing photo from phone gallery
- [ ] Verify photo preview before upload
- [ ] Check multiple photos can be added
- [ ] Test photo order is maintained

#### 5.3 Photo Storage
- [ ] Upload 4 photos to single work item
- [ ] Verify all photos are stored
- [ ] Check photos persist after logout/login
- [ ] Verify photos load in correct resolution
- [ ] Test photo file size (should be optimized, under 500KB each)

#### 5.4 Photo Limits
- [ ] Test uploading 5+ photos (verify limit or handling)
- [ ] Test very large photo (5MB+)
- [ ] Verify error messages for upload failures
- [ ] Check system behavior when disk space is low

### 6. Document Generation

#### 6.1 Work Order Document
- [ ] Complete a work item with 3 photos
- [ ] Click "Generate Document" (or similar button)
- [ ] Verify PDF is generated
- [ ] Check PDF contains:
  - Work item number and description
  - Location and priority
  - Assignment and completion dates
  - All 3 photos embedded
  - Admin notes (if any)
  - Completion notes

#### 6.2 Document with 4 Photos
- [ ] Complete work item with 4 photos
- [ ] Generate document
- [ ] Verify all 4 photos appear in PDF
- [ ] Check photo layout is readable
- [ ] Confirm photo captions/timestamps

#### 6.3 Document Quality
- [ ] Verify PDF is properly formatted
- [ ] Check photos are clear and properly sized
- [ ] Test document opens on mobile device
- [ ] Verify document can be emailed/shared
- [ ] Check file size is reasonable (<5MB)

#### 6.4 Bulk Document Generation
- [ ] Select 5 completed work items
- [ ] Generate documents for all
- [ ] Verify all 5 PDFs are created
- [ ] Check each document has correct content

### 7. Railway Deployment Validation

#### 7.1 Pre-Deployment Checks
- [ ] Verify `railway.json` or `railway.toml` is configured
- [ ] Check environment variables are set in Railway dashboard:
  - `DATABASE_URL` (if applicable)
  - `SECRET_KEY`
  - `TWILIO_ACCOUNT_SID`
  - `TWILIO_AUTH_TOKEN`
  - `TWILIO_PHONE_NUMBER`
- [ ] Verify `requirements.txt` or `package.json` is up to date
- [ ] Check `Procfile` or start command is correct

#### 7.2 Deployment Process
- [ ] Connect GitHub repository to Railway
- [ ] Trigger deployment
- [ ] Monitor build logs for errors
- [ ] Verify deployment completes successfully
- [ ] Check deployment URL is active

#### 7.3 Post-Deployment Smoke Tests
- [ ] **Basic Connectivity**
  - [ ] Access application URL
  - [ ] Verify homepage loads
  - [ ] Check no SSL/certificate errors

- [ ] **Database**
  - [ ] Verify database is accessible
  - [ ] Check initial data is loaded (crew members, etc.)
  - [ ] Test database writes (create test work item)

- [ ] **File Storage**
  - [ ] Upload test photo
  - [ ] Verify photo is stored correctly
  - [ ] Check photo can be retrieved and displayed

- [ ] **SMS Integration**
  - [ ] Send test SMS from production environment
  - [ ] Verify SMS is received
  - [ ] Check Twilio logs in dashboard

#### 7.4 Production Monitoring
- [ ] Set up Railway health check endpoint
- [ ] Configure uptime monitoring (Railway built-in or external)
- [ ] Set up error alerting
- [ ] Document how to view application logs
- [ ] Test log access from Railway dashboard

#### 7.5 Performance Testing
- [ ] Test page load times (<3 seconds)
- [ ] Upload 4 photos simultaneously
- [ ] Create 10 work items rapidly
- [ ] Test with 3 concurrent users
- [ ] Monitor Railway metrics (CPU, memory, disk)

### 8. Data Validation and Integrity

#### 8.1 Data Entry Validation
- [ ] Test required field validation
- [ ] Try to submit form with missing data
- [ ] Verify error messages are clear
- [ ] Test character limits on text fields
- [ ] Check date field validation

#### 8.2 Database Integrity
- [ ] Create 10 work items
- [ ] Verify all are saved correctly
- [ ] Check foreign key relationships (crew assignments)
- [ ] Test data retrieval queries
- [ ] Verify no data loss on page refresh

#### 8.3 Scale Testing (60-Day Simulation)
- [ ] Create 70 work items over several days
- [ ] Add 240+ photos (simulate full deployment)
- [ ] Verify application performance with full data
- [ ] Check database size (~50MB + overhead)
- [ ] Monitor Railway free tier usage
- [ ] Document if upgrade is needed

### 9. Security and Access Control

#### 9.1 Authentication
- [ ] Test login with valid credentials
- [ ] Test login with invalid credentials
- [ ] Verify password is not shown in plain text
- [ ] Test session timeout (if implemented)
- [ ] Verify logout functionality

#### 9.2 Authorization
- [ ] Crew member cannot access admin functions
- [ ] Crew member cannot view other crew members' assignments
- [ ] Admin can view all work items
- [ ] Admin can edit any work item
- [ ] Test direct URL access to restricted pages

#### 9.3 Data Protection
- [ ] Verify photos are not publicly accessible without login
- [ ] Check SQL injection protection on forms
- [ ] Test XSS protection in notes/comments
- [ ] Verify CSRF protection on forms (if implemented)

### 10. User Experience

#### 10.1 Navigation
- [ ] Test all navigation menu items
- [ ] Verify breadcrumbs (if present)
- [ ] Check back button behavior
- [ ] Test deep linking to specific work items

#### 10.2 Responsiveness
- [ ] Test on 320px width (iPhone SE)
- [ ] Test on tablet (768px)
- [ ] Test on desktop (1920px)
- [ ] Verify no horizontal scrolling

#### 10.3 Loading States
- [ ] Verify loading indicators during photo upload
- [ ] Check loading state during page navigation
- [ ] Test slow network conditions (3G throttling)
- [ ] Verify appropriate error messages

#### 10.4 Accessibility
- [ ] Test with screen reader (basic check)
- [ ] Verify sufficient color contrast
- [ ] Check keyboard navigation
- [ ] Verify form labels are present

## Deployment Day Checklist

- [ ] All pre-deployment tests passed
- [ ] Railway deployment successful
- [ ] Production environment variables verified
- [ ] Test SMS sent to all 6 crew members
- [ ] Admin login credentials shared securely
- [ ] Crew member login credentials shared securely
- [ ] Application URL bookmarked on all crew mobile devices
- [ ] Emergency contact procedure documented
- [ ] Backup procedure verified (if applicable)
- [ ] Monitoring alerts configured

## Post-Deployment Monitoring (First Week)

- [ ] **Day 1**: Monitor all SMS notifications
- [ ] **Day 2**: Check photo upload success rate
- [ ] **Day 3**: Verify document generation works
- [ ] **Day 4**: Review Railway metrics (CPU, memory, bandwidth)
- [ ] **Day 5**: Check for any error reports from crew
- [ ] **Day 7**: Validate storage usage is within limits

## Issue Tracking Template

When issues are found, document them using this template:

```
### Issue: [Short Description]
- **Severity**: Critical / High / Medium / Low
- **Device/Browser**: [e.g., iPhone 12, Safari 14]
- **Steps to Reproduce**:
  1. Step 1
  2. Step 2
  3. Step 3
- **Expected Result**: [What should happen]
- **Actual Result**: [What actually happened]
- **Screenshots**: [Attach if applicable]
- **Workaround**: [If any temporary fix exists]
```

## Test Coverage Summary

After completing all tests, fill out this summary:

- **Total Test Cases**: [ ]
- **Passed**: [ ]
- **Failed**: [ ]
- **Blocked**: [ ]
- **Pass Rate**: [ ]%

**Critical Issues Found**: [ ]
**High Priority Issues**: [ ]
**Medium Priority Issues**: [ ]
**Low Priority Issues**: [ ]

**Ready for Production?** YES / NO

**Sign-off**:
- Tested by: _______________
- Date: _______________
- Approved by: _______________

---

## Quick Reference: Test Credentials

```
Admin:
- Username: [TO BE SET]
- Password: [TO BE SET]

Crew Member 1:
- Username: [TO BE SET]
- Password: [TO BE SET]

[... repeat for all 6 crew members]
```

## Quick Reference: Test Data

- **Test Phone Number**: [Your test number]
- **Railway App URL**: [To be filled after deployment]
- **Twilio Dashboard**: https://www.twilio.com/console
- **Railway Dashboard**: https://railway.app/dashboard
