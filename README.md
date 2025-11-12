# Arrowhead MTA 26

A mobile-first web application for managing Arrowhead Maintenance Availability 2026 work item documentation.

## 🚀 Quick Start

### 1. Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py
```

### 2. Access the App
- Open browser: `http://localhost:5001`
- **Crew Login:** Password: `crew2026`
- **Admin Login:** Username: `admin`, Password: `admin2026`

> **Note:** Port changed to 5001 due to macOS AirTunes using port 5000

## 👥 For Junior Engineers

This project includes comprehensive documentation designed for junior engineers:

### Quick Start Workflow
1. **Read this README** to understand the project
2. **Review `ENGINEER_TASKS.md`** to see available tasks
3. **Pick a task** based on your skill level (⭐ Easy, ⭐⭐ Medium, ⭐⭐⭐ Hard)
4. **Follow the task instructions** including testing requirements
5. **Use `TESTING_CHECKLIST.md`** to verify your changes
6. **Submit for code review** when complete

### Task Priority Guide
- 🔴 **Critical**: Must be done before deployment
- 🟡 **High**: Important for production readiness
- 🟢 **Medium**: Nice to have, improves UX
- 🔵 **Low**: Future enhancements

### Getting Started
```bash
# 1. Set up development environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Pick a task from ENGINEER_TASKS.md
# Start with ⭐ Easy tasks if you're new to the codebase

# 3. Create a feature branch
git checkout -b feature/your-task-name

# 4. Make your changes and test
python run.py

# 5. Run relevant tests from TESTING_CHECKLIST.md

# 6. Commit and push
git add .
git commit -m "[Task ID] Your descriptive message"
git push origin feature/your-task-name
```

### Need Help?
- Check `ENGINEER_TASKS.md` for detailed task instructions
- Review `TESTING_CHECKLIST.md` for testing guidance
- Search error messages on Stack Overflow
- Ask teammates if stuck > 30 minutes

## 📋 What's Included

### Core Files
- `SHIP_MAINTENANCE_APP_BUILD_GUIDE.md` - Complete build instructions
- `TESTING_CHECKLIST.md` - Comprehensive testing scenarios for QA
- `ENGINEER_TASKS.md` - Task breakdown for development team
- `requirements.txt` - Python dependencies
- `run.py` - Application entry point
- `config.py` - Configuration settings

### Templates
- `admin_login.html` - Admin authentication
- `admin_view_item.html` - View work item details
- Additional templates in `/app/templates/` (see build guide)

## 📁 Project Structure

```
ship-maintenance-tracker/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── auth.py
│   ├── crew.py
│   ├── admin.py
│   ├── docx_generator.py
│   ├── utils.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/main.js
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── crew_form.html
│       ├── crew_success.html
│       ├── admin_login.html
│       ├── admin_dashboard.html
│       └── admin_view_item.html
├── uploads/
├── generated_docs/
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## 🔨 Build Instructions

For complete step-by-step build instructions, see:
**`SHIP_MAINTENANCE_APP_BUILD_GUIDE.md`**

This guide includes:
- Detailed implementation phases
- Complete code for all files
- Deployment instructions
- Troubleshooting tips
- Testing checklist

## 🌐 Production Deployment

### Railway Deployment (Recommended)

Railway is the recommended hosting platform for this application. The free tier is sufficient for the expected usage (6 users, 60-70 work items, ~50MB photo storage).

#### Prerequisites
- Railway account (https://railway.app)
- Twilio account for SMS notifications (https://www.twilio.com)
- GitHub repository connected to Railway

#### Step 1: Environment Configuration

Set the following environment variables in Railway dashboard:

```bash
# Application Settings
SECRET_KEY=<generate-random-32-char-string>
FLASK_ENV=production

# Database (Railway provides automatically if using their PostgreSQL)
DATABASE_URL=<auto-provided-or-use-sqlite>

# Twilio SMS Configuration (REQUIRED)
TWILIO_ACCOUNT_SID=<your-twilio-account-sid>
TWILIO_AUTH_TOKEN=<your-twilio-auth-token>
TWILIO_PHONE_NUMBER=<your-twilio-number-with-country-code>

# Optional: Admin Credentials (if not using default)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<change-in-production>
```

#### Step 2: Deploy to Railway

```bash
# Option 1: Using Railway CLI
railway login
railway init
railway up

# Option 2: Using GitHub Integration (Recommended)
1. Go to Railway dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect and deploy
```

#### Step 3: Configure Start Command

In Railway dashboard, set the start command:
```bash
gunicorn run:app --bind 0.0.0.0:$PORT
```

Or add a `Procfile` to your repository:
```
web: gunicorn run:app --bind 0.0.0.0:$PORT
```

#### Step 4: Initial Database Setup

After deployment, run the initialization script:
```bash
# Using Railway CLI
railway run python scripts/init_db.py

