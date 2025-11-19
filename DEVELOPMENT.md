# Ship MTA Development Guide
*How to improve ship-MTA-draft without disrupting current users*

## Overview

This guide explains how to safely iterate on the ship-MTA-draft application while keeping it running for your crew. Standard development practices for production applications with active users.

---

## 1. Branch Strategy

### The Foundation
```
main          → Production (Railway auto-deploys from here)
├─ develop    → Staging/testing branch
└─ feature/*  → Individual features
```

### Workflow
```
feature/new-thing → develop → main
```

### Setup Commands

```bash
cd /Users/dp/repos/ship-MTA-draft  # or wherever you cloned it

# Create develop branch
git checkout -b develop
git push -u origin develop

# For new features:
git checkout develop
git checkout -b feature/better-photo-upload
# ... make changes ...
git commit -m "feat: improve photo upload UX"
git push -u origin feature/better-photo-upload

# Merge to develop first (test there)
git checkout develop
git merge feature/better-photo-upload

# When stable, merge to main (production)
git checkout main
git merge develop
git push
```

---

## 2. Environment Separation

You need **three environments**:

### Local (Your Machine)
- SQLite database
- Test credentials
- Port 5001
- Fast iteration

### Staging (Railway Project #2)
- Separate Railway deployment
- PostgreSQL database (separate from prod)
- Real-ish data (anonymized copy of prod)
- URL: `https://ship-mta-staging.up.railway.app`

### Production (Current Deployment)
- Your crew uses this
- Never deploy directly here
- Only deploy from `main` after staging verification

### Railway Staging Setup

**In Railway dashboard:**
1. Create new project "ship-MTA-staging"
2. Connect same GitHub repo but deploy from `develop` branch
3. Add PostgreSQL
4. Set environment variables (use test credentials)
5. Different `CREW_PASSWORD` so users don't accidentally use staging

### Config Changes

**Update `config.py`:**
```python
import os

class Config:
    # Environment detection
    ENV = os.getenv('ENVIRONMENT', 'development')  # 'development', 'staging', 'production'

    # Different settings per environment
    if ENV == 'production':
        DEBUG = False
        TESTING = False
    elif ENV == 'staging':
        DEBUG = True
        TESTING = True
    else:  # development
        DEBUG = True
        TESTING = True
```

**Railway Environment Variables:**
- Production: `ENVIRONMENT=production`
- Staging: `ENVIRONMENT=staging`

---

## 3. Database Migrations

When you change the database schema, you can't just `db.create_all()` in production.

### Install Flask-Migrate

```bash
pip install Flask-Migrate
pip freeze > requirements.txt
```

### Setup Migrations

**In `app/__init__.py`:**
```python
from flask_migrate import Migrate

app = Flask(__name__)
db.init_app(app)
migrate = Migrate(app, db)  # Add this
```

### Create Initial Migration

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### When You Change Models

```bash
# Make changes to models.py
flask db migrate -m "Add new field to WorkItem"
flask db upgrade  # Applies migration

# Test locally, then deploy
git add migrations/
git commit -m "feat: add new database field"
```

**Benefits:**
- Add fields without destroying data
- Roll back changes if something breaks
- Track schema changes in Git

---

## 4. Feature Flags

For risky changes, deploy them "dark" - in production but hidden behind a flag.

### Simple Implementation

**In `config.py`:**
```python
ENABLE_NEW_PHOTO_UPLOADER = os.getenv('ENABLE_NEW_PHOTO_UPLOADER', 'False') == 'True'
ENABLE_BATCH_EDIT = os.getenv('ENABLE_BATCH_EDIT', 'False') == 'True'
```

**In your routes:**
```python
@crew_bp.route('/submit', methods=['GET', 'POST'])
def crew_form():
    if current_app.config['ENABLE_NEW_PHOTO_UPLOADER']:
        return render_template('crew_form_v2.html')
    else:
        return render_template('crew_form.html')  # Old version
```

### Deploy Process
1. Deploy new code with flag OFF
2. Test in production (only you see it by manually enabling)
3. Flip flag ON for everyone when ready
4. Remove old code later

---

## 5. Testing Strategy

### Directory Structure

```
tests/
├─ __init__.py
├─ test_auth.py
├─ test_crew_submit.py
├─ test_admin_dashboard.py
└─ test_docx_generation.py
```

### Basic Test Example

