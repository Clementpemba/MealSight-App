from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, update

from app.models.nutrition_alert import NutritionAlert
from app.repositories.base_repository import BaseRepository


class NutritionAlertRepository(BaseRepository[NutritionAlert]):
    """Repository for NutritionAlert model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, NutritionAlert)
    
    async def get_by_user(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 50,
        unread_only: bool = False
    ) -> List[NutritionAlert]:
        """Get alerts for a user."""
        query = select(NutritionAlert).where(NutritionAlert.user_id == user_id)
        
        if unread_only:
            query = query.where(NutritionAlert.is_read == False)
        
        result = await self.db.execute(
            query.order_by(NutritionAlert.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_child(
        self, 
        child_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[NutritionAlert]:
        """Get alerts for a child."""
        result = await self.db.execute(
            select(NutritionAlert)
            .where(NutritionAlert.child_id == child_id)
            .order_by(NutritionAlert.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_unread_count(self, user_id: int) -> int:
        """Get count of unread alerts for a user."""
        result = await self.db.execute(
            select(func.count(NutritionAlert.id)).where(
                and_(
                    NutritionAlert.user_id == user_id,
                    NutritionAlert.is_read == False
                )
            )
        )
        return result.scalar_one()
    
    async def mark_as_read(self, alert_id: int) -> bool:
        """Mark an alert as read."""
        await self.db.execute(
            update(NutritionAlert)
            .where(NutritionAlert.id == alert_id)
            .values(is_read=True)
        )
        await self.db.commit()
        return True
    
    async def mark_all_as_read(self, user_id: int) -> int:
        """Mark all alerts for a user as read."""
        result = await self.db.execute(
            update(NutritionAlert)
            .where(
                and_(
                    NutritionAlert.user_id == user_id,
                    NutritionAlert.is_read == False
                )
            )
            .values(is_read=True)
        )
        await self.db.commit()
        return result.rowcount
    
    async def get_by_severity(
        self, 
        user_id: int, 
        severity: str
    ) -> List[NutritionAlert]:
        """Get alerts by severity level."""
        result = await self.db.execute(
            select(NutritionAlert).where(
                and_(
                    NutritionAlert.user_id == user_id,
                    NutritionAlert.severity == severity
                )
            ).order_by(NutritionAlert.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def get_stats(self, user_id: int) -> dict:
        """Get alert statistics for a user."""
        result = await self.db.execute(
            select(
                func.count(NutritionAlert.id).label("total"),
                func.sum(
                    func.cast(NutritionAlert.is_read == False, Integer)
                ).label("unread"),
            ).where(NutritionAlert.user_id == user_id)
        )
        row = result.one()
        
        # Get counts by severity
        severity_counts = {}
        for sev in ["low", "medium", "high", "critical"]:
            count_result = await self.db.execute(
                select(func.count(NutritionAlert.id)).where(
                    and_(
                        NutritionAlert.user_id == user_id,
                        NutritionAlert.severity == sev
                    )
                )
            )
            severity_counts[f"{sev}_count"] = count_result.scalar_one()
        
        return {
            "total_alerts": row.total or 0,
            "unread_count": row.unread or 0,
            **severity_counts,
        }


from sqlalchemy import Integer
