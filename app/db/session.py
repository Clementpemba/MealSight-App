from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
import os

# Use SQLite instead of PostgreSQL
# This creates a file called mealsight.db in your project
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./mealsight.db")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    poolclass=NullPool,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session():
    async with async_session_maker() as session:
        yield session