# Or via Railway shell in dashboard
```

#### Step 5: Verify Deployment

1. Access your Railway app URL (e.g., `https://your-app.up.railway.app`)
2. Test admin login
3. Create a test work item
4. Upload a test photo
5. Send a test SMS notification
6. Generate a test document

### Deployment Checklist

Before going live, complete these steps:

- [ ] All environment variables configured
- [ ] Twilio account verified and phone numbers loaded
- [ ] Database initialized with crew member data
- [ ] Admin and crew accounts created
- [ ] SMS notifications tested with all 6 crew members
- [ ] Photo upload tested from iPhone and Android
- [ ] Document generation tested with 3-4 photos
- [ ] Railway health monitoring enabled
- [ ] All tests from `TESTING_CHECKLIST.md` passed
- [ ] Credentials shared securely with team

### Alternative: Render Deployment

If using Render instead of Railway:
1. Connect your GitHub repo
2. Set environment variables in Render dashboard
3. Deploy directly from dashboard
4. Configure persistent disk for SQLite database
5. Follow similar verification steps as Railway

### Monitoring and Maintenance

#### Railway Dashboard Access
- **Metrics**: View CPU, memory, and bandwidth usage
- **Logs**: Real-time application logs
- **Deployments**: Rollback if needed
- **Environment Variables**: Update settings without redeploying

#### Application Monitoring
- Health check endpoint: `/health`
- View logs: `railway logs` (CLI) or via dashboard
- Error tracking: Check Railway dashboard for errors
- Twilio logs: https://www.twilio.com/console/sms/logs

#### Daily/Weekly Checks
- Monitor Railway usage (free tier limits)
- Check SMS delivery success rate in Twilio dashboard
- Review application logs for errors
- Verify photo storage size (target: ~50MB for 60 days)
- Test work item creation and submission weekly

### Scale Considerations

This application is designed for:
- **Users**: 6 crew members + 1 admin
- **Duration**: 60-day deployment
- **Work Items**: 60-70 expected
- **Photos**: 3-4 per item (~240 total, ~50MB)
- **Database**: SQLite is sufficient for this scale
- **Hosting**: Railway free tier should suffice (willing to upgrade if needed)

If usage exceeds these limits:
- Railway will notify you of usage limits
- Upgrade to Railway paid plan (~$5-20/month)
- Consider migrating SQLite to PostgreSQL for better concurrent access

### Cost Estimate

**Monthly costs for production**:
- Railway: $0 (free tier) or ~$5-10 if upgraded
- Twilio: ~$1/month for phone number + $0.0075 per SMS
  - Expected SMS: ~70 assignments = ~$0.53 for SMS
  - **Total Twilio**: ~$1.50/month
- **Total estimated cost**: $1.50 - $12/month

### Backup and Data Export

#### Manual Backup (SQLite)
```bash
# Download database from Railway
railway run sqlite3 maintenance.db ".backup backup.db"

# Or use Railway's file system access to download maintenance.db
```

#### Export Work Items
- Use the bulk export feature to generate PDFs
- Download all documents as ZIP file
- Store in secure location for records

### Security Considerations

**Note**: Password security is not a priority for this short-term deployment, but basic precautions are recommended:

- [ ] Change default admin password
- [ ] Use HTTPS (Railway provides automatically)
- [ ] Don't commit secrets to Git (use .env files)
- [ ] Restrict Railway dashboard access
- [ ] Use secure method to share credentials (not email)

### Troubleshooting Production Issues

#### SMS Not Sending
1. Check Twilio credentials in Railway environment variables
2. Verify Twilio account has sufficient balance
3. Check phone numbers are in E.164 format (+1234567890)
4. Review Twilio logs for delivery failures
5. Test with Twilio's SMS test tool

#### Photos Not Uploading
1. Check Railway disk usage
2. Verify file permissions in Railway environment
3. Test with smaller photo first
4. Check browser console for errors
5. Try different browser or device

#### Slow Performance
1. Check Railway metrics (CPU/memory)
2. Review application logs for errors
3. Consider upgrading Railway plan
4. Optimize photo sizes if needed
5. Check internet connection on mobile device

#### Database Issues
1. Check Railway logs for database errors
2. Verify DATABASE_URL environment variable
3. Consider migrating to PostgreSQL if SQLite issues persist
4. Download and inspect database file locally

### Rollback Procedure

If deployment fails or has critical issues:
```bash
# Using Railway CLI
railway rollback

# Or via Railway dashboard:
1. Go to Deployments tab
2. Find previous working deployment
3. Click "Rollback to this version"
```

### Support and Resources

- **Testing Documentation**: See `TESTING_CHECKLIST.md`
- **Engineer Tasks**: See `ENGINEER_TASKS.md` for development tasks
- **Build Guide**: See `SHIP_MAINTENANCE_APP_BUILD_GUIDE.md`
- **Railway Docs**: https://docs.railway.app/
- **Twilio Docs**: https://www.twilio.com/docs/sms
- **Flask Docs**: https://flask.palletsprojects.com/

