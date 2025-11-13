# Changelog

All notable changes to the Ship Maintenance Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-11-13

### Added

#### Design System Foundation
- **CSS Variables System** (`variables.css`) with PayPal-inspired color palette
  - Primary blues (#0070ba) and gold accents (#ffc439)
  - Semantic color system (success, warning, danger, info)
  - Consistent spacing scale (4px to 48px)
  - Typography scale (12px to 30px)
  - Shadow system (sm, md, lg, xl)
  - Border radius scale (4px to 12px)
  - Touch-friendly button heights (44px minimum for mobile accessibility)

#### Photo Upload System
- **Enhanced Photo Upload** (`photo-upload.js`) - 349-line JavaScript module
  - Drag-and-drop interface with visual feedback
  - Instant image previews before upload
  - Individual photo deletion with smooth animations
  - Photo captions with inline editing
  - File validation (type, size, max photos)
  - Loading states with spinners
  - Toast notifications for errors
  - File size display with auto-formatting (KB/MB)
  - Mobile-optimized touch targets

#### User Interface Improvements
- **Modernized Login Pages** (crew and admin)
  - Centered card layout with shadow effects
  - SVG icons throughout (person, lock, eye)
  - Password visibility toggle with eye icon button
  - Large touch targets (44px+ buttons) for mobile
  - Animated card entrance with subtle fade-in
  - Better visual hierarchy with proper spacing
  - Mobile-responsive (works on 320px+ screens)

- **Card-Based Admin Dashboard**
  - Responsive 3-column grid layout (stacks on mobile)
  - Photo thumbnails on each work item card
  - Batch selection with "select all" functionality
  - Enhanced filters (status, sort, search)
  - Color-coded status badges:
    - Submitted: Blue
    - In Review: Yellow
    - Needs Revision: Red
    - Awaiting Photos: Cyan
    - Completed: Green
  - Photo count indicators on cards
  - Toast notifications for actions
  - Lazy loading for photo thumbnails

- **Enhanced Crew Dashboard**
  - Tab-based navigation (Submit New, In Progress, Completed)
  - Assigned items banner for items needing revision
  - Improved form field grouping
  - Better photo preview sections
  - Revision notes display with clear formatting

#### Styling Enhancements
- Expanded `style.css` from ~200 to 750+ lines
- Modern button system (primary, secondary, success, danger, etc.)
- Consistent card components with hover effects
- Improved form controls with better focus states
- Toast notification system
- Photo upload UI (drop zones, preview cards)
- Work item card grid with hover effects
- Loading states and spinners
- Responsive breakpoints for mobile/tablet/desktop

### Changed
- Updated backend routes in `admin.py` for enhanced functionality
  - Added `search_query` parameter to dashboard
  - Enhanced work item filtering capabilities

### Fixed
- **Critical: Photo Preview Bug** - Fixed photo route in admin dashboard
  - Changed from `admin.serve_upload` to `serve_upload`
  - Photos now display correctly across all templates
  - Ensured consistent photo URL routing
  
- **Critical: Dark Mode Removal** - Removed automatic dark mode activation
  - Deleted `@media (prefers-color-scheme: dark)` query from `variables.css`
  - App now stays in light mode regardless of system preferences
  - Improved consistency for crew working in various lighting conditions

### Technical Details
- **Files Modified:** 12 files
- **Lines Added:** 1,487
- **Lines Removed:** 336
- **New Files:**
  - `app/static/css/variables.css` (132 lines)
  - `app/static/js/photo-upload.js` (349 lines)
  - `test_photo_upload.html` (132 lines)

### Commits Included
1. `c6737bb` - Add design system foundation with PayPal-inspired colors
2. `126d910` - Improve crew dashboard with modern card-based design
3. `b158069` - Modernize admin dashboard with card grid layout and enhanced features
4. `9e86d0a` - Modernize crew and admin login pages
5. `cfc0cab` - Enhance photo upload UX with drag-and-drop and instant previews
6. `cb9f24e` - Merge design system foundation
7. `cb66a1f` - Merge modernized login pages
8. `be28780` - Merge improved crew dashboard
9. `be8850b` - Merge enhanced photo upload UX
10. `04c0c8c` - Merge modernized admin dashboard
11. `95d0dd9` - Fix photo preview and remove dark mode

### Migration Notes
- No database migrations required
- Backward compatible with existing data
- No breaking changes to existing functionality
- All routes and endpoints remain the same

### Testing Recommendations
- Verify photo display in admin dashboard cards
- Confirm dark mode no longer activates with system preferences
- Test drag-and-drop photo upload on desktop and mobile
- Verify responsive behavior on iPhone SE (320px), iPhone 12/13 (375px), iPad (768px)
- Test all login flows (crew and admin)
- Verify batch selection and download functionality

---

## [1.0.0] - 2024-XX-XX

### Added
- Initial release of Ship Maintenance Tracker
- Crew work item submission system
- Admin review and approval workflow
- Photo attachment support with HEIC conversion
- DOCX document generation for drydock submissions
- Status tracking (Draft, Submitted, In Review, Needs Revision, etc.)
- Comment system for admin feedback
- PostgreSQL database integration
- Railway.app deployment configuration

[2.0.0]: https://github.com/Dparent97/ship-MTA-draft/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/Dparent97/ship-MTA-draft/releases/tag/v1.0.0

