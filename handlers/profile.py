from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from database import is_approved, update_nickname, update_description, add_log, get_user_logs_count
from keyboards import main_menu_kb, mentor_request_kb, profile_kb, log_request_kb
from states import ChangeNickname, ChangeDescription, TransferLog
from config import ADMINS

router = Router()


@router.callback_query(lambda c: c.data == "edit_nickname")
async def edit_nickname_start(callback: types.CallbackQuery, state: FSMContext):
    if not await is_approved(callback.from_user.id):
        await callback.answer("Ваша заявка ещё не одобрена!", show_alert=True)
        return
    
    await callback.message.answer("✏️ Введите новый никнейм:")
    await state.set_state(ChangeNickname.waiting)
    await callback.answer()


@router.message(ChangeNickname.waiting)
async def edit_nickname_process(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    new_nickname = message.text.strip()
    
    if len(new_nickname) > 50:
        await message.answer("Слишком длинный никнейм! Максимум 50 символов.")
        return
    
    await update_nickname(user_id, new_nickname)
    await message.answer("✅ Никнейм изменён на: " + new_nickname)
    await message.answer("Главное меню:", reply_markup=main_menu_kb())
    await state.clear()


@router.callback_query(lambda c: c.data == "edit_description")
async def edit_desc_start(callback: types.CallbackQuery, state: FSMContext):
    if not await is_approved(callback.from_user.id):
        await callback.answer("Ваша заявка ещё не одобрена!", show_alert=True)
        return
    
    await callback.message.answer("📝 Введите новое описание:")
    await state.set_state(ChangeDescription.waiting)
    await callback.answer()


@router.message(ChangeDescription.waiting)
async def edit_desc_process(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    new_desc = message.text.strip()
    
    if len(new_desc) > 500:
        await message.answer("Слишком длинное описание! Максимум 500 символов.")
        return
    
    await update_description(user_id, new_desc)
    await message.answer("✅ Описание изменено!")
    await message.answer("Главное меню:", reply_markup=main_menu_kb())
    await state.clear()


@router.callback_query(lambda c: c.data == "transfer_log")
async def transfer_log_start(callback: types.CallbackQuery, state: FSMContext):
    if not await is_approved(callback.from_user.id):
        await callback.answer("Ваша заявка ещё не одобрена!", show_alert=True)
        return
    
    await callback.message.answer("📤 Передача лога\n\n1) Введите адрес кошелька клиента:")
    await state.set_state(TransferLog.wallet_address)
    await callback.answer()


@router.message(TransferLog.wallet_address)
async def transfer_log_wallet(message: types.Message, state: FSMContext):
    await state.update_data(wallet_address=message.text.strip())
    await message.answer("2) Введите баланс кошелька (от 1500 USDT):")
    await state.set_state(TransferLog.balance)


@router.message(TransferLog.balance)
async def transfer_log_balance(message: types.Message, state: FSMContext):
    await state.update_data(balance=message.text.strip())
    await message.answer("3) Введите название сделки (аренда/покупка) и что покупаете/арендуете:")
    await state.set_state(TransferLog.deal_type)


@router.message(TransferLog.deal_type)
async def transfer_log_deal_type(message: types.Message, state: FSMContext):
    await state.update_data(deal_type=message.text.strip())
    await message.answer("4) Введите номер мессенджера, в котором происходит сделка:")
    await state.set_state(TransferLog.messenger)


@router.message(TransferLog.messenger)
async def transfer_log_messenger(message: types.Message, state: FSMContext):
    await state.update_data(messenger=message.text.strip())
    await message.answer("5) Прикрепите скриншот переписки:")
    await state.set_state(TransferLog.screenshot)


@router.message(TransferLog.screenshot)
async def transfer_log_screenshot(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, прикрепите скриншот (фото):")
        return
    
    screenshot_file_id = message.photo[-1].file_id
    await state.update_data(screenshot=screenshot_file_id)
    await message.answer("6) Введите сумму сделки (в USDT):")
    await state.set_state(TransferLog.amount)


@router.message(TransferLog.amount)
async def transfer_log_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.strip().replace(",", "."))
    except ValueError:
        await message.answer("Введите число! Пример: 1500")
        return
    
    data = await state.get_data()
    user_id = message.from_user.id
    
    await add_log(
        user_id=user_id,
        wallet_address=data['wallet_address'],
        balance=data['balance'],
        deal_type=data['deal_type'],
        deal_item=data['deal_type'],
        messenger=data['messenger'],
        screenshot_file_id=data['screenshot'],
        amount=amount
    )
    
    await message.answer("✅ Лог передан! Ожидайте подтверждения.")
    await message.answer("Главное меню:", reply_markup=main_menu_kb())
    await state.clear()
    
    # Уведомление админам
    text = f"""📤 Новый лог

👤 Пользователь: {message.from_user.id}
💰 Кошелек: {data['wallet_address']}
💵 Баланс: {data['balance']}
📋 Сделка: {data['deal_type']}
📱 Мессенджер: {data['messenger']}
💲 Сумма: {amount} USDT"""
    
    for admin_id in ADMINS:
        try:
            await message.bot.send_photo(admin_id, photo=data['screenshot'], caption=text, reply_markup=log_request_kb())
        except Exception as e:
            print(f"Ошибка отправки админу {admin_id}: {e}")


@router.callback_query(lambda c: c.data.startswith("req_mentor_"))
async def request_mentor(callback: types.CallbackQuery):
    if not await is_approved(callback.from_user.id):
        await callback.answer("Ваша заявка ещё не одобрена!", show_alert=True)
        return
    
    mentor_name = callback.data.split("_")[2]
    user_id = callback.from_user.id
    username = callback.from_user.username or "Без username"
    
    from database import create_mentor_request
    await create_mentor_request(user_id, mentor_name)
    
    await callback.message.answer("✅ Заявка наставнику подана! Ожидайте ответа.")
    await callback.answer()
    
    for admin_id in ADMINS:
        try:
            await callback.message.bot.send_message(
                admin_id,
                f"📝 Заявка на наставника от @{username} (ID: {user_id})\n\nНаставник: {mentor_name.capitalize()}",
                reply_markup=mentor_request_kb(user_id, mentor_name)
            )
        except:
            pass