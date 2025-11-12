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

## 📋 What's Included

### Core Files
- `SHIP_MAINTENANCE_APP_BUILD_GUIDE.md` - Complete build instructions
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

Railway provides a seamless deployment experience with PostgreSQL database support and persistent storage options.

#### Prerequisites
- GitHub repository with your code
- Railway account (https://railway.app)
- Updated credentials (see Security section below)

#### Step-by-Step Deployment

1. **Prepare Your Code**
   ```bash
   # Ensure all files are committed
   git add .
   git commit -m "Prepare for production deployment"
   git push origin main
   ```

2. **Create Railway Project**
   ```bash
   # Install Railway CLI (optional)
   npm install -g railway

   # Login to Railway
   railway login

   # Create new project
   railway init
   ```

   Or use the Railway web dashboard:
   - Go to https://railway.app/new
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Environment Variables**

   In Railway dashboard, go to your project → Variables → Add all of these:

   **Required Variables:**
   ```bash
   # Application Security
   SECRET_KEY=<generate-random-64-char-string>
   ADMIN_USERNAME=<your-admin-username>
   ADMIN_PASSWORD=<strong-password-here>
   CREW_PASSWORD=<strong-password-here>

   # Database (automatically set by Railway if you add PostgreSQL)
   DATABASE_URL=<automatically-provided-by-railway>

   # Python Environment
   PYTHONUNBUFFERED=1
   ```

   **Optional Variables (for SMS notifications):**
   ```bash
   ENABLE_NOTIFICATIONS=True
   TWILIO_ACCOUNT_SID=<your-twilio-sid>
   TWILIO_AUTH_TOKEN=<your-twilio-token>
   TWILIO_PHONE_NUMBER=<your-twilio-number>

   # Crew member phone numbers (E.164 format: +1234567890)
   DP_PHONE=+1234567890
   AL_PHONE=+1234567890
   KAITLYN_PHONE=+1234567890
   MARK_PHONE=+1234567890
   ART_PHONE=+1234567890
   D2_PHONE=+1234567890
   ```

   **Generate SECRET_KEY:**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

4. **Add PostgreSQL Database**
   - In Railway dashboard, click "New" → "Database" → "Add PostgreSQL"
   - Railway automatically sets the `DATABASE_URL` environment variable
   - Database tables will be created automatically on first run

5. **Configure File Storage (Critical!)**

   Railway uses ephemeral filesystem - uploaded files are lost on restart. Choose one option:

   **Option A: Railway Volumes (Simpler)**
   - In Railway dashboard, go to Settings → Volumes
   - Add volume: Mount path `/app/uploads`
   - Add volume: Mount path `/app/generated_docs`
   - Redeploy application

   **Option B: Cloud Storage (Recommended for production)**
   - Use AWS S3, Google Cloud Storage, or Cloudinary
   - See `ENGINEER_TASKS.md` Task 1.5 for implementation details
   - Update code to store files in cloud instead of local filesystem

6. **Deploy**
   ```bash
   # Using Railway CLI
   railway up

   # Or push to GitHub (if auto-deploy enabled)
   git push origin main
   ```

7. **Monitor Deployment**
   - Watch build logs in Railway dashboard
   - Verify deployment succeeds
   - Check for any error messages

8. **Access Your Application**
   - Railway provides a public URL: `https://your-app.up.railway.app`
   - Test login functionality
   - Verify database connectivity
   - Upload test photo and verify persistence

#### Post-Deployment Checklist

- [ ] Application accessible via HTTPS
- [ ] Admin login works with new credentials
- [ ] Crew login works with new password
- [ ] Database persists data after restart
- [ ] Photo uploads work and persist
- [ ] Document generation works
- [ ] Mobile UI functions correctly on iPhone and Android
- [ ] SMS notifications working (if enabled)
- [ ] Check Railway logs for errors
- [ ] Monitor application performance

#### Updating Production

```bash
# Make changes locally
git add .
git commit -m "Update: description of changes"
git push origin main

# Railway auto-deploys (if enabled)
# Or manually trigger: railway up
```

#### Railway Configuration Files

Create `railway.json` in project root (optional):
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python run.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Or create `Procfile`:
```
web: python run.py
```

---

### Alternative: Render Deployment

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** arrowhead-mta-2026
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python run.py`

3. **Add PostgreSQL Database**
   - Click "New" → "PostgreSQL"
   - Note the internal database URL

4. **Configure Environment Variables**
   - Add all variables listed in Railway section above
   - Set `DATABASE_URL` to your Render PostgreSQL URL

5. **Deploy**
   - Render automatically deploys on push to main branch
   - Monitor build logs
   - Access via provided URL: `https://your-app.onrender.com`

---

### Alternative: Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   brew install heroku/brew/heroku  # macOS
   # Or download from heroku.com
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create arrowhead-mta-2026
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Configure Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set ADMIN_USERNAME=your-admin
   heroku config:set ADMIN_PASSWORD=your-password
   heroku config:set CREW_PASSWORD=your-crew-password
   ```

5. **Create Procfile**
   ```
   web: python run.py
   ```

6. **Deploy**
   ```bash
   git push heroku main
   heroku open
   ```

---

### Docker Deployment (Advanced)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "run.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5001:5001"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/maintenance
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./generated_docs:/app/generated_docs
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=maintenance
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Deploy:
```bash
docker-compose up -d
```

---

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes* | `dev_key_change_in_production` | Flask session secret (change in prod!) |
| `ADMIN_USERNAME` | Yes* | `admin` | Admin login username (change in prod!) |
| `ADMIN_PASSWORD` | Yes* | `admin350` | Admin login password (change in prod!) |
| `CREW_PASSWORD` | Yes* | `crew350` | Crew login password (change in prod!) |
| `DATABASE_URL` | No | `sqlite:///maintenance.db` | PostgreSQL connection string |
| `ENABLE_NOTIFICATIONS` | No | `False` | Enable SMS notifications |
| `TWILIO_ACCOUNT_SID` | No | - | Twilio account SID (for SMS) |
| `TWILIO_AUTH_TOKEN` | No | - | Twilio auth token (for SMS) |
| `TWILIO_PHONE_NUMBER` | No | - | Twilio phone number (for SMS) |
| `DP_PHONE` | No | - | DP crew member phone |
| `AL_PHONE` | No | - | AL crew member phone |
| `KAITLYN_PHONE` | No | - | Kaitlyn crew member phone |
| `MARK_PHONE` | No | - | Mark crew member phone |
| `ART_PHONE` | No | - | Art crew member phone |
| `D2_PHONE` | No | - | D2 crew member phone |

*Required in production - defaults are insecure and should only be used for local development.

---

### Deployment Troubleshooting

#### Application Won't Start
- Check Railway/Render logs for Python errors
- Verify all required environment variables are set
- Ensure `requirements.txt` includes all dependencies
- Check Python version compatibility (requires 3.8+)

#### Database Connection Errors
- Verify `DATABASE_URL` is set correctly
- Ensure PostgreSQL service is running
- Check database credentials
- Test connection manually: `psql $DATABASE_URL`

#### Photos Not Persisting After Restart
- Railway/Render use ephemeral filesystems
- Must use Railway Volumes or cloud storage (S3, Cloudinary)
- See Task 1.5 in `ENGINEER_TASKS.md` for implementation

#### 404 Errors on Static Files
- Ensure `/app/static/` folder exists
- Check file permissions
- Verify static file paths in templates

#### SMS Notifications Not Working
- Verify `ENABLE_NOTIFICATIONS=True`
- Check Twilio credentials are correct
- Verify phone numbers in E.164 format (+1234567890)
- Check Twilio account balance
- Review application logs for Twilio errors

#### Performance Issues
- Enable database connection pooling
- Optimize image processing (see Task 4.4 in `ENGINEER_TASKS.md`)
- Consider caching with Redis
- Monitor Railway metrics (CPU, memory, response times)
- Add database indexes for frequently queried fields

#### SSL/HTTPS Issues
- Railway and Render provide HTTPS automatically
- If using custom domain, configure DNS correctly
- Ensure SSL certificate is valid

---

### Monitoring & Maintenance

#### Railway Monitoring
- Access logs: Railway dashboard → Deployments → View logs
- Monitor metrics: CPU, memory, disk usage
- Set up alerts for downtime
- Enable auto-scaling if needed

#### Health Checks
Create `/health` endpoint in `app/__init__.py`:
```python
@app.route('/health')
def health_check():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        return {'status': 'healthy', 'database': 'connected'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

#### Backup Strategy
- Railway PostgreSQL: Enable automated backups
- Export database regularly: `pg_dump $DATABASE_URL > backup.sql`
- Backup uploaded photos to S3/cloud storage
- Keep copies of generated documents

#### Log Monitoring
```python
# Add structured logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
```

---

### Security Best Practices for Production

1. **Change All Default Credentials**
   - Generate strong passwords (16+ characters)
   - Use password manager (1Password, Bitwarden)
   - Never commit credentials to Git

2. **Enable HTTPS Only**
   - Railway/Render provide HTTPS automatically
   - Set `SESSION_COOKIE_SECURE = True` in production

3. **Secure File Uploads**
   - Validate file types and sizes
   - Scan for malware (optional: use ClamAV)
   - Store files outside web root

4. **Database Security**
   - Use strong PostgreSQL password
   - Limit database access by IP (if possible)
   - Regular security updates

5. **Regular Updates**
   - Keep Python dependencies updated: `pip list --outdated`
   - Monitor security advisories
   - Update Flask and Pillow regularly

6. **Rate Limiting**
   - Add Flask-Limiter to prevent abuse
   - Limit login attempts
   - Throttle API endpoints

7. **Error Handling**
   - Never expose stack traces in production
   - Log errors securely
   - Use custom error pages

---

### Performance Optimization

1. **Database Optimization**
   - Add indexes: `db.Index('idx_status', 'status')`
   - Use database connection pooling
   - Optimize slow queries

2. **Caching**
   - Cache rendered pages (Flask-Caching)
   - Cache database queries
   - Use CDN for static assets

3. **Image Optimization**
   - Process images asynchronously (Celery + Redis)
   - Use WebP format for smaller file sizes
   - Implement lazy loading

4. **Code Optimization**
   - Use pagination for large result sets
   - Minimize database queries (eager loading)
   - Profile slow endpoints

---

### Scaling Considerations

As your application grows, consider:

1. **Horizontal Scaling**
   - Multiple Railway instances behind load balancer
   - Stateless application design
   - Shared PostgreSQL database

2. **Vertical Scaling**
   - Upgrade Railway plan for more CPU/memory
   - Optimize application performance first

3. **Microservices (Future)**
   - Separate document generation service
   - Separate notification service
   - API gateway

4. **CDN Integration**
   - CloudFlare for static assets
   - Faster photo delivery worldwide
   - DDoS protection

## 📸 Features

- ✅ Mobile-optimized submission form
- ✅ Photo upload with auto-resize (4" width)
- ✅ Generates .docx files matching template
- ✅ Admin dashboard with status tracking
- ✅ Batch download as .zip
- ✅ Works on iPhone and Android

## 🔐 Security Notes

**IMPORTANT:** Change these defaults in production:
- `SECRET_KEY` in config.py
- `CREW_PASSWORD` in config.py
- `ADMIN_PASSWORD` in config.py

## 📝 Customization

### Update Crew Members
Edit `config.py`:
```python
CREW_MEMBERS = [
    'Your',
    'Crew',
    'Names',
    'Here'
]
```

### Adjust Photo Settings
Edit `config.py`:
```python
PHOTO_MAX_WIDTH = 576  # 4 inches at 144 DPI
PHOTO_MIN_COUNT = 2
PHOTO_MAX_COUNT = 6
```

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Run `pip install -r requirements.txt`
2. **Database errors**: Delete `maintenance.db` and restart
3. **Port in use**: Change port in `run.py`
4. **Photos not uploading**: Check folder permissions

## 📚 Documentation

### Project Documentation
- **Build Guide**: `SHIP_MAINTENANCE_APP_BUILD_GUIDE.md` - Complete step-by-step build instructions
- **Testing Checklist**: `TESTING_CHECKLIST.md` - Comprehensive manual test scenarios for all features
- **Engineer Tasks**: `ENGINEER_TASKS.md` - Task breakdown and implementation guide for junior engineers
- **README**: `README.md` - This file - overview and deployment guide

### External Documentation
- **Flask Docs**: https://flask.palletsprojects.com/
- **python-docx Docs**: https://python-docx.readthedocs.io/
- **Pillow Docs**: https://pillow.readthedocs.io/
- **Railway Docs**: https://docs.railway.app/
- **Twilio SMS API**: https://www.twilio.com/docs/sms

## ⚓ Credits

Built for maritime maintenance tracking operations.

## 📄 License

Proprietary - For internal use only.
