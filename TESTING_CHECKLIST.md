# Testing Checklist - Ship Maintenance Tracking Application

## Overview
This comprehensive testing checklist covers all critical functionality of the Arrowhead MTA 2026 Ship Maintenance Tracking Application. Use this checklist to validate the application before production deployment.

**Target Devices:**
- iPhone (Safari)
- Android (Chrome)
- Desktop (Chrome, Firefox, Safari)

**Test Environments:**
- Local development (http://localhost:5001)
- Railway production (your-app.railway.app)

---

## 1. Authentication & Session Management

### Crew Login
- [ ] Navigate to login page (/)
- [ ] Select crew member from dropdown (test with all 9 crew members: DP, AL, Kaitlyn, Mark, Art, D2, Zach, Maverick, Rhyan)
- [ ] Enter correct password: `crew350`
- [ ] Verify successful login redirects to `/crew/submit`
- [ ] Test incorrect password - should show error message
- [ ] Test session persistence (refresh page, should stay logged in)

### Admin Login
- [ ] Navigate to admin login (/admin-login)
- [ ] Enter username: `admin`
- [ ] Enter password: `admin350`
- [ ] Verify successful login redirects to `/admin/dashboard`
- [ ] Test incorrect credentials - should show error message
- [ ] Test session persistence

### Session Timeout
- [ ] Login and wait 8+ hours (or temporarily reduce PERMANENT_SESSION_LIFETIME in config.py)
- [ ] Attempt to access protected page
- [ ] Verify redirect to login page

### Logout
- [ ] Click logout button from crew or admin interface
- [ ] Verify redirect to login page
- [ ] Attempt to access protected page without logging in
- [ ] Verify redirect to login page

---

## 2. Work Item Submission (Crew Interface)

### Create New Work Item - Custom Entry
- [ ] Login as crew member
- [ ] Select "Custom Entry" from dropdown
- [ ] Fill in all required fields:
  - Location: "Engine Room 3"
  - NS Equipment: "Main Engine Port"
  - Description: "Test work item submission"
  - Detail: "Detailed description of maintenance work required"
  - References: "MRC 123-456" (optional)
- [ ] Submit without photos
- [ ] Verify success page displays
- [ ] Verify item appears in admin dashboard with status "Submitted"
- [ ] Verify item_number is auto-generated (e.g., "DRAFT_0001")

### Create New Work Item - EV Yard Predefined
- [ ] Select any EV Yard item from dropdown (e.g., "EV_001 - Shaft Seal Replacement")
- [ ] Verify form fields auto-populate with predefined data
- [ ] Submit form
- [ ] Verify success and admin dashboard shows correct item

### Create New Work Item - DRAFT Predefined
- [ ] Select any DRAFT item from dropdown (e.g., "DRAFT_001 - 3M-6 Trash Can Replacement")
- [ ] Verify form fields auto-populate
- [ ] Submit form
- [ ] Verify item appears in admin dashboard

### Photo Upload - Basic
- [ ] Create new work item
- [ ] Click "Add Photo" button
- [ ] Upload 1 photo (JPEG format)
- [ ] Add caption: "Test photo caption"
- [ ] Submit form
- [ ] Verify photo appears in admin view
- [ ] Verify caption displays correctly

### Photo Upload - Multiple Photos (3-4 photos)
- [ ] Create new work item
- [ ] Add 4 photos using "Add Photo" button multiple times
- [ ] Add unique captions for each photo:
  - Photo 1: "Overview of damaged area"
  - Photo 2: "Close-up of corrosion"
  - Photo 3: "Serial number plate"
  - Photo 4: "Surrounding equipment"
- [ ] Verify all 4 photos and captions appear in admin view
- [ ] Download document - verify all 4 photos embedded

### Photo Upload - Maximum Limit
- [ ] Attempt to add 7 photos (max is 6)
- [ ] Verify system handles gracefully (either prevents 7th upload or shows error)

### Photo Upload - Format Validation
- [ ] Test JPEG upload - should succeed
- [ ] Test PNG upload - should succeed
- [ ] Test HEIC upload (iPhone) - should succeed and auto-convert to JPEG
- [ ] Test invalid format (PDF, TXT) - should reject

### Photo Upload - Size Validation
- [ ] Upload very large photo (>16MB)
- [ ] Verify error message or rejection
- [ ] Verify photo auto-resizes to 576px width maximum

### Update Existing Work Item
- [ ] Login as crew member
- [ ] Verify "Your Assigned Items" section shows assigned items
- [ ] Click "Load & Edit This Item" button
- [ ] Verify form populates with existing data
- [ ] Modify description field
- [ ] Add 1 additional photo
- [ ] Submit form
- [ ] Verify admin dashboard shows updated data
- [ ] Verify both original and new photos appear

---

## 3. Mobile UI Testing

### iPhone Safari Testing
- [ ] Open application on iPhone Safari
- [ ] Test crew login flow
- [ ] Test form filling (verify large touch-friendly inputs)
- [ ] Test photo upload from camera:
  - Click file input
  - Select "Take Photo"
  - Take photo with camera
  - Verify HEIC format auto-converts to JPEG
- [ ] Test photo upload from photo library
- [ ] Verify all buttons are touch-friendly (minimum 44x44pt)
- [ ] Test landscape and portrait orientations
- [ ] Verify responsive layout (no horizontal scrolling)
- [ ] Test form submission
- [ ] Test assigned items loading

### Android Chrome Testing
- [ ] Open application on Android Chrome
- [ ] Test crew login flow
- [ ] Test form filling
- [ ] Test photo upload from camera:
  - Click file input
  - Select "Camera"
  - Take photo
  - Verify upload succeeds
- [ ] Test photo upload from gallery
- [ ] Verify responsive layout
- [ ] Test form submission
- [ ] Test assigned items loading
- [ ] Verify no layout issues

### Desktop Responsive Testing
- [ ] Open application on desktop browser
- [ ] Resize browser window to mobile width (375px)
- [ ] Verify layout adapts correctly
- [ ] Test at tablet width (768px)
- [ ] Test at desktop width (1200px+)

---

## 4. Assignment Workflow (Admin Interface)

### Assign Work Item
- [ ] Login as admin
- [ ] Navigate to dashboard
- [ ] Click "View" on any submitted work item
- [ ] Select crew member from "Assign to" dropdown (e.g., "DP")
- [ ] Select status "Needs Revision"
- [ ] Add revision notes: "Please add 2 more photos showing the damaged area from different angles"
- [ ] Click "Save Changes"
- [ ] Verify status changes to "Needs Revision"
- [ ] Verify assigned_to shows "DP"
- [ ] Verify revision notes saved

### Crew Receives Assignment
- [ ] Logout admin
- [ ] Login as assigned crew member (DP)
- [ ] Verify "Your Assigned Items" section shows the assigned item
- [ ] Verify status badge shows "Needs Revision"
- [ ] Verify revision notes display in alert box
- [ ] Click "Load & Edit This Item"
- [ ] Verify alert shows revision notes
- [ ] Verify form populates with existing data

### Crew Edits and Resubmits
- [ ] As crew member, edit the loaded item
- [ ] Add 2 new photos as requested
- [ ] Update detail field with additional information
- [ ] Submit form
- [ ] Verify success page
- [ ] Verify item now shows updated photos and data

### Admin Reviews Resubmission
- [ ] Login as admin
- [ ] View the resubmitted item
- [ ] Verify new photos are present
- [ ] Change status to "In Review by DP"
- [ ] Clear revision notes
- [ ] Save changes
- [ ] Verify status history shows progression

### Status Workflow Progression
Test complete status progression:
- [ ] Create new item (status: "Submitted")
- [ ] Assign and change status to "In Review by DP"
- [ ] Change status to "In Review by AL"
- [ ] Change status to "Awaiting Photos"
- [ ] Add photos and change to "Completed Review"
- [ ] Verify status history table shows all changes with timestamps

---

## 5. Admin Notes & Comments

### Create Revision Notes
- [ ] Login as admin
- [ ] View any work item
- [ ] Add revision notes in textarea: "Please clarify the location - specify which deck and frame number"
- [ ] Change status to "Needs Revision"
- [ ] Save changes
- [ ] Verify notes saved
- [ ] Reload page - verify notes persist

### Edit Revision Notes
- [ ] View item with existing revision notes
- [ ] Modify notes: "Update: Add reference to MRC drawing 123-456"
- [ ] Save changes
- [ ] Verify updated notes display

### View Revision Notes (Crew Side)
- [ ] Login as crew member assigned to item with revision notes
- [ ] View assigned items section
- [ ] Verify revision notes display
- [ ] Click "Load & Edit This Item"
- [ ] Verify alert box shows revision notes
- [ ] Verify notes are clear and actionable

### Clear Revision Notes
- [ ] Login as admin
- [ ] View item with revision notes
- [ ] Clear notes textarea (delete all text)
- [ ] Change status to "Completed Review"
- [ ] Save changes
- [ ] Verify notes are cleared

---

## 6. Document Generation

### Generate Single Document
- [ ] Login as admin
- [ ] View work item with 3-4 photos
- [ ] Click "Download Document (.docx)" button
- [ ] Verify .docx file downloads
- [ ] Open document in Microsoft Word or Google Docs
- [ ] Verify document contains:
  - Title: "WORK ITEM DRAFT TEMPLATE"
  - Item NO: [item_number]
  - Location, NS Equipment, Description, Detail, References
  - All 3-4 photos embedded at 4 inches wide
  - Photo captions in italics below each photo
  - Footer: "Submitted by [name] | Date [timestamp]"

### Generate Document - Photo Quality
- [ ] Open generated document
- [ ] Verify photos are clear and readable
- [ ] Verify photos are properly sized (4 inches wide)
- [ ] Verify photos maintain aspect ratio
- [ ] Verify no pixelation or distortion

### Generate Document - No Photos
- [ ] Generate document for item without photos
- [ ] Verify document generates successfully
- [ ] Verify "PHOTOS:" section is absent or empty
- [ ] Verify all other sections present

### Batch Download (ZIP)
- [ ] Login as admin
- [ ] Navigate to dashboard
- [ ] Select checkboxes for 3-5 work items
- [ ] Click "Batch Download Selected" button
- [ ] Verify ZIP file downloads (`work_items_batch.zip`)
- [ ] Extract ZIP file
- [ ] Verify correct number of .docx files present
- [ ] Open each .docx file and verify content
- [ ] Verify filenames follow pattern: `{item_number}_{description}.docx`

### Batch Download - All Items
- [ ] Select "Select All" checkbox
- [ ] Verify all items are checked
- [ ] Click "Batch Download Selected"
- [ ] Verify ZIP downloads with all items
- [ ] Verify file count matches dashboard item count

---

## 7. Photo Management (Admin)

### View Photos
- [ ] Login as admin
- [ ] View work item with multiple photos
- [ ] Verify photos display in grid layout
- [ ] Verify captions display below each photo
- [ ] Verify photos are clickable/viewable

### Edit Photo Captions
- [ ] Click "Edit" button on photo caption
- [ ] Modify caption: "Updated caption text"
- [ ] Save changes
- [ ] Verify caption updates in view
- [ ] Download document - verify new caption appears

### Download Single Photo
- [ ] Click "Download" button on specific photo
- [ ] Verify photo downloads with correct filename
- [ ] Verify downloaded photo is processed version (max 576px width)

### Delete Photo
- [ ] Click "Delete" button on specific photo
- [ ] Verify confirmation prompt appears
- [ ] Confirm deletion
- [ ] Verify photo removed from item
- [ ] Verify file deleted from uploads folder (admin can check)
- [ ] Download document - verify deleted photo not included

### Add Photos to Existing Item
- [ ] View item with 2 photos
- [ ] Scroll to "Add New Photos" section
- [ ] Upload 2 additional photos with captions
- [ ] Save changes
- [ ] Verify all 4 photos now display
- [ ] Download document - verify all 4 photos embedded

---

## 8. Admin Dashboard Features

### Filter by Status
- [ ] Login as admin
- [ ] Verify dashboard shows all work items
- [ ] Select "Submitted" from status filter dropdown
- [ ] Verify only submitted items display
- [ ] Test each status filter option:
  - All Statuses (default)
  - Submitted
  - In Review by DP
  - In Review by AL
  - Needs Revision
  - Awaiting Photos
  - Completed Review

### Filter by Assigned User
- [ ] Select specific crew member from "Assigned to" filter
- [ ] Verify only items assigned to that crew member display
- [ ] Test "All Users" option - verify all items display

### Sort Items
- [ ] Test sorting by:
  - Newest first (submitted_at DESC)
  - Oldest first (submitted_at ASC)
  - Item number A-Z
  - Item number Z-A

### Search Functionality (if implemented)
- [ ] Enter search term in search box
- [ ] Verify results filter correctly
- [ ] Test searching by:
  - Item number
  - Location
  - Description
  - Submitter name

### View Item Details
- [ ] Click "View" button on any item
- [ ] Verify full item details display
- [ ] Verify photos display
- [ ] Verify status history table displays
- [ ] Verify edit form is accessible

### Delete Work Item
- [ ] Click "Delete" button on test item
- [ ] Verify confirmation prompt
- [ ] Confirm deletion
- [ ] Verify item removed from dashboard
- [ ] Verify associated photos deleted
- [ ] Verify database record removed

---

## 9. SMS Notification Testing (When Implemented)

**Note:** SMS notifications are currently not implemented. These tests should be run once Twilio integration is added.

### Prerequisites
- [ ] Set environment variable `ENABLE_NOTIFICATIONS=True`
- [ ] Configure Twilio credentials in environment
- [ ] Add crew member phone numbers to config

### Assignment Notification
- [ ] Assign work item to crew member
- [ ] Verify SMS sent to crew member's phone
- [ ] Verify SMS contains:
  - Item number
  - Status
  - Revision notes (if applicable)
  - Link to login page

### Test All Crew Members (6 crew members)
- [ ] Assign items to each crew member (DP, AL, Kaitlyn, Mark, Art, D2)
- [ ] Verify each receives SMS notification
- [ ] Verify phone numbers are correct
- [ ] Verify message formatting is correct

### Status Change Notification
- [ ] Change status to "Needs Revision"
- [ ] Verify assigned crew member receives SMS
- [ ] Change status to "Completed Review"
- [ ] Verify notification sent (if configured)

### Notification Failure Handling
- [ ] Test with invalid phone number
- [ ] Verify application handles error gracefully
- [ ] Verify error logged (check logs)
- [ ] Verify work item still updates even if SMS fails

---

## 10. Railway Production Deployment Validation

### Pre-Deployment Checklist
- [ ] Verify all environment variables set in Railway:
  - `DATABASE_URL` (PostgreSQL)
  - `SECRET_KEY` (random string)
  - `ADMIN_USERNAME` (change from default)
  - `ADMIN_PASSWORD` (change from default)
  - `CREW_PASSWORD` (change from default)
  - `ENABLE_NOTIFICATIONS` (if using)
  - Twilio credentials (if using SMS)
- [ ] Verify requirements.txt includes all dependencies
- [ ] Verify railway.json or Procfile configured correctly

### Deployment Process
- [ ] Push code to GitHub repository
- [ ] Connect Railway to GitHub repository
- [ ] Trigger deployment
- [ ] Monitor build logs for errors
- [ ] Verify deployment succeeds

### Post-Deployment Validation
- [ ] Access application URL (https://your-app.railway.app)
- [ ] Verify HTTPS connection (secure)
- [ ] Verify no console errors in browser DevTools
- [ ] Test crew login with production credentials
- [ ] Test admin login with production credentials
- [ ] Create test work item
- [ ] Upload photo from mobile device
- [ ] Assign work item
- [ ] Generate document
- [ ] Test on both iPhone and Android devices

### Database Migration (SQLite to PostgreSQL)
- [ ] Verify PostgreSQL database created in Railway
- [ ] Verify tables auto-created on first run (db.create_all())
- [ ] Test creating work items in production
- [ ] Verify data persists after deployment restart
- [ ] Test photo uploads (verify file storage persists)

### Performance Testing
- [ ] Test page load times (should be <3 seconds)
- [ ] Upload large photo (test file size limits)
- [ ] Generate document with 6 photos (test generation time)
- [ ] Batch download 10+ items (test ZIP generation)
- [ ] Test concurrent users (have 2-3 people use simultaneously)

### Production Data Validation
- [ ] Verify uploads folder created and writable
- [ ] Verify generated_docs folder created and writable
- [ ] Verify file permissions correct
- [ ] Test file cleanup (delete photos, verify files removed)

### Error Handling
- [ ] Test 404 error (access non-existent page)
- [ ] Test 500 error (trigger database error if possible)
- [ ] Verify error pages display correctly
- [ ] Verify errors logged (check Railway logs)

### Security Testing
- [ ] Verify SQL injection prevention (try malicious input in forms)
- [ ] Verify XSS prevention (try script tags in text fields)
- [ ] Test CSRF protection (if implemented)
- [ ] Verify file upload restrictions (try uploading .exe, .php files)
- [ ] Verify authentication required for protected pages
- [ ] Test session hijacking protection

### Monitoring & Logging
- [ ] Check Railway logs for application errors
- [ ] Verify all routes logging correctly
- [ ] Test error scenarios and verify logging
- [ ] Set up uptime monitoring (optional: UptimeRobot, Pingdom)

---

## 11. Edge Cases & Error Handling

### Form Validation
- [ ] Submit form with missing required fields
- [ ] Verify error messages display
- [ ] Submit form with extremely long text (>500 chars in description)
- [ ] Verify handling of special characters (<, >, &, quotes)

### File Upload Edge Cases
- [ ] Upload photo with no file selected
- [ ] Upload photo with very long filename (>200 chars)
- [ ] Upload photo with special characters in filename
- [ ] Upload corrupted image file
- [ ] Test rapid consecutive uploads

### Database Edge Cases
- [ ] Create 100+ work items (test pagination if implemented)
- [ ] Create item with all optional fields empty
- [ ] Test concurrent edits (2 admins editing same item)
- [ ] Test database connection failure (temporarily stop DB)

### Network Issues
- [ ] Test form submission with slow network (throttle to 3G)
- [ ] Test photo upload with network interruption
- [ ] Test download with network interruption
- [ ] Verify appropriate error messages

---

## 12. Regression Testing (Run Before Each Release)

Quick regression test checklist for rapid validation:

- [ ] Crew login → Submit item with 2 photos → Success
- [ ] Admin login → View item → Assign to crew → Add notes → Save
- [ ] Crew login (assigned) → Load assigned item → Edit → Resubmit
- [ ] Admin login → Change status → Download document → Verify
- [ ] Admin → Select 3 items → Batch download → Verify ZIP
- [ ] Mobile (iPhone) → Login → Submit with camera photo → Success
- [ ] Mobile (Android) → Login → Submit with camera photo → Success
- [ ] Production → Full workflow → End-to-end test

---

## Test Results Template

Use this template to track testing results:

```
Test Date: ___________
Tester Name: ___________
Environment: [ ] Local [ ] Railway Production
Device: ___________
Browser: ___________

| Section | Pass | Fail | Notes |
|---------|------|------|-------|
| 1. Authentication | ☐ | ☐ | |
| 2. Work Item Submission | ☐ | ☐ | |
| 3. Mobile UI | ☐ | ☐ | |
| 4. Assignment Workflow | ☐ | ☐ | |
| 5. Admin Notes | ☐ | ☐ | |
| 6. Document Generation | ☐ | ☐ | |
| 7. Photo Management | ☐ | ☐ | |
| 8. Admin Dashboard | ☐ | ☐ | |
| 9. SMS Notifications | ☐ | ☐ | N/A (not implemented) |
| 10. Railway Deployment | ☐ | ☐ | |
| 11. Edge Cases | ☐ | ☐ | |
| 12. Regression | ☐ | ☐ | |

Critical Bugs Found:
1. ___________
2. ___________

Minor Issues:
1. ___________
2. ___________

Overall Result: [ ] PASS [ ] FAIL
Production Ready: [ ] YES [ ] NO
```

---

## Approval Sign-Off

Before production deployment, all critical tests must pass.

- [ ] All critical functionality tested and passing
- [ ] Mobile UI tested on iPhone Safari
- [ ] Mobile UI tested on Android Chrome
- [ ] Railway deployment tested and validated
- [ ] Security testing passed
- [ ] Performance acceptable (<3 second page loads)
- [ ] Photo upload from mobile camera working
- [ ] Document generation with 3-4 photos working
- [ ] Assignment workflow end-to-end tested
- [ ] No critical bugs remaining

**Tested By:** _____________________ **Date:** _________

**Approved By:** _____________________ **Date:** _________

---

## Notes
- Keep this checklist updated as new features are added
- Report all bugs in GitHub Issues or project management tool
- Document any deviations from expected behavior
- Take screenshots of bugs for easier debugging
- Test frequently on mobile devices throughout development
