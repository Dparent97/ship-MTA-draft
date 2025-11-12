# Railway Deployment Guide

This guide walks you through deploying the Ship Maintenance Tracking Application to Railway.

## Prerequisites

1. A [Railway](https://railway.app/) account
2. Railway CLI installed (optional but recommended): `npm install -g @railway/cli`
3. Git repository with your code

## Quick Start Deployment

### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub** (if not already done)

2. **Create a new Railway project:**
   - Go to [railway.app](https://railway.app/)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect the Python application

3. **Configure Environment Variables:**
   - In your Railway project dashboard, go to "Variables"
   - Add the following required variables:

   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-a-secure-random-string>
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=<your-secure-admin-password>
   CREW_PASSWORD=<your-secure-crew-password>
   ```

   **Generate a secure SECRET_KEY:**
   ```bash
   python -c 'import secrets; print(secrets.token_hex(32))'
   ```

4. **Deploy!**
   - Railway will automatically build and deploy your application
   - Your app will be available at the generated Railway URL

### Option 2: Deploy from Railway CLI

1. **Login to Railway:**
   ```bash
   railway login
   ```

2. **Initialize Railway in your project:**
   ```bash
   railway init
   ```

3. **Set environment variables:**
   ```bash
   railway variables set FLASK_ENV=production
   railway variables set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
   railway variables set ADMIN_USERNAME=admin
   railway variables set ADMIN_PASSWORD=your-secure-password
   railway variables set CREW_PASSWORD=your-crew-password
   ```

4. **Deploy:**
   ```bash
   railway up
   ```

## Database Options

### Option A: SQLite (Default - Simpler Setup)

SQLite is configured by default and works well for small to medium workloads.

**Important:** You need to set up a Railway Volume to persist SQLite data:

1. In Railway dashboard, go to your service
2. Click on "Settings" → "Volumes"
3. Add a new volume:
   - **Mount Path:** `/app/data`
   - Click "Add Volume"

4. Update DATABASE_URL variable:
   ```bash
   railway variables set DATABASE_URL=sqlite:////app/data/maintenance.db
   ```

### Option B: PostgreSQL (Recommended for Production)

For better performance and reliability in production:

1. **Add PostgreSQL to your Railway project:**
   - In your Railway project, click "New Service"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically provision a PostgreSQL database

2. **Link the database:**
   - Railway will automatically set the `DATABASE_URL` environment variable
   - The app is already configured to handle Railway's PostgreSQL connection string

3. **No additional configuration needed!**
   - The app will automatically use PostgreSQL when `DATABASE_URL` is set

## Persistent File Storage

The application needs persistent storage for uploaded photos and generated documents.

### Set Up Railway Volume

1. In Railway dashboard, go to your service
2. Click "Settings" → "Volumes"
3. Add volumes for:
   - **Mount Path:** `/app/uploads` (for photo uploads)
   - **Mount Path:** `/app/generated_docs` (for generated Word documents)

Alternatively, if using a single volume:
- **Mount Path:** `/app/data`
- Update environment variables:
  ```bash
  railway variables set UPLOAD_FOLDER=/app/data/uploads
  railway variables set GENERATED_DOCS_FOLDER=/app/data/generated_docs
  ```

## Optional: Email Notifications

To enable email notifications for status updates:

1. **Set notification environment variables:**
   ```bash
   railway variables set ENABLE_NOTIFICATIONS=True
   railway variables set SMTP_SERVER=smtp.gmail.com
   railway variables set SMTP_PORT=587
   railway variables set SMTP_USERNAME=your-email@gmail.com
   railway variables set SMTP_PASSWORD=your-app-password
   railway variables set NOTIFICATION_FROM_EMAIL=noreply@yourdomain.com
   ```

2. **Set crew email addresses:**
   ```bash
   railway variables set DP_EMAIL=dp@example.com
   railway variables set AL_EMAIL=al@example.com
   # ... add other crew emails as needed
   ```

**Note:** For Gmail, you'll need to use an [App Password](https://support.google.com/accounts/answer/185833).

## Monitoring and Logs

### View Logs
- In Railway dashboard: Click on "Deployments" → Select deployment → View logs
- Via CLI: `railway logs`

### Monitor Application
- Railway provides built-in metrics (CPU, Memory, Network)
- Access via the "Metrics" tab in your service dashboard

## Custom Domain (Optional)

1. In Railway dashboard, go to "Settings" → "Domains"
2. Click "Generate Domain" for a Railway subdomain, or
3. Click "Custom Domain" to add your own domain
4. Follow the DNS configuration instructions

## Updating Your Deployment

### Automatic Deployments (GitHub)
- Railway automatically deploys on every push to your main branch
- Configure deployment branch in Settings → Deployment

### Manual Deployments (CLI)
```bash
railway up
```

## Troubleshooting

### Application Won't Start

1. **Check environment variables:**
   ```bash
   railway variables
   ```
   - Ensure `FLASK_ENV=production`
   - Ensure `SECRET_KEY` is set

2. **Check logs:**
   ```bash
   railway logs
   ```

### Database Connection Issues

**For PostgreSQL:**
- Verify `DATABASE_URL` is set: `railway variables | grep DATABASE_URL`
- Check PostgreSQL service is running in Railway dashboard

**For SQLite:**
- Ensure volume is mounted correctly
- Verify `DATABASE_URL` points to the volume path

### File Upload Issues

1. **Verify volumes are mounted:**
   - Check Railway dashboard → Settings → Volumes
   - Ensure mount paths match `UPLOAD_FOLDER` and `GENERATED_DOCS_FOLDER`

2. **Check folder permissions:**
   - Logs should show folder creation on startup
   - If permission errors, verify volume mount paths

### Out of Memory

If the app runs out of memory:
1. Upgrade your Railway plan for more resources
2. Reduce Gunicorn workers in `Procfile`:
   ```
   web: gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 run:app
   ```

## Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore` by default
2. **Use strong passwords** - Especially for `ADMIN_PASSWORD` and `SECRET_KEY`
3. **Regularly update dependencies:**
   ```bash
   pip list --outdated
   pip install --upgrade <package>
   ```
4. **Enable HTTPS** - Railway provides HTTPS by default
5. **Set secure session cookies** - Already configured in production mode

## Cost Optimization

- **Starter Plan:** Free tier with $5/month credit (sufficient for small teams)
- **Developer Plan:** $20/month for more resources
- **SQLite vs PostgreSQL:** SQLite is free; PostgreSQL costs $5-20/month depending on usage

## Support and Resources

- [Railway Documentation](https://docs.railway.app/)
- [Railway Discord Community](https://discord.gg/railway)
- [Application Repository Issues](https://github.com/your-repo/issues)

## Rollback Procedure

If a deployment fails or has issues:

1. **Via Dashboard:**
   - Go to "Deployments"
   - Find the last working deployment
   - Click "Redeploy"

2. **Via CLI:**
   ```bash
   railway rollback
   ```

## Health Checks

Railway automatically monitors your application. To add custom health check:

Add to `app/__init__.py`:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200
```

Configure in Railway:
- Settings → Health Check Path: `/health`

## Backup Strategy

### For SQLite:
- Use Railway's volume snapshots (Pro plan feature)
- Or manually download the database file periodically

### For PostgreSQL:
- Railway automatically creates daily backups
- Access backups in PostgreSQL service → Backups tab
- Manual backup: `railway connect postgres` then use `pg_dump`

---

**Deployment Checklist:**

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Environment variables configured (FLASK_ENV, SECRET_KEY, passwords)
- [ ] Database option selected (SQLite with volume OR PostgreSQL)
- [ ] Volumes configured for file uploads
- [ ] Application deployed and accessible
- [ ] Admin login tested
- [ ] Crew login tested
- [ ] File upload tested
- [ ] Custom domain configured (optional)
- [ ] Email notifications configured (optional)

**You're all set! Your Ship Maintenance Tracking Application is now running on Railway.**
