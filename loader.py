from settings import bot_token, db_address, pg_user, pg_pass
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from filters.base import AdminFilter
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


bot = Bot(token=bot_token, parse_mode="HTML")
storage = MemoryStorage()
db_engine = create_async_engine(f"postgresql+asyncpg://{pg_user}:{pg_pass}@{db_address}", echo=True)
db_session = sessionmaker(db_engine, expire_on_commit=False, class_=AsyncSession)
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)

"""Register middlewares here before starting up the bot"""
dp.middleware.setup(LoggingMiddleware())

"""Filters"""
dp.filters_factory.bind(AdminFilter)
