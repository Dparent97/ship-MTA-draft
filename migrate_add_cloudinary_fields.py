"""
Migration script to add cloudinary_public_id and cloudinary_url fields to photos table.
Run this script once to update an existing database for Cloudinary support.
"""
from app import create_app, db

def migrate():
    app = create_app()
    with app.app_context():
        # Check if columns already exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('photos')]

        if 'cloudinary_public_id' not in columns or 'cloudinary_url' not in columns:
            print("Adding Cloudinary columns to photos table...")

            # Add the new columns using raw SQL
            with db.engine.connect() as conn:
                if 'cloudinary_public_id' not in columns:
                    conn.execute(db.text('ALTER TABLE photos ADD COLUMN cloudinary_public_id VARCHAR(300)'))
                    print("✓ Added cloudinary_public_id column")

                if 'cloudinary_url' not in columns:
                    conn.execute(db.text('ALTER TABLE photos ADD COLUMN cloudinary_url VARCHAR(500)'))
                    print("✓ Added cloudinary_url column")

                conn.commit()

            print("Migration completed successfully!")
            print("\nNote: To enable Cloudinary storage, set these environment variables:")
            print("  CLOUDINARY_CLOUD_NAME=your_cloud_name")
            print("  CLOUDINARY_API_KEY=your_api_key")
            print("  CLOUDINARY_API_SECRET=your_api_secret")
        else:
            print("Columns already exist. No migration needed.")

if __name__ == '__main__':
    migrate()
