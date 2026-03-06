"""
Script to drop all tables in the database.
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.config import settings


async def drop_all_tables():
    # Fix for asyncpg: convert sslmode to ssl parameter
    db_url = settings.DATABASE_URL.replace("sslmode=require", "ssl=require")
    engine = create_async_engine(db_url)
    
    async with engine.begin() as conn:
        # Get all table names
        result = await conn.execute(text("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
        """))
        tables = result.fetchall()
        
        if tables:
            # Drop all tables with CASCADE
            table_names = ', '.join([f'"{t[0]}"' for t in tables])
            await conn.execute(text(f"DROP TABLE IF EXISTS {table_names} CASCADE"))
            print(f"Dropped tables: {[t[0] for t in tables]}")
        else:
            print("No tables found to drop.")
    
    await engine.dispose()
    print("Done!")


if __name__ == "__main__":
    asyncio.run(drop_all_tables())