**`tests/test_crew_submit.py`:**
```python
import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_crew_login(client):
    """Test crew can log in"""
    response = client.post('/crew/login', data={
        'password': 'crew2026'
    })
    assert response.status_code == 302  # Redirect on success

def test_crew_submit_form(client):
    """Test crew can submit work item"""
    # Login first
    client.post('/crew/login', data={'password': 'crew2026'})

    # Submit form
    response = client.post('/crew/submit', data={
        'description': 'Test work item',
        'location': 'Engine Room',
        # ... other fields
    })
    assert response.status_code == 200
    assert b'Success' in response.data
```

### Run Tests

```bash
pip install pytest
pytest tests/
```

---

## 6. Deployment Checklist

### Pre-Deployment

```markdown
- [ ] All tests pass locally
- [ ] Changes tested in staging environment
- [ ] Database migrations tested (if applicable)
- [ ] No breaking changes to API/URLs
- [ ] Environment variables updated (if needed)
- [ ] Backup current production database
- [ ] Notify crew of downtime (if any)
```

### Post-Deployment

```markdown
- [ ] Verify app is accessible
- [ ] Test login (crew and admin)
- [ ] Test core functionality (submit, view, download)
- [ ] Check Railway logs for errors
- [ ] Monitor for 30 minutes
```

### Rollback Plan

If something breaks:
```bash
git revert <commit-hash>
git push origin main
```

---

## 7. Backward Compatibility Rules

### Never Break These
- Existing URLs (crew bookmarked them)
- Database field removal (migrate, don't delete)
- Authentication flow (crew know current password)
- Generated .docx format (they have templates expecting this)

### If You Must Change These
1. Deploy new version alongside old
2. Redirect old URLs to new
3. Keep both working for 2-4 weeks
4. Remove old version after verification

---

## 8. Communication with Users

### Before Major Changes

```
Hey team - Upgrading the MTA app this weekend.
New features:
- Faster photo upload
- Bulk editing for admin

Expect 10 minutes downtime Saturday 0300.
Old URL still works. Nothing changes for crew submissions.

Questions? Text me.
```

### After Deployment

```
✅ Upgrade complete. App is faster.
Everything works same as before.
Let me know if anything looks weird.
```

---

## Immediate Action Plan

### Week 1: Setup Infrastructure

```bash
# 1. Create branches
git checkout -b develop
git push -u origin develop

# 2. Setup staging on Railway
# (manual: create new Railway project, point to develop branch)

# 3. Add Flask-Migrate
pip install Flask-Migrate
# Add to app/__init__.py
flask db init
flask db migrate -m "Initial migration"
git add .
git commit -m "chore: add database migrations"
git push origin develop

# 4. Create tests directory
mkdir tests
touch tests/__init__.py tests/test_basic.py
```

### Week 2: Add First Feature (Safe)

```bash
git checkout develop
git checkout -b feature/improved-logging

# Add logging to critical points
# Test locally
# Deploy to staging
# Verify in staging
# Merge to develop
# Deploy to production via main
```

### Week 3+: Iterate
- Each feature: branch → develop → test → main
- Database changes: migrations first
- Big changes: feature flags
- Always test in staging

---

## Low Risk, High Value Additions

### 1. Health Check Endpoint

```python
@app.route('/health')
def health():
    return {'status': 'ok', 'environment': Config.ENV}, 200
```

### 2. Better Logging

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@crew_bp.route('/submit', methods=['POST'])
def submit():
    logger.info(f"Work item submitted by {session.get('name')}")
    # ... rest of code
```

### 3. Admin Metrics Dashboard
- Submissions per day
- Average photos per submission
- Most common locations
- Quick stats for usage monitoring

### 4. Error Handling

```python
@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Server Error: {error}')
    return render_template('error.html'), 500
```

---

## Summary: What Normal Developers Do

1. ✅ Use branches (feature → develop → main)
2. ✅ Have staging environment
3. ✅ Test before production
4. ✅ Use database migrations
5. ✅ Deploy small changes frequently
6. ✅ Monitor after deployment
7. ✅ Keep rollback plan ready

## Your Checklist

1. Set up `develop` branch TODAY
2. Create staging Railway project THIS WEEK
3. Add Flask-Migrate BEFORE your next DB change
4. Make one small improvement (logging) as practice
5. Then tackle bigger features with confidence

---

*Generated for DP - Marine Engineer transitioning to infrastructure/AI roles*
*Keep this guide in your project repo for reference*
