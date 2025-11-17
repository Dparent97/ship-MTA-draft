# Database Migration Setup Instructions

## Overview
This project now uses Flask-Migrate for database migrations instead of `db.create_all()`.

## Initial Setup (One-time)

After deploying this update, run the following commands:

```bash
# 1. Install updated dependencies
pip install -r requirements.txt

# 2. Initialize migrations (if migrations/ directory doesn't exist)
flask db init

# 3. Create initial migration from current models
flask db migrate -m "Initial migration from existing schema"

# 4. Apply the migration
flask db upgrade
```

## Future Schema Changes

When you need to modify the database schema:

```bash
# 1. Update your models in app/models.py

# 2. Generate a migration script
flask db migrate -m "Description of changes"

# 3. Review the generated migration in migrations/versions/

# 4. Apply the migration
flask db upgrade
```

## Rollback

If you need to rollback a migration:

```bash
# Rollback one version
flask db downgrade

# Rollback to a specific version
flask db downgrade <revision_id>
```

## Notes

- The `db.create_all()` line has been removed from `app/__init__.py`
- Migrations are now managed through Alembic via Flask-Migrate
- Always review generated migrations before applying them
- Backup your database before running migrations in production
