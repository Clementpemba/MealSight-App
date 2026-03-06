from typing import Optional, List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.growth_record import GrowthRecord
from app.repositories.base_repository import BaseRepository


class GrowthRecordRepository(BaseRepository[GrowthRecord]):
    """Repository for GrowthRecord model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, GrowthRecord)
    
    async def get_by_child(
        self, 
        child_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[GrowthRecord]:
        """Get all growth records for a child."""
        result = await self.db.execute(
            select(GrowthRecord)
            .where(GrowthRecord.child_id == child_id)
            .order_by(GrowthRecord.recorded_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_latest_by_child(self, child_id: int) -> Optional[GrowthRecord]:
        """Get the most recent growth record for a child."""
        result = await self.db.execute(
            select(GrowthRecord)
            .where(GrowthRecord.child_id == child_id)
            .order_by(GrowthRecord.recorded_date.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    async def get_by_date_range(
        self,
        child_id: int,
        start_date: date,
        end_date: date
    ) -> List[GrowthRecord]:
        """Get growth records within a date range."""
        result = await self.db.execute(
            select(GrowthRecord).where(
                and_(
                    GrowthRecord.child_id == child_id,
                    GrowthRecord.recorded_date >= start_date,
                    GrowthRecord.recorded_date <= end_date
                )
            ).order_by(GrowthRecord.recorded_date)
        )
        return list(result.scalars().all())
    
    async def get_by_child_and_date(
        self, 
        child_id: int, 
        recorded_date: date
    ) -> Optional[GrowthRecord]:
        """Get growth record for a child on a specific date."""
        result = await self.db.execute(
            select(GrowthRecord).where(
                and_(
                    GrowthRecord.child_id == child_id,
                    GrowthRecord.recorded_date == recorded_date
                )
            )
        )
        return result.scalar_one_or_none()
