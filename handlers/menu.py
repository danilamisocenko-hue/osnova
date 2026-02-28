from aiogram import Router, types

from config import (
    MAIN_MENU_IMAGE, PROFILE_IMAGE, CHATS_IMAGE, BOTS_IMAGE,
    MENTORS_IMAGE, ABOUT_TEXT,
    CHAT_LINK, CHECKER_LINK, PARSER_LINK,
    MANUAL_LINK, PAYOUTS_LINK, DOCS_LINK, SPHERES_LINK, TOOLS_LINK, EXAMPLES_LINK
)
from database import is_approved, get_user, get_mentor, get_user_logs_count
from keyboards import (
    main_menu_kb, profile_kb, chats_section_kb, bots_kb,
    mentors_kb, mentor_info_kb
)
from filters import check_access

router = Router()


@router.callback_query(lambda c: c.data == "menu_back")
async def menu_back(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(photo=MAIN_MENU_IMAGE, caption="Главное меню:", reply_markup=main_menu_kb())


@router.callback_query(lambda c: c.data == "menu_profile")
async def show_profile(callback: types.CallbackQuery):
    if not await check_access(callback):
        return

    user_id = callback.from_user.id
    user = await get_user(user_id)

    if not user:
        await callback.answer("Профиль не найден!", show_alert=True)
        return

    nickname = user.get('nickname') or "Не установлен"
    desc = user.get('description') or "Нет"
    profits = user.get('profits') or 0
    count = user.get('profits_count') or 0
    avg = profits / count if count > 0 else 0
    join_date = user.get('join_date') or "Неизвестно"
    logs_count = await get_user_logs_count(user_id)

    text = (
        f"👤 {nickname} (ID: {user_id})\n\n"
        f"📝 Описание: {desc}\n\n"
        f"💰 Профиты: {count} шт. на {profits:.2f} RUB\n"
        f"📊 Средний: {avg:.2f} RUB\n\n"
        f"📤 Логов: {logs_count}\n\n"
        f"📅 В команде с: {join_date}"
    )

    await callback.message.delete()
    await callback.message.answer_photo(photo=PROFILE_IMAGE, caption=text, reply_markup=profile_kb())


@router.callback_query(lambda c: c.data == "menu_chats")
async def show_chats(callback: types.CallbackQuery):
    if not await check_access(callback):
        return

    await callback.message.delete()
    await callback.message.answer_photo(
        photo=CHATS_IMAGE,
        caption="💬 Раздел «Чаты» и материалы:\n\nВыберите нужный пункт 👇",
        reply_markup=chats_section_kb(
            manual_link=MANUAL_LINK,
            team_chat_link=CHAT_LINK,
            payouts_link=PAYOUTS_LINK,
            docs_link=DOCS_LINK,
            spheres_link=SPHERES_LINK,
            tools_link=TOOLS_LINK,
            examples_link=EXAMPLES_LINK,
        ),
    )


@router.callback_query(lambda c: c.data == "menu_bots")
async def show_bots(callback: types.CallbackQuery):
    if not await check_access(callback):
        return
    await callback.message.delete()
    await callback.message.answer_photo(photo=BOTS_IMAGE, caption="🤖 Боты:", reply_markup=bots_kb(CHECKER_LINK, PARSER_LINK))


@router.callback_query(lambda c: c.data == "menu_mentors")
async def show_mentors(callback: types.CallbackQuery):
    if not await check_access(callback):
        return
    await callback.message.delete()
    await callback.message.answer_photo(photo=MENTORS_IMAGE, caption="👨‍🏫 Наставники:", reply_markup=mentors_kb())


@router.callback_query(lambda c: c.data == "mentor_carlo")
async def show_mentor_info(callback: types.CallbackQuery):
    if not await check_access(callback):
        return

    mentor = await get_mentor("carlo")

    if not mentor:
        await callback.answer("Наставник не найден!", show_alert=True)
        return

    text = "👨 Carlo\n\n" + mentor['description'] + "\n\n📊 Процент от профита: " + str(mentor['percentage']) + "%"

    await callback.message.delete()
    await callback.message.answer(text, reply_markup=mentor_info_kb("carlo"))


@router.callback_query(lambda c: c.data == "menu_about")
async def show_about(callback: types.CallbackQuery):
    if not await check_access(callback):
        return
    await callback.message.delete()
    await callback.message.answer(ABOUT_TEXT, reply_markup=main_menu_kb())