## 📸 Features

### Core Functionality
- ✅ Mobile-optimized submission form
- ✅ Photo upload with auto-resize (4" width)
- ✅ Mobile camera integration (iPhone & Android)
- ✅ SMS notifications via Twilio (assignment alerts)
- ✅ Generates .docx files with embedded photos
- ✅ Admin dashboard with status tracking
- ✅ Batch download as .zip
- ✅ Admin notes system
- ✅ Work item assignment workflow

### Mobile Support
- ✅ Responsive design for small screens (320px+)
- ✅ Touch-friendly buttons (44x44px minimum)
- ✅ Works on iPhone Safari and Android Chrome
- ✅ Camera access from mobile browser
- ✅ Optimized for 3G/4G connections
- ✅ Photo preview before upload

### Production Features
- ✅ Railway deployment ready
- ✅ SQLite database (sufficient for 60-70 items)
- ✅ Photo storage (~50MB capacity)
- ✅ SMS delivery tracking
- ✅ Error logging and monitoring
- ✅ Health check endpoint

## 🔐 Security Notes

**IMPORTANT:** Change these defaults in production:
- `SECRET_KEY` in config.py
- `CREW_PASSWORD` in config.py
- `ADMIN_PASSWORD` in config.py

## 📱 Mobile Considerations

### Supported Devices
- **iPhone**: iOS 13+ with Safari browser
- **Android**: Android 8+ with Chrome browser
- **Screen sizes**: 320px (iPhone SE) to 768px+ (tablets)

### Mobile Testing Requirements
Before deployment, test these scenarios on real devices:

**iPhone Safari**:
- [ ] Login and navigation
- [ ] Photo upload from camera
- [ ] Photo upload from gallery
- [ ] Form submission
- [ ] Work item viewing
- [ ] Document download

**Android Chrome**:
- [ ] Login and navigation
- [ ] Photo upload from camera
- [ ] Photo upload from gallery
- [ ] Form submission
- [ ] Work item viewing
- [ ] Document download

### Mobile Network Considerations
- App is optimized for 3G/4G connections
- Photo compression reduces upload time
- Loading indicators show progress
- Graceful degradation on slow connections

### Camera Permissions
Users will be prompted to allow camera access on first photo upload:
- **iOS**: "Allow [App Name] to access the camera"
- **Android**: "Let [App Name] take pictures and record video"

Both permissions are required for photo upload functionality.

## 📝 Customization

### Update Crew Members
Edit `config.py` or load from `crew_data.csv`:
```python
CREW_MEMBERS = [
    'Your',
    'Crew',
    'Names',
    'Here'
]
```

For CSV format:
```csv
name,phone,role
John Doe,+11234567890,crew
Jane Smith,+11234567891,crew
```

### Adjust Photo Settings
Edit `config.py`:
```python
PHOTO_MAX_WIDTH = 576  # 4 inches at 144 DPI
PHOTO_MIN_COUNT = 2
PHOTO_MAX_COUNT = 6
```

### SMS Message Template
Edit in `services/sms.py`:
```python
message = f"New work item assigned: [{item_id}] {description}"
```

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Run `pip install -r requirements.txt`
2. **Database errors**: Delete `maintenance.db` and restart
3. **Port in use**: Change port in `run.py`
4. **Photos not uploading**: Check folder permissions

## 📚 Documentation

### Project Documentation
- **Build Guide**: `SHIP_MAINTENANCE_APP_BUILD_GUIDE.md` - Complete build instructions
- **Testing Checklist**: `TESTING_CHECKLIST.md` - Comprehensive manual testing scenarios
- **Engineer Tasks**: `ENGINEER_TASKS.md` - Task breakdown for junior engineers
- **README**: This file - Overview and deployment guide

### Testing Documentation

#### TESTING_CHECKLIST.md
Comprehensive testing checklist covering:
- SMS delivery testing (all 6 crew members)
- Assignment workflow (assign → notify → edit → submit)
- Admin notes system (create, edit, view)
- Mobile UI testing (iPhone Safari, Android Chrome)
- Photo upload from mobile camera
- Document generation with 3-4 photos
- Railway deployment validation
- Scale testing (60-day simulation)

**Use this checklist before deployment and during QA**

#### ENGINEER_TASKS.md
Task breakdown for development team:
- 20+ tasks organized by priority and complexity
- Estimated time for each task
- Testing requirements per task
- Development guidelines for junior engineers
- Progress tracking template
- Getting help resources

**Assign tasks from this document to team members**

### External Resources
- **Flask Docs**: https://flask.palletsprojects.com/
- **python-docx Docs**: https://python-docx.readthedocs.io/
- **Railway Docs**: https://docs.railway.app/
- **Twilio SMS Docs**: https://www.twilio.com/docs/sms

## ⚓ Credits

Built for maritime maintenance tracking operations.

## 📄 License

Proprietary - For internal use only.
