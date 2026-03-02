from aiogram import Router, types, F
from config import PROFILE_IMAGE
from keyboards import profile_kb, main_menu_kb
from database import get_user, ensure_user
from middleware import require_access

router = Router()


@router.callback_query(F.data == "menu:profile")
@require_access
async def show_profile(cb: types.CallbackQuery):
    user_id = cb.from_user.id
    await ensure_user(user_id)
    u = await get_user(user_id)

    nick = u.get("nickname") or "Не установлен"
    desc = u.get("description") or "Нет"
    mentor = u.get("mentor") or "Не назначен"

    # кликабельная ссылка по id
    user_link = f'<a href="tg://user?id={user_id}">{user_id}</a>'

    text = (
        f"👤 Ник: {nick}\n"
        f"🆔 ID: {user_link}\n\n"
        f"📝 Описание: {desc}\n"
        f"👨‍🏫 Наставник: {mentor}\n"
    )

    await cb.message.delete()
    if PROFILE_IMAGE:
        await cb.message.answer_photo(PROFILE_IMAGE, caption=text, parse_mode="HTML", reply_markup=profile_kb())
    else:
        await cb.message.answer(text, parse_mode="HTML", reply_markup=profile_kb())


@router.callback_query(F.data == "profile:edit_nick")
@require_access
async def edit_nick(cb: types.CallbackQuery):
    await cb.answer("Сделай обработчик изменения ника (если нужно).", show_alert=True)


@router.callback_query(F.data == "profile:edit_desc")
@require_access
async def edit_desc(cb: types.CallbackQuery):
    await cb.answer("Сделай обработчик изменения описания (если нужно).", show_alert=True)
