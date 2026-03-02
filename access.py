from aiogram.exceptions import TelegramBadRequest
from config import CHANNEL_ID, TEAM_CHAT_ID

ALLOWED = {"member", "administrator", "creator"}


async def is_subscribed(bot, user_id: int) -> bool:
    try:
        m = await bot.get_chat_member(CHANNEL_ID, user_id)
        return m.status in ALLOWED
    except TelegramBadRequest:
        # бот не может проверить канал (не админ / нет доступа)
        return False


async def is_in_team_chat(bot, user_id: int) -> bool:
    try:
        m = await bot.get_chat_member(TEAM_CHAT_ID, user_id)
        return m.status in ALLOWED
    except TelegramBadRequest:
        return False
