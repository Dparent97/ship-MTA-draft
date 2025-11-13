# Railway Staging Environment Setup Guide

This guide explains how to set up a staging environment on Railway for testing the frontend modernization changes before deploying to production.

---

## 🎯 Why a Staging Environment?

A staging environment allows you to:
- Test the `frontend-development` branch in a production-like environment
- Verify all features work with a real PostgreSQL database
- Test on actual mobile devices using a public URL
- Catch issues before they reach production
- Allow others to test without running locally

---

## 📋 Prerequisites

- Railway account (already set up for production)
- Railway CLI installed (optional but recommended)
- GitHub repository access
- Admin access to Railway project

---

## 🚀 Method 1: Railway Dashboard (Recommended)

### Step 1: Create New Service

1. Go to your Railway dashboard: https://railway.app/dashboard
2. Open your existing project (`ship-mta-draft-production`)
3. Click **"+ New"** → **"Empty Service"**
4. Name it: `ship-mta-draft-staging`

### Step 2: Connect GitHub Repository

1. In the new service, click **"Settings"**
2. Under **"Source"**, click **"Connect Repo"**
3. Select: `Dparent97/ship-MTA-draft`
4. Under **"Branch"**, select: `frontend-development`
5. **Important:** Enable **"Watch Paths"** if you only want to deploy on changes to specific files (optional)

### Step 3: Add PostgreSQL Database

1. Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway will create a new PostgreSQL instance
3. Name it: `staging-database`

### Step 4: Configure Environment Variables

In your staging service settings, add these environment variables:

```bash
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=<generate-new-secret-key-for-staging>

# Database (Railway will auto-populate these)
DATABASE_URL=${DATABASE_URL}  # This references the staging PostgreSQL

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin67

# Crew Password
CREW_PASSWORD=crew67

# File Upload Settings
UPLOAD_FOLDER=/app/uploads
GENERATED_DOCS_FOLDER=/app/generated_docs
MAX_CONTENT_LENGTH=10485760  # 10MB

# Optional: Flag to indicate staging environment
ENVIRONMENT=staging
```

**To generate a new SECRET_KEY:**
```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

### Step 5: Configure Volumes (Persistent Storage)

1. In service settings, go to **"Volumes"**
2. Add two volumes:
   - **Mount Path:** `/app/uploads`
     - **Size:** 5GB
   - **Mount Path:** `/app/generated_docs`
     - **Size:** 2GB

### Step 6: Configure Deployment

1. In **"Settings"** → **"Deploy"**
2. Set **"Start Command"**: `gunicorn --bind 0.0.0.0:$PORT run:app`
3. Set **"Build Command"**: (leave empty, Railway auto-detects)
4. **"Health Check Path"**: `/crew/login` (or `/`)

### Step 7: Deploy

1. Click **"Deploy"**
2. Railway will build and deploy your staging environment
3. Watch the logs for any errors
4. Once deployed, you'll get a staging URL like: `https://ship-mta-draft-staging.up.railway.app`

### Step 8: Initialize Database

The staging database will be empty. You have two options:

**Option A: Start Fresh (Recommended for Testing)**
- The app will auto-create tables on first run
- You'll need to manually create test data

**Option B: Clone Production Data**
1. Export production database (careful with sensitive data!)
2. Import into staging database

---

## 🛠️ Method 2: Railway CLI

### Install Railway CLI

```bash
# macOS
brew install railway

# Or via npm
npm install -g @railway/cli
```

### Login to Railway

```bash
railway login
```

### Create Staging Environment

```bash
# Clone your production project
railway link

# Create new environment
railway environment create staging

# Switch to staging environment
railway environment use staging

# Deploy frontend-development branch
railway up --branch frontend-development

# Add PostgreSQL
railway add --database postgresql

# Set environment variables
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=<your-new-secret-key>
railway variables set ENVIRONMENT=staging
```

### View Staging URL

```bash
railway domain
```

---

## 🔧 Configuration Differences: Staging vs Production

| Setting | Production | Staging |
|---------|-----------|---------|
| **Branch** | `main` | `frontend-development` |
| **Database** | `production-db` | `staging-db` (separate) |
| **URL** | `ship-mta-draft-production.up.railway.app` | `ship-mta-draft-staging.up.railway.app` |
| **Environment Variable** | `ENVIRONMENT=production` | `ENVIRONMENT=staging` |
| **Auto-deploy** | On push to `main` | On push to `frontend-development` |

---

## 🧪 Testing Workflow

### Step 1: Push Changes to Frontend Branch

```bash
git checkout frontend-development
git add .
git commit -m "Your changes"
git push origin frontend-development
```

Railway will automatically deploy to staging.

### Step 2: Access Staging URL

Visit your staging URL: `https://ship-mta-draft-staging.up.railway.app`

### Step 3: Run Tests

Use the testing checklist (`TESTING_PR1_FRONTEND.md`) or run:

```bash
# Update the script to point to staging URL instead of localhost
./test_frontend.sh
```

### Step 4: Test on Mobile Devices

- Open staging URL on actual iPhone/Android devices
- Test photo upload from camera
- Test responsive behavior
- Verify touch targets are adequate

### Step 5: Monitor Logs

```bash
# Via CLI
railway logs --environment staging

# Or in Railway Dashboard → Staging Service → Logs
```

### Step 6: Approve and Merge

Once all tests pass on staging:
1. Approve PR #1 on GitHub
2. Merge `frontend-development` → `main`
3. Production will auto-deploy from `main` branch

---

## 🔄 Automatic Staging Deploys with GitHub Actions (Optional)

