# Data Loss Issue & Fix

## What Happened

Your production data (5 completed, 3 in progress work items) was lost because:

1. **Railway uses ephemeral storage** - containers restart periodically (deployments, inactivity, updates)
2. **SQLite without a volume** - the database file is stored in the container, which gets wiped on restart
3. **Recent deployments** - pushing the ZOA banner updates triggered redeployments, wiping your database

## Fix: Add PostgreSQL Database

To prevent data loss, set up PostgreSQL on Railway (takes 5 minutes):

### Step 1: Add PostgreSQL to Railway

1. Open your Railway project: https://railway.app/project/your-project
2. Click **"New"** → **"Database"** → **"Add PostgreSQL"**
3. Railway automatically provisions the database

### Step 2: Link Database (Automatic)

Railway automatically sets the `DATABASE_URL` environment variable. Your app is already configured to use it - no code changes needed!

### Step 3: Verify Setup

1. Go to your Railway service → **"Variables"**
2. Confirm `DATABASE_URL` exists (starts with `postgresql://`)
3. Redeploy your app (it will auto-create tables)

### Step 4: Test

1. Create a test work item
2. Go to Railway → your service → **"Deployments"** → **"Restart"**
3. Check if the test item still exists ✅

## Alternative: SQLite with Railway Volume

If you prefer SQLite:

1. Go to Railway service → **"Settings"** → **"Volumes"**
2. Add volume with mount path: `/app/data`
3. Set environment variable: `DATABASE_URL=sqlite:////app/data/maintenance.db`
4. Redeploy

**Note:** PostgreSQL is more reliable and scales better.

## Current Status

- **Local database:** Empty (0 items)
- **Production database:** Was wiped during recent deployments
- **ZOA banner:** Removed (as requested)

## Next Steps

1. **Set up PostgreSQL** (recommended) - follow steps above
2. **Re-enter your data** - unfortunately, the lost data cannot be recovered
3. **Future-proof** - with PostgreSQL, your data will persist through all deployments

---

**Need help?** Check `DEPLOYMENT.md` for detailed Railway setup instructions.

