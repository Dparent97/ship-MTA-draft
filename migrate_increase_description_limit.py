"""
Migration script to increase description field limit from 500 to 2000 characters.
Run this script once to update the production database schema.

Usage:
    python migrate_increase_description_limit.py
"""

import os
import sys
from sqlalchemy import create_engine, text

def migrate():
    """Increase description column size from VARCHAR(500) to VARCHAR(2000)"""
    
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set!")
        print("\nTo run this migration:")
        print("1. Set DATABASE_URL locally:")
        print("   export DATABASE_URL='postgresql://...'")
        print("2. Or run via Railway CLI:")
        print("   railway run python migrate_increase_description_limit.py")
        sys.exit(1)
    
    # Handle Railway's postgres:// format
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    print(f"Connecting to database...")
    print(f"Database: {database_url.split('@')[1] if '@' in database_url else 'local'}")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check current column type
            result = conn.execute(text("""
                SELECT character_maximum_length 
                FROM information_schema.columns 
                WHERE table_name = 'work_items' 
                AND column_name = 'description'
            """))
            
            current_length = result.fetchone()
            
            if current_length:
                current_length = current_length[0]
                print(f"Current description length: {current_length}")
                
                if current_length == 2000:
                    print("✓ Column already set to VARCHAR(2000). No migration needed.")
                    return
            
            print("\nApplying migration...")
            print("Altering column: description VARCHAR(500) -> VARCHAR(2000)")
            
            # Alter the column type
            conn.execute(text("""
                ALTER TABLE work_items 
                ALTER COLUMN description TYPE VARCHAR(2000)
            """))
            
            conn.commit()
            
            print("✓ Migration successful!")
            print("\nDescription field can now hold up to 2000 characters.")
            
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    print("="*70)
    print("  Database Migration: Increase Description Field Limit")
    print("="*70)
    print()
    
    migrate()
    
    print()
    print("="*70)
    print("  Migration Complete")
    print("="*70)

