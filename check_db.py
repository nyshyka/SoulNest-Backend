"""Quick script to check database connection and status"""
import asyncio
import sys
from sqlalchemy import text
from app.db.session import engine
from app.core.config import settings

async def check_db():
    print(f"Database URL: {settings.database_url.split('@')[1] if '@' in settings.database_url else 'REDACTED'}")
    print("\nAttempting to connect to database...")
    
    try:
        async with engine.begin() as conn:
            # Check if we can connect
            result = await conn.execute(text("SELECT 1"))
            print("✓ Database connection successful!")
            
            # Check if database exists
            result = await conn.execute(text("SELECT DATABASE()"))
            db_name = result.scalar()
            print(f"✓ Connected to database: {db_name}")
            
            # Check if tables exist
            result = await conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            if tables:
                print(f"\n✓ Found {len(tables)} table(s):")
                for table in tables:
                    print(f"  - {table[0]}")
                
                # Check if products table has data
                result = await conn.execute(text("SELECT COUNT(*) FROM products"))
                count = result.scalar()
                print(f"\n✓ Products table has {count} record(s)")
            else:
                print("\n✗ No tables found in database!")
                print("  You need to run the seed script: mysql_seed.sql")
                return False
                
    except Exception as e:
        print(f"\n✗ Database connection failed!")
        print(f"  Error: {str(e)}")
        print(f"\nPossible issues:")
        print(f"  1. Database doesn't exist")
        print(f"  2. Wrong credentials in .env file")
        print(f"  3. MySQL server is not accessible")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(check_db())
    sys.exit(0 if success else 1)





