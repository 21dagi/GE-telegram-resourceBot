import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# MODIFICATION: Import the new 'inline_search' handler
from bot.handlers import admin, user, search, inline_search
from database.firestore_service import setup_firestore
from database.seed import seed_database
from utils.i18n import setup_middleware

load_dotenv()

async def main():
    """Initializes and starts the Telegram bot."""
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=getenv("TELEGRAM_BOT_TOKEN"))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Setup internationalization middleware
    setup_middleware(dp)

    # Include routers
    dp.include_router(user.router)
    dp.include_router(admin.router)
    dp.include_router(search.router)
    # MODIFICATION: Include the new inline_search router
    dp.include_router(inline_search.router)

    # Setup and seed Firestore
    setup_firestore()
    await seed_database()

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())