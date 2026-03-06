from typing import TypeVar, Generic, Type, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(Generic[ModelType]):
    """
    Base repository with common CRUD operations.
    
    Provides type-safe database operations using SQLAlchemy async.
    """
    
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self.db = db
        self.model = model
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        **filters
    ) -> List[ModelType]:
        """Get all records with optional pagination and filters."""
        query = select(self.model)
        
        # Apply filters
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.where(getattr(self.model, key) == value)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def create(self, obj_in: dict) -> ModelType:
        """Create a new record."""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
    
    async def update(
        self, 
        id: int, 
        obj_in: dict
    ) -> Optional[ModelType]:
        """Update a record by ID."""
        # Remove None values
        update_data = {k: v for k, v in obj_in.items() if v is not None}
        
        if not update_data:
            return await self.get_by_id(id)
        
        await self.db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
        )
        await self.db.commit()
        return await self.get_by_id(id)
    
    async def delete(self, id: int) -> bool:
        """Delete a record by ID."""
        result = await self.db.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def count(self, **filters) -> int:
        """Count records with optional filters."""
        from sqlalchemy import func
        
        query = select(func.count()).select_from(self.model)
        
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.where(getattr(self.model, key) == value)
        
        result = await self.db.execute(query)
        return result.scalar_one()
    
    async def exists(self, **filters) -> bool:
        """Check if a record exists with given filters."""
        from sqlalchemy import exists as sql_exists
        
        query = select(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.where(getattr(self.model, key) == value)
        
        result = await self.db.execute(
            select(sql_exists(query))
        )
        return result.scalar_one()
