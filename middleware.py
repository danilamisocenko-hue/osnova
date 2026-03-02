from functools import wraps
from aiogram import types

from config import CHANNEL_LINK, TEAM_CHAT_LINK
from keyboards import access_kb
from access import is_subscribed, is_in_team_chat
from database import has_join_requested


def require_access(handler):
    @wraps(handler)
    async def wrapper(event, *args, **kwargs):
        # event может быть Message или CallbackQuery
        if isinstance(event, types.CallbackQuery):
            user_id = event.from_user.id
            bot = event.bot
            responder = event.message
        else:
            user_id = event.from_user.id
            bot = event.bot
            responder = event

        # 1) подписка на канал
        if not await is_subscribed(bot, user_id):
            await responder.answer(
                "❗ Чтобы пользоваться ботом, подпишись на канал.",
                reply_markup=access_kb(CHANNEL_LINK, TEAM_CHAT_LINK),
            )
            if isinstance(event, types.CallbackQuery):
                await event.answer()
            return

        # 2) в чате или подавал заявку
        in_chat = await is_in_team_chat(bot, user_id)
        requested = await has_join_requested(user_id)

        if not in_chat and not requested:
            await responder.answer(
                "❗ Чтобы пользоваться ботом, подай заявку в чат команды (или вступи).",
                reply_markup=access_kb(CHANNEL_LINK, TEAM_CHAT_LINK),
            )
            if isinstance(event, types.CallbackQuery):
                await event.answer()
            return

        return await handler(event, *args, **kwargs)

    return wrapper
