import asyncio
from app.db.session import async_session_maker
from app.models.food import Food  # adjust path if needed

async def seed_foods():
    async with async_session_maker() as session:

        # optional check
        existing = await session.execute(
            Food.__table__.select()
        )

        foods = [
            Food(name="Rice", calories=130, protein=2.7, carbs=28),
            Food(name="Fish", calories=206, protein=22, carbs=0),
            Food(name="Nsima", calories=150, protein=3, carbs=33),
        ]

        session.add_all(foods)
        await session.commit()

async def main():
    await seed_foods()

if __name__ == "__main__":
    asyncio.run(main())