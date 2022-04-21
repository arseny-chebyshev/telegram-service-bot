from loader import dp
from aiogram import executor
from handlers.admin.base import send_to_admin, shutdown
import logging


logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=send_to_admin, on_shutdown=shutdown)
