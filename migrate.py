import asyncio
from loader import db_engine
from models.table_models import Base


async def migrate():
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await db_engine.dispose()

asyncio.run(migrate())
