from aiogram import Router, types, F
from config import ADMINS
from keyboards import mentor_info_kb, mentor_request_admin_kb
from database import create_mentor_request, ensure_user
from middleware import require_access

router = Router()


@router.callback_query(F.data.startswith("mentor:info:"))
@require_access
async def mentor_info(cb: types.CallbackQuery):
    mentor = cb.data.split(":")[-1]
    text = f"👨‍🏫 Наставник: {mentor}\n\nНажми «Подать заявку», чтобы отправить запрос."
    await cb.message.delete()
    await cb.message.answer(text, reply_markup=mentor_info_kb(mentor))


@router.callback_query(F.data.startswith("mentor:req:"))
@require_access
async def mentor_request(cb: types.CallbackQuery):
    mentor = cb.data.split(":")[-1]
    user_id = cb.from_user.id
    await ensure_user(user_id)

    await create_mentor_request(user_id, mentor)

    user_link = f'<a href="tg://user?id={user_id}">{user_id}</a>'
    admin_text = (
        f"📝 Заявка на наставничество\n\n"
        f"👤 Пользователь: {user_link}\n"
        f"👨‍🏫 Наставник: {mentor}"
    )

    for admin_id in ADMINS:
        try:
            await cb.bot.send_message(
                admin_id,
                admin_text,
                parse_mode="HTML",
                reply_markup=mentor_request_admin_kb(user_id, mentor),
                disable_web_page_preview=True
            )
        except:
            pass

    await cb.answer("Заявка отправлена ✅", show_alert=True)
