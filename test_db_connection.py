"""Test database connection and identify issues"""
import asyncio
import sys
from sqlalchemy import text
from app.db.session import AsyncSessionLocal, engine
from app.core.config import settings


async def test_connection():
    """Test database connection"""
    print("=" * 50)
    print("Testing Database Connection")
    print("=" * 50)
    
    # Test 1: Check settings
    print(f"\n1. Database URL: {settings.database_url}")
    print(f"   JWT Secret: {'✓ Set' if settings.jwt_secret_key else '✗ Missing'}")
    
    # Test 2: Test connection
    print("\n2. Testing connection...")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("   ✓ Connection successful!")
    except Exception as e:
        print(f"   ✗ Connection failed: {e}")
        return False
    
    # Test 3: Check if database exists
    print("\n3. Checking database...")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT DATABASE()"))
            db_name = result.scalar()
            print(f"   ✓ Connected to database: {db_name}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 4: Check if tables exist
    print("\n4. Checking tables...")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            print(f"   ✓ Found {len(tables)} tables:")
            for table in tables:
                print(f"     - {table}")
            
            required_tables = ['users', 'categories', 'products', 'product_images']
            missing = [t for t in required_tables if t not in tables]
            if missing:
                print(f"\n   ✗ Missing tables: {missing}")
                return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 5: Test a simple query
    print("\n5. Testing queries...")
    try:
        async with AsyncSessionLocal() as session:
            # Test categories
            result = await session.execute(text("SELECT COUNT(*) FROM categories"))
            cat_count = result.scalar()
            print(f"   ✓ Categories: {cat_count} found")
            
            # Test products
            result = await session.execute(text("SELECT COUNT(*) FROM products"))
            prod_count = result.scalar()
            print(f"   ✓ Products: {prod_count} found")
            
            # Test featured products
            result = await session.execute(text("SELECT COUNT(*) FROM products WHERE is_featured = TRUE"))
            featured_count = result.scalar()
            print(f"   ✓ Featured products: {featured_count} found")
            
            # Test bestsellers
            result = await session.execute(text("SELECT COUNT(*) FROM products WHERE is_bestseller = TRUE"))
            bestseller_count = result.scalar()
            print(f"   ✓ Bestsellers: {bestseller_count} found")
    except Exception as e:
        print(f"   ✗ Query error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 50)
    print("✓ All tests passed!")
    print("=" * 50)
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(test_connection())
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

