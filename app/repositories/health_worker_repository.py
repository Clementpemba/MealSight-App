from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.health_worker import HealthWorker, HealthWorkerAssignment
from app.repositories.base_repository import BaseRepository


class HealthWorkerRepository(BaseRepository[HealthWorker]):
    """Repository for HealthWorker model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, HealthWorker)
    
    async def get_by_email(self, email: str) -> Optional[HealthWorker]:
        """Get a health worker by email."""
        result = await self.db.execute(
            select(HealthWorker).where(HealthWorker.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_verified(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[HealthWorker]:
        """Get all verified health workers."""
        result = await self.db.execute(
            select(HealthWorker)
            .where(HealthWorker.is_verified == True)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_facility(
        self, 
        facility_name: str
    ) -> List[HealthWorker]:
        """Get health workers by facility."""
        result = await self.db.execute(
            select(HealthWorker)
            .where(HealthWorker.facility_name == facility_name)
        )
        return list(result.scalars().all())
    
    async def email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        return await self.exists(email=email)


class HealthWorkerAssignmentRepository(BaseRepository[HealthWorkerAssignment]):
    """Repository for HealthWorkerAssignment model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, HealthWorkerAssignment)
    
    async def get_by_health_worker(
        self, 
        health_worker_id: int,
        active_only: bool = True
    ) -> List[HealthWorkerAssignment]:
        """Get all assignments for a health worker."""
        query = select(HealthWorkerAssignment).where(
            HealthWorkerAssignment.health_worker_id == health_worker_id
        )
        
        if active_only:
            query = query.where(HealthWorkerAssignment.is_active == True)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_user(
        self, 
        user_id: int,
        active_only: bool = True
    ) -> List[HealthWorkerAssignment]:
        """Get all assignments for a user."""
        query = select(HealthWorkerAssignment).where(
            HealthWorkerAssignment.user_id == user_id
        )
        
        if active_only:
            query = query.where(HealthWorkerAssignment.is_active == True)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_assignment(
        self, 
        health_worker_id: int, 
        user_id: int
    ) -> Optional[HealthWorkerAssignment]:
        """Get a specific assignment."""
        result = await self.db.execute(
            select(HealthWorkerAssignment).where(
                and_(
                    HealthWorkerAssignment.health_worker_id == health_worker_id,
                    HealthWorkerAssignment.user_id == user_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def deactivate_assignment(
        self, 
        health_worker_id: int, 
        user_id: int
    ) -> bool:
        """Deactivate an assignment."""
        assignment = await self.get_assignment(health_worker_id, user_id)
        if assignment:
            await self.update(assignment.id, {"is_active": False})
            return True
        return False
