"""
Migration script to add admin_notes fields to work_items table.
Run this script once to update an existing database.
"""
from app import create_app, db

def migrate():
    app = create_app()
    with app.app_context():
        # Check if columns already exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('work_items')]

        if 'admin_notes' not in columns or 'admin_notes_updated_at' not in columns:
            print("Adding admin_notes columns to work_items table...")

            # Add the new columns using raw SQL
            with db.engine.connect() as conn:
                if 'admin_notes' not in columns:
                    conn.execute(db.text('ALTER TABLE work_items ADD COLUMN admin_notes TEXT'))
                    print("✓ Added admin_notes column")

                if 'admin_notes_updated_at' not in columns:
                    conn.execute(db.text('ALTER TABLE work_items ADD COLUMN admin_notes_updated_at DATETIME'))
                    print("✓ Added admin_notes_updated_at column")

                conn.commit()

            print("Migration completed successfully!")
        else:
            print("Columns already exist. No migration needed.")

if __name__ == '__main__':
    migrate()
