import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import load_config
from bot.handlers import contact, fallback, quiz, result, start


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    config = load_config()

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher(config=config)
    dispatcher.include_routers(
        start.router,
        quiz.router,
        result.router,
        contact.router,
        fallback.router,
    )

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
