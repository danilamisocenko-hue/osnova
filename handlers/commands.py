from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import MAIN_MENU_IMAGE, ADMINS
from database import is_approved, get_join_request, create_join_request, update_join_status
from keyboards import main_menu_kb, join_request_kb
from states import JoinSurvey

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or "Без username"
    await state.clear()
    
    if await is_approved(user_id):
        await message.answer_photo(photo=MAIN_MENU_IMAGE, caption="Добро пожаловать в CAMORRA TEAM!", reply_markup=main_menu_kb())
        return
    
    request = await get_join_request(user_id)
    
    if request:
        status = request['status']
        if status == 'approved':
            await update_join_status(user_id, 'approved')
            await message.answer_photo(photo=MAIN_MENU_IMAGE, caption="Добро пожаловать в CAMORRA TEAM!", reply_markup=main_menu_kb())
        elif status == 'pending':
            await message.answer("Ваша заявка на рассмотрении. Ожидайте.")
        else:
            await message.answer("Ваша заявка отклонена. Свяжитесь с админами.")
    else:
        await message.answer("Вас приветствует команда CAMORRA TEAM\n\nЧтобы попасть в команду ответьте на несколько вопросов\n\n1) Откуда о нас узнал?")
        await state.set_state(JoinSurvey.source)

@router.message(JoinSurvey.source)
async def survey_source(message: types.Message, state: FSMContext):
    await state.update_data(source=message.text)
    await message.answer("2) Сколько времени в сфере и какие результаты?")
    await state.set_state(JoinSurvey.experience)

@router.message(JoinSurvey.experience)
async def survey_exp(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("3) Сколько времени готов уделять работе?")
    await state.set_state(JoinSurvey.time)

@router.message(JoinSurvey.time)
async def survey_time(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    username = message.from_user.username or "Без username"
    
    await create_join_request(user_id, username, data['source'], data['experience'], message.text)
    await message.answer("Ваша заявка подана. Ожидайте одобрения.")
    await state.clear()
    
    answers = f"1) {data['source']}\n2) {data['experience']}\n3) {message.text}"
    
    for admin_id in ADMINS:
        try:
            await message.bot.send_message(admin_id, f"📝 Новая заявка от @{username} (ID: {user_id})\n\nОтветы:\n{answers}", reply_markup=join_request_kb(user_id))
        except:
            pass