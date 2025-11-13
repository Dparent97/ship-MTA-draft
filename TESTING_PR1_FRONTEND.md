# Frontend Modernization Testing Checklist - PR #1

**PR URL:** https://github.com/Dparent97/ship-MTA-draft/pull/1  
**Branch:** `frontend-development` → `main`  
**Version:** 2.0.0  
**Test Date:** _____________  
**Tester:** _____________

---

## 🎯 Critical Bug Fixes (Test First!)

### ✅ Bug Fix #1: Photo Preview in Admin Dashboard

**Issue:** Photos were not displaying in admin dashboard cards  
**Fix:** Changed route from `admin.serve_upload` to `serve_upload`

- [ ] **TEST 1.1:** Navigate to admin dashboard
  - **Expected:** All work items with photos display thumbnail images
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 1.2:** Click on a work item card with photos
  - **Expected:** Full-size photos are visible in detail view
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 1.3:** Check photo count badge on cards
  - **Expected:** Badge shows correct number of photos (e.g., "3" if 3 photos)
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### ✅ Bug Fix #2: Dark Mode Removal

**Issue:** App was switching to dark mode based on system preferences  
**Fix:** Removed `@media (prefers-color-scheme: dark)` from variables.css

- [ ] **TEST 2.1:** Access app with system in Dark Mode
  - **Expected:** App stays in light mode with white backgrounds
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 2.2:** Toggle system dark mode while app is open
  - **Expected:** No visual changes to app (stays light)
  - **Actual:** _______________
  - **Status:** PASS / FAIL

---

## 🔐 Login Pages

### Crew Login (`/crew/login`)

- [ ] **TEST 3.1:** Page loads correctly
  - **Expected:** Centered card with ship icon, title "Crew Login"
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 3.2:** Crew name dropdown
  - **Expected:** Dropdown shows all crew members, large touch target (48px+)
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 3.3:** Password visibility toggle
  - **Expected:** Eye icon button toggles password visibility on/off
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 3.4:** Successful login
  - **Expected:** Redirects to crew dashboard after correct credentials
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 3.5:** Failed login
  - **Expected:** Error message displays clearly
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Admin Login (`/admin/login`)

- [ ] **TEST 4.1:** Page loads correctly
  - **Expected:** Centered card with admin icon, title "Admin Login"
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 4.2:** Username input
  - **Expected:** Large input field with icon, 48px height
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 4.3:** Password visibility toggle
  - **Expected:** Eye icon button toggles password visibility on/off
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 4.4:** Successful login
  - **Expected:** Redirects to admin dashboard (username: admin, password: admin67)
  - **Actual:** _______________
  - **Status:** PASS / FAIL

---

## 📊 Admin Dashboard

### Layout & Design

- [ ] **TEST 5.1:** Card grid layout
  - **Expected:** 3 columns on desktop (1024px+), 2 on tablet (768px), 1 on mobile
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 5.2:** Work item cards display correctly
  - **Expected:** Each card shows item number, status badge, photo thumbnail, description
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 5.3:** Status badges color-coded
  - **Expected:**
    - Submitted: Blue
    - In Review: Yellow
    - Needs Revision: Red
    - Awaiting Photos: Cyan
    - Completed: Green
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 5.4:** Photo thumbnails lazy load
  - **Expected:** Photos load as you scroll, no lag
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Filters & Search

- [ ] **TEST 6.1:** Status filter dropdown
  - **Expected:** Filters work items by status, updates view immediately
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 6.2:** Sort dropdown
  - **Expected:** Sorts by newest, oldest, item number, submitter
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 6.3:** Search input
  - **Expected:** Searches across item numbers, descriptions, locations
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Batch Actions

- [ ] **TEST 7.1:** Select all checkbox
  - **Expected:** Checks/unchecks all visible work items
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 7.2:** Individual item selection
  - **Expected:** Can select/deselect individual cards
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 7.3:** Selected count badge
  - **Expected:** Shows "X selected" count updates in real-time
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 7.4:** Download batch button
  - **Expected:** Downloads .zip file with selected work item DOCXs
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 7.5:** Download button disabled state
  - **Expected:** Button disabled when 0 items selected, enabled when 1+
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Toast Notifications

- [ ] **TEST 8.1:** Action success toast
  - **Expected:** Green toast appears for successful actions (e.g., batch download)
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 8.2:** Toast auto-dismisses
  - **Expected:** Toast disappears after ~4 seconds
  - **Actual:** _______________
  - **Status:** PASS / FAIL

---

## 📝 Crew Dashboard & Form

### Tab Navigation

- [ ] **TEST 9.1:** "Submit New" tab
  - **Expected:** Shows new work item submission form
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 9.2:** "In Progress" tab
  - **Expected:** Shows work items in draft/submitted status
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 9.3:** "Completed" tab
  - **Expected:** Shows completed work items
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 9.4:** Tab switching
  - **Expected:** Smooth transition between tabs, no page reload
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Assigned Items Banner

- [ ] **TEST 10.1:** Banner displays for assigned items
  - **Expected:** Yellow banner shows when admin assigns item back for revision
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 10.2:** Revision notes visible
  - **Expected:** Admin's revision notes clearly displayed in banner
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Form Submission

- [ ] **TEST 11.1:** All form fields present
  - **Expected:** Location, description, detail, operator furnished material fields
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 11.2:** Form validation
  - **Expected:** Required fields show errors if empty on submit
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 11.3:** Successful submission
  - **Expected:** Success message, redirects to view/edit page
  - **Actual:** _______________
  - **Status:** PASS / FAIL

---

## 📷 Photo Upload System

### Drag & Drop

- [ ] **TEST 12.1:** Drop zone displays correctly
  - **Expected:** Dashed border box with upload icon, "Drag & Drop Photos Here" text
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 12.2:** Drag over effect
  - **Expected:** Drop zone highlights when dragging files over it
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 12.3:** Drop to upload
  - **Expected:** Dragging and dropping image files starts upload
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 12.4:** Multiple file drop
  - **Expected:** Can drag and drop multiple images at once
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### File Selection (Mobile/Desktop)

- [ ] **TEST 13.1:** "Choose Photos" button
  - **Expected:** Opens file picker dialog
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 13.2:** Camera access (mobile only)
  - **Expected:** Option to take photo with camera appears on mobile
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 13.3:** Photo library access (mobile only)
  - **Expected:** Can select from photo library
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Photo Preview

- [ ] **TEST 14.1:** Loading state
  - **Expected:** Spinner shows while photo is loading
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 14.2:** Instant preview
  - **Expected:** Photo preview appears within 1 second of selection
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 14.3:** Preview card layout
  - **Expected:** Card shows thumbnail, filename, file size
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 14.4:** Multiple previews
  - **Expected:** All selected photos show as separate preview cards
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Photo Management

- [ ] **TEST 15.1:** Caption input
  - **Expected:** Can type caption for each photo in preview card
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 15.2:** Delete button
  - **Expected:** Trash icon button appears on each preview card
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 15.3:** Delete functionality
  - **Expected:** Clicking delete removes photo with smooth animation
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 15.4:** File size display
  - **Expected:** Shows file size in KB or MB (e.g., "2.3 MB")
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Validation

- [ ] **TEST 16.1:** File type validation
  - **Expected:** Only accepts JPG, PNG, HEIC (error toast for other types)
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 16.2:** File size validation
  - **Expected:** Rejects files over 10MB with error toast
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 16.3:** Max photo limit
  - **Expected:** Cannot add more than 10 photos, button shows "Maximum 10 photos reached"
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 16.4:** Error toast notifications
  - **Expected:** Clear error messages for validation failures
  - **Actual:** _______________
  - **Status:** PASS / FAIL

---

## 📱 Mobile Responsiveness

### iPhone SE (320px)

- [ ] **TEST 17.1:** Login page
  - **Expected:** Card fits screen, buttons are tappable (44px+)
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 17.2:** Admin dashboard
  - **Expected:** Cards stack vertically, no horizontal scroll
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 17.3:** Crew form
  - **Expected:** All fields visible, no text cutoff
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 17.4:** Photo upload
  - **Expected:** Drop zone and previews fit screen width
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### iPhone 12/13 (375px)

- [ ] **TEST 18.1:** Navigation works smoothly
  - **Expected:** All menus and buttons accessible
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 18.2:** Card layouts responsive
  - **Expected:** Cards have proper spacing, not cramped
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### iPad (768px)

- [ ] **TEST 19.1:** Dashboard shows 2-column grid
  - **Expected:** Admin dashboard shows 2 cards per row
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 19.2:** Forms utilize screen width
  - **Expected:** Form fields sized appropriately, not stretched
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Desktop (1024px+)

- [ ] **TEST 20.1:** Dashboard shows 3-column grid
  - **Expected:** Admin dashboard shows 3 cards per row
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 20.2:** Drag-and-drop works
  - **Expected:** Can drag files from desktop to drop zone
  - **Actual:** _______________
  - **Status:** PASS / FAIL

---

## 🌐 Browser Compatibility

### Safari (iOS) - PRIMARY

- [ ] **TEST 21.1:** All features work
  - **Expected:** No console errors, all interactions smooth
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 21.2:** Photo upload from camera
  - **Expected:** Camera opens, photo captures and uploads
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Chrome (Android) - PRIMARY

- [ ] **TEST 22.1:** All features work
  - **Expected:** No console errors, all interactions smooth
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 22.2:** Photo upload from camera
  - **Expected:** Camera opens, photo captures and uploads
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Chrome (Desktop)

- [ ] **TEST 23.1:** Full functionality
  - **Expected:** All features work, responsive tools functional
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Safari (Desktop)

- [ ] **TEST 24.1:** Full functionality
  - **Expected:** All features work, no webkit-specific issues
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Firefox (Desktop)

- [ ] **TEST 25.1:** Full functionality
  - **Expected:** All features work, CSS variables render correctly
  - **Actual:** _______________
  - **Status:** PASS / FAIL

---

## 🔧 Developer Console

### JavaScript Errors

- [ ] **TEST 26.1:** No console errors on login pages
  - **Expected:** Clean console, no errors or warnings
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 26.2:** No console errors on dashboards
  - **Expected:** Clean console, no errors or warnings
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 26.3:** No console errors during photo upload
  - **Expected:** Clean console, no errors or warnings
  - **Actual:** _______________
  - **Status:** PASS / FAIL

### Network Requests

- [ ] **TEST 27.1:** All assets load successfully
  - **Expected:** CSS, JS, images all return 200 status
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 27.2:** Photo uploads complete
  - **Expected:** Upload requests return 200/201 status
  - **Actual:** _______________
  - **Status:** PASS / FAIL

---

## 🔄 Backward Compatibility

### Existing Data

- [ ] **TEST 28.1:** Old work items display correctly
  - **Expected:** All existing work items show properly with new design
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 28.2:** Old photos still accessible
  - **Expected:** All previously uploaded photos display correctly
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 28.3:** DOCX generation still works
  - **Expected:** Can generate and download DOCX files for work items
  - **Actual:** _______________
  - **Status:** PASS / FAIL

---

## 📈 Performance

### Load Times

- [ ] **TEST 29.1:** Login page loads < 2 seconds
  - **Expected:** Fast initial load
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 29.2:** Dashboard loads < 3 seconds
  - **Expected:** Loads with 50+ work items without lag
  - **Actual:** _______________
  - **Status:** PASS / FAIL

- [ ] **TEST 29.3:** Photo upload preview < 1 second
  - **Expected:** Instant preview for images under 5MB
  - **Actual:** _______________
  - **Status:** PASS / FAIL

---

## ✅ Test Summary

**Total Tests:** 87  
**Passed:** _____  
**Failed:** _____  
**Skipped:** _____  

**Critical Issues Found:**
1. _______________
2. _______________
3. _______________

**Minor Issues Found:**
1. _______________
2. _______________
3. _______________

**Recommendation:**
- [ ] APPROVED - Ready to merge to main
- [ ] APPROVED WITH MINOR FIXES - Can merge after addressing minor issues
- [ ] REQUIRES FIXES - Must address critical issues before merge
- [ ] BLOCKED - Major issues prevent deployment

**Tester Signature:** _______________  
**Date Completed:** _______________

---

## 📝 Notes

Additional observations or comments:

_______________________________________________
_______________________________________________
_______________________________________________
_______________________________________________