Create `.github/workflows/staging-deploy.yml`:

```yaml
name: Deploy to Staging

on:
  push:
    branches:
      - frontend-development

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Install Railway CLI
        run: npm install -g @railway/cli
      
      - name: Deploy to Railway Staging
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          railway link ${{ secrets.RAILWAY_PROJECT_ID }}
          railway environment use staging
          railway up
```

**Setup:**
1. Get Railway token: `railway login && railway whoami --token`
2. Add to GitHub Secrets: `RAILWAY_TOKEN`
3. Get project ID from Railway dashboard
4. Add to GitHub Secrets: `RAILWAY_PROJECT_ID`

---

## 🗄️ Database Management

### Create Test Data in Staging

```python
# Use this script to populate staging with test data
# Run: python create_test_data.py

from app import app, db
from app.models import WorkItem, Photo
import random

with app.app_context():
    # Create test work items
    crew_members = ["John Smith", "Jane Doe", "Mike Johnson", "Sarah Williams"]
    locations = ["Engine Room", "Pilot House", "Main Deck", "Galley"]
    
    for i in range(20):
        item = WorkItem(
            item_number=f"TEST_{i+1:04d}",
            submitted_by=random.choice(crew_members),
            location=random.choice(locations),
            description=f"Test work item {i+1}",
            detail=f"This is a detailed description for test item {i+1}",
            status=random.choice(["Submitted", "In Review by DP", "Completed Review"])
        )
        db.session.add(item)
    
    db.session.commit()
    print("✓ Test data created successfully")
```

### Reset Staging Database

```bash
# Via Railway CLI
railway run --environment staging python << EOF
from app import app, db
with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database reset complete")
EOF
```

---

## 🔐 Security Considerations

### Staging Environment Best Practices

1. **Different Credentials:** Use different passwords than production
2. **Test Data Only:** Don't use real production data in staging
3. **Access Control:** Limit who has access to staging URL
4. **Temporary Files:** Clear uploads periodically in staging
5. **Environment Variables:** Never commit secrets to Git

### Protecting Staging URL

If you want to restrict access to staging:

1. **Railway Private Networking:** Enable private networking (Pro plan)
2. **Basic Auth:** Add middleware to require authentication
3. **IP Whitelist:** Configure Railway firewall rules

---

## 📊 Monitoring Staging

### Railway Dashboard Metrics

Monitor in Railway Dashboard:
- **Deployment Status:** Success/failure of builds
- **Resource Usage:** CPU, Memory, Disk
- **Logs:** Real-time application logs
- **Metrics:** Request count, response times

### Application Logs

```bash
# Watch logs in real-time
railway logs --environment staging --tail

# Filter for errors
railway logs --environment staging | grep ERROR
```

---

## 🧹 Cleanup & Cost Management

### Delete Staging When Done

If you only need staging temporarily:

```bash
# Via CLI
railway environment delete staging

# Or in Dashboard: Settings → Danger Zone → Delete Service
```

### Cost Estimates

Railway pricing (as of 2024):
- **Hobby Plan:** $5/month (500 hours execution time)
- **Pro Plan:** $20/month (unlimited execution)
- **Database:** Included in plan
- **Additional Storage:** ~$0.25/GB/month

**Staging costs:**
- If running 24/7: ~$5-10/month
- If only running during testing: ~$2-5/month

---

## 🆘 Troubleshooting

### Deployment Fails

```bash
# Check build logs
railway logs --environment staging

# Common issues:
# 1. Missing environment variables → Check settings
# 2. Database connection fails → Verify DATABASE_URL
# 3. Port binding error → Use PORT env var: gunicorn --bind 0.0.0.0:$PORT
```

### Database Connection Errors

```bash
# Verify database is connected
railway variables --environment staging | grep DATABASE_URL

# Test database connection
railway run --environment staging python -c "from app import db; print(db.engine.url)"
```

### File Upload Not Working

```bash
# Check volumes are mounted
railway volumes --environment staging

# Verify permissions
railway run --environment staging ls -la /app/uploads
```

---

## ✅ Staging Checklist

Before considering staging setup complete:

- [ ] Staging service created and deployed
- [ ] Separate PostgreSQL database connected
- [ ] All environment variables configured
- [ ] Volumes mounted for uploads and docs
- [ ] Staging URL accessible
- [ ] Can log in as admin
- [ ] Can log in as crew member
- [ ] Database tables created automatically
- [ ] Test data populated (optional)
- [ ] Logs show no errors
- [ ] Auto-deploy from `frontend-development` branch working

---

## 📞 Next Steps

1. **Set up staging environment** using Method 1 or 2 above
2. **Run comprehensive tests** using `TESTING_PR1_FRONTEND.md`
3. **Test on actual mobile devices** using staging URL
4. **Document any issues** found
5. **Fix issues** in `frontend-development` branch (auto-deploys to staging)
6. **Re-test** until all tests pass
7. **Merge to main** when ready

---

## 📚 Additional Resources

- **Railway Docs:** https://docs.railway.app/
- **Railway CLI Reference:** https://docs.railway.app/develop/cli
- **Flask Deployment Guide:** https://flask.palletsprojects.com/en/2.3.x/deploying/
- **Gunicorn Configuration:** https://docs.gunicorn.org/en/stable/configure.html

---

**Questions or Issues?**

If you encounter problems setting up staging:
1. Check Railway dashboard logs
2. Verify all environment variables are set
3. Ensure database is connected
4. Review this guide's troubleshooting section
5. Contact Railway support if needed

Happy testing! 🚀

