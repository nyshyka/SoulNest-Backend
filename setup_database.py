"""Script to set up the database - creates database and runs seed script"""
import asyncio
import sys
from pathlib import Path
from sqlalchemy import text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

async def setup_database():
    """Create database and seed it with initial data"""
    print("=" * 60)
    print("SoulNest Database Setup")
    print("=" * 60)
    
    # Parse database URL to get connection info
    db_url = settings.database_url
    print(f"\nDatabase URL: {db_url.split('@')[1] if '@' in db_url else 'REDACTED'}")
    
    # Extract database name from URL
    # Format: mysql+aiomysql://user:pass@host:port/dbname
    if 'mysql+aiomysql://' in db_url:
        db_part = db_url.split('mysql+aiomysql://')[1]
        if '@' in db_part:
            db_name = db_part.split('/')[-1].split('?')[0]
        else:
            db_name = db_part.split('/')[-1].split('?')[0]
    else:
        print("✗ Invalid database URL format")
        return False
    
    print(f"Target database: {db_name}")
    
    # Create sync engine for database creation (can't create DB with async)
    sync_url = db_url.replace('mysql+aiomysql://', 'mysql+pymysql://')
    sync_engine = create_engine(sync_url.rsplit('/', 1)[0] + '/', echo=False)
    
    try:
        # Create database if it doesn't exist
        print("\n1. Creating database...")
        with sync_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            conn.commit()
        print(f"   ✓ Database '{db_name}' ready")
        
        # Now use the async engine to check tables
        print("\n2. Checking tables...")
        async_engine = create_async_engine(settings.database_url, echo=False)
        async with async_engine.begin() as conn:
            result = await conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            
            if tables:
                print(f"   ✓ Found {len(tables)} existing table(s)")
                print("\n   Database already has tables. You can:")
                print("   - Use the existing data, OR")
                print("   - Drop and recreate by running: mysql -u root -p < seeds/mysql_seed.sql")
            else:
                print("   ✗ No tables found")
                print("\n   You need to run the seed script to create tables and data.")
                print("   Run this command (replace with your MySQL path if needed):")
                print(f"   mysql -u root -p < seeds/mysql_seed.sql")
                print("\n   Or use MySQL Workbench to execute seeds/mysql_seed.sql")
                
        async_engine.dispose()
        sync_engine.dispose()
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your .env file has correct DATABASE_URL")
        print("2. Make sure MySQL is running")
        print("3. Verify MySQL username and password are correct")
        print("4. Check MySQL user has CREATE DATABASE permission")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(setup_database())
        if success:
            print("\n" + "=" * 60)
            print("Next steps:")
            print("1. Run the seed script to create tables: mysql -u root -p < seeds/mysql_seed.sql")
            print("2. Start your backend server: uvicorn app.main:app --reload")
            print("3. Test the API: curl http://127.0.0.1:8000/api/products/bestsellers")
            print("=" * 60)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(1)

