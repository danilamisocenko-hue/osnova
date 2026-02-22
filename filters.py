from aiogram import types
from config import ADMINS
from database import is_approved

def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

async def check_access(callback: types.CallbackQuery) -> bool:
    user_id = callback.from_user.id
    if not await is_approved(user_id):
        await callback.answer("Ваша заявка ещё не одобрена!", show_alert=True)
        return False
    return True