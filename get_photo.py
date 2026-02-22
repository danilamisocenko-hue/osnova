import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN = "8589733726:AAFM6Cfnhr6-mWWxokr9Bg4mYUGDQyN_5Xk"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(lambda message: message.photo)
async def get_photo_id(message: types.Message):
    await message.reply(f"File ID: {message.photo[-1].file_id}")

async def main():
    print("Бот запущен. Перешли ему фото.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())