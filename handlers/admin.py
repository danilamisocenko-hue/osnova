from aiogram import Router, types, F
from config import ADMINS
from database import set_user_mentor, set_mentor_request_status

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMINS


@router.callback_query(F.data.startswith("mentor_accept:"))
async def mentor_accept(cb: types.CallbackQuery):
    if not is_admin(cb.from_user.id):
        return await cb.answer("Нет доступа", show_alert=True)

    try:
        _, user_id, mentor = cb.data.split(":")
        user_id = int(user_id)
    except Exception:
        return await cb.answer("Ошибка данных", show_alert=True)

    await set_user_mentor(user_id, mentor)
    await set_mentor_request_status(user_id, mentor, "accepted")

    await cb.answer("Принято ✅")
    try:
        await cb.message.edit_text(cb.message.text + "\n\n✅ Заявка принята")
    except:
        pass

    try:
        await cb.bot.send_message(user_id, f"✅ Ваша заявка на наставничество принята!\nНаставник: {mentor}")
    except:
        pass


@router.callback_query(F.data.startswith("mentor_deny:"))
async def mentor_deny(cb: types.CallbackQuery):
    if not is_admin(cb.from_user.id):
        return await cb.answer("Нет доступа", show_alert=True)

    try:
        _, user_id, mentor = cb.data.split(":")
        user_id = int(user_id)
    except Exception:
        return await cb.answer("Ошибка данных", show_alert=True)

    await set_mentor_request_status(user_id, mentor, "denied")

    await cb.answer("Отклонено ❌")
    try:
        await cb.message.edit_text(cb.message.text + "\n\n❌ Заявка отклонена")
    except:
        pass

    try:
        await cb.bot.send_message(user_id, "❌ Ваша заявка на наставничество отклонена.")
    except:
        pass
