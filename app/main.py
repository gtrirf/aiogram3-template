import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.routers import setup_routers
from app.logging import setup_logging


async def on_startup(bot: Bot):
    if not settings.admins:
        return

    text = "✅Bot launched"
    for admin_id in settings.admins:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            logging.error(f"Startup message failed for {admin_id}: {e}")


async def on_shutdown(bot: Bot):
    if not settings.admins:
        return

    text = "⛔️ Bot has stopped"
    for admin_id in settings.admins:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            logging.error(f"Shutdown message failed for {admin_id}: {e}")


async def main():
    setup_logging(logging.INFO)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_router(setup_routers())

    dp.startup.register(lambda: on_startup(bot))
    dp.shutdown.register(lambda: on_shutdown(bot))

    logging.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())