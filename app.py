import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database import init_db

from handlers import menu, profile, admin, mentors, join_requests


async def main():
    await init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    dp.include_router(join_requests.router)
    dp.include_router(admin.router)
    dp.include_router(mentors.router)
    dp.include_router(profile.router)
    dp.include_router(menu.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
