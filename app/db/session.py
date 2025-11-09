from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Ensure the database URL uses aiomysql driver
db_url = settings.database_url
# Fix common incorrect URL formats
if db_url.startswith("mysql+pymysql://"):
    db_url = db_url.replace("mysql+pymysql://", "mysql+aiomysql://", 1)
    logger.info(f"Database URL updated from pymysql to aiomysql")
elif db_url.startswith("mysql://"):
    db_url = db_url.replace("mysql://", "mysql+aiomysql://", 1)
    logger.info(f"Database URL updated to use aiomysql")
elif not db_url.startswith("mysql+aiomysql://"):
    logger.warning(f"Database URL format may be incorrect: {db_url}")

# Create async engine with explicit aiomysql driver
# Note: aiomysql handles charset in the URL, not connect_args
engine = create_async_engine(
    db_url,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=3600,
    # aiomysql-specific settings
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

