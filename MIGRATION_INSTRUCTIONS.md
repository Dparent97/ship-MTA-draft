# Database Migration: Increase Description Field Limit

## Problem
Users are getting an error when trying to save work items with descriptions longer than 500 characters:

```
value too long for type character varying(500)
```

## Solution
Increased the `description` field limit from **500** to **2000** characters.

## Migration Steps

### Step 1: Push Changes to GitHub

```bash
git push origin main
```

### Step 2: Run Migration on Railway

Use the Railway CLI to run the migration script on the production database:

```bash
# Make sure you're logged in
railway login

# Link to your project (if not already linked)
railway link

# Run the migration
railway run python migrate_increase_description_limit.py
```

**Expected output:**
```
======================================================================
  Database Migration: Increase Description Field Limit
======================================================================

Connecting to database...
Database: hopper.proxy.rlwy.net:18755/railway
Current description length: 500

Applying migration...
Altering column: description VARCHAR(500) -> VARCHAR(2000)
✓ Migration successful!

Description field can now hold up to 2000 characters.

======================================================================
  Migration Complete
======================================================================
```

### Step 3: Verify

1. Wait for Railway to redeploy (happens automatically after git push)
2. Have ART try to save their work item again
3. The error should be gone!

## What Changed

**File:** `app/models.py` (Line 12)
```python
# Before:
description = db.Column(db.String(500), nullable=False)

# After:
description = db.Column(db.String(2000), nullable=False)  # Increased from 500 to 2000
```

**Migration Script:** `migrate_increase_description_limit.py`
- Safely alters the PostgreSQL column type
- Can be run multiple times (idempotent)
- Checks current state before applying changes

## Troubleshooting

### If migration fails:

**Error: "DATABASE_URL not set"**
```bash
# Get the DATABASE_URL from Railway dashboard
railway variables

# Or run via Railway CLI which auto-loads env vars
railway run python migrate_increase_description_limit.py
```

**Error: "relation 'work_items' does not exist"**
- This shouldn't happen since the app is already running
- Check that you're connected to the right database

### Manual Migration (if script fails):

```bash
# Connect to Railway PostgreSQL directly
railway run bash

# Then run psql
psql $DATABASE_URL

# Run the SQL manually
ALTER TABLE work_items ALTER COLUMN description TYPE VARCHAR(2000);

# Exit
\q
exit
```

## After Migration

- **No data loss**: Existing descriptions remain intact
- **Existing items**: All work items keep their current descriptions
- **New limit**: Users can now enter up to 2000 characters
- **No app restart needed**: Railway auto-redeploys on git push

---

**Status:** Ready to deploy
**Impact:** Fixes the truncation error for ART and other users with long descriptions

