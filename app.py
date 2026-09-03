import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from loader import bot, dp
from handlers import start as start_handlers
from handlers import admin

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=logging.INFO,
    )

    # Подключаем роутер с твоей логикой
    dp.include_router(start_handlers.router)
    
    # Подключаем админ-роутер
    dp.include_router(admin.router)

    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Бот запущен...")
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Бот остановлен")
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Остановлено пользователем")