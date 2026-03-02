from aiogram import Router, types, F

from config import (
    ABOUT_TEXT,
    MAIN_MENU_IMAGE, PROFILE_IMAGE, CHATS_IMAGE, MENTORS_IMAGE,
    MANUAL_LINK, TEAM_CHAT_LINK, PAYOUTS_LINK, DOCS_LINK, SPHERES_LINK, TOOLS_LINK, EXAMPLES_LINK,
)
from keyboards import main_menu_kb, chats_section_kb, mentors_kb
from middleware import require_access

router = Router()


@router.message(F.text.in_({"/start", "Старт", "Меню"}))
@require_access
async def start(message: types.Message):
    if MAIN_MENU_IMAGE:
        await message.answer_photo(MAIN_MENU_IMAGE, caption="Главное меню:", reply_markup=main_menu_kb())
    else:
        await message.answer("Главное меню:", reply_markup=main_menu_kb())


@router.callback_query(F.data == "menu:home")
@require_access
async def menu_home(cb: types.CallbackQuery):
    await cb.message.delete()
    if MAIN_MENU_IMAGE:
        await cb.message.answer_photo(MAIN_MENU_IMAGE, caption="Главное меню:", reply_markup=main_menu_kb())
    else:
        await cb.message.answer("Главное меню:", reply_markup=main_menu_kb())


@router.callback_query(F.data == "menu:chats")
@require_access
async def menu_chats(cb: types.CallbackQuery):
    await cb.message.delete()
    text = "💬 Раздел «Чаты» и материалы:\n\nВыберите нужный пункт 👇"
    if CHATS_IMAGE:
        await cb.message.answer_photo(
            CHATS_IMAGE,
            caption=text,
            reply_markup=chats_section_kb(
                MANUAL_LINK, TEAM_CHAT_LINK, PAYOUTS_LINK, DOCS_LINK, SPHERES_LINK, TOOLS_LINK, EXAMPLES_LINK
            ),
        )
    else:
        await cb.message.answer(
            text,
            reply_markup=chats_section_kb(
                MANUAL_LINK, TEAM_CHAT_LINK, PAYOUTS_LINK, DOCS_LINK, SPHERES_LINK, TOOLS_LINK, EXAMPLES_LINK
            ),
        )


@router.callback_query(F.data == "menu:mentors")
@require_access
async def menu_mentors(cb: types.CallbackQuery):
    await cb.message.delete()
    if MENTORS_IMAGE:
        await cb.message.answer_photo(MENTORS_IMAGE, caption="👨‍🏫 Наставники:", reply_markup=mentors_kb())
    else:
        await cb.message.answer("👨‍🏫 Наставники:", reply_markup=mentors_kb())


@router.callback_query(F.data == "menu:about")
@require_access
async def menu_about(cb: types.CallbackQuery):
    await cb.message.delete()
    await cb.message.answer(ABOUT_TEXT, reply_markup=main_menu_kb())
