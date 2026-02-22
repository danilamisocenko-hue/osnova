from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from config import ADMINS
from database import (
    get_all_students, add_profits, update_mentor_desc,
    update_join_status, update_mentor_status, get_join_request,
    get_pending_logs, update_log_status, get_log
)
from keyboards import admin_menu_kb, back_admin_kb, log_request_kb
from states import AddProfits, ChangeMentorDesc, ChangeAbout
from states import ChangeStatus as ChangeUserStatus
from states import RejectLog
from filters import is_admin

router = Router()


@router.message(lambda m: m.text == "/admin")
async def admin_panel(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    
    await message.answer("⚙️ Админ-панель:", reply_markup=admin_menu_kb())


@router.callback_query(lambda c: c.data == "admin_back")
async def admin_back(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа!", show_alert=True)
        return
    
    await callback.message.edit_text("⚙️ Админ-панель:", reply_markup=admin_menu_kb())


@router.callback_query(lambda c: c.data == "admin_students")
async def list_students(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    
    students = await get_all_students()
    
    if not students:
        text = "📭 Учеников пока нет."
    else:
        text = "👥 Список учеников:\n\n"
        for s in students:
            mentor = s.get('mentor', 'Без наставника')
            text += f"• {s.get('nickname', 'Нет')} (@{s.get('username', 'нет')}) - {mentor}\n"
    
    await callback.message.edit_text(text, reply_markup=back_admin_kb())


@router.callback_query(lambda c: c.data == "admin_profits")
async def add_profits_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    
    await callback.message.answer("Введите ID пользователя:")
    await state.set_state(AddProfits.user_id)
    await callback.answer()


@router.message(AddProfits.user_id)
async def add_profits_user(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer("Введите число!")
        return
    
    await state.update_data(user_id=user_id)
    await message.answer("Введите сумму профита:")
    await state.set_state(AddProfits.amount)


@router.message(AddProfits.amount)
async def add_profits_finish(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.strip())
    except ValueError:
        await message.answer("Введите число!")
        return
    
    data = await state.get_data()
    await add_profits(data['user_id'], amount)
    await message.answer(f"✅ Профит {amount} RUB добавлен пользователю {data['user_id']}")
    await state.clear()


@router.callback_query(lambda c: c.data == "admin_mentor_desc")
async def edit_mentor_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    
    await callback.message.answer("Введите имя наставника (carlo):")
    await state.set_state(ChangeMentorDesc.mentor)
    await callback.answer()


@router.message(ChangeMentorDesc.mentor)
async def edit_mentor_desc(message: types.Message, state: FSMContext):
    mentor = message.text.strip().lower()
    await state.update_data(mentor=mentor)
    await message.answer("Введите новое описание наставника:")
    await state.set_state(ChangeMentorDesc.description)


@router.message(ChangeMentorDesc.description)
async def edit_mentor_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await update_mentor_desc(data['mentor'], message.text.strip())
    await message.answer("✅ Описание наставника обновлено!")
    await state.clear()


@router.callback_query(lambda c: c.data == "admin_about")
async def edit_about_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    
    await callback.message.answer("Введите новый текст 'О проекте':")
    await state.set_state(ChangeAbout.text)
    await callback.answer()


@router.message(ChangeAbout.text)
async def edit_about_finish(message: types.Message, state: FSMContext):
    from config import ABOUT_TEXT
    ABOUT_TEXT = message.text.strip()
    await message.answer("✅ Текст 'О проекте' обновлён!")
    await state.clear()


@router.callback_query(lambda c: c.data == "admin_status")
async def change_status_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    
    await callback.message.answer("Введите ID пользователя:")
    await state.set_state(ChangeUserStatus.user_id)
    await callback.answer()


@router.message(ChangeUserStatus.user_id)
async def change_status_user(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer("Введите число!")
        return
    
    await state.update_data(user_id=user_id)
    await message.answer("Введите новый статус (approved/rejected):")
    await state.set_state(ChangeUserStatus.status)


@router.message(ChangeUserStatus.status)
async def change_status_finish(message: types.Message, state: FSMContext):
    status = message.text.strip().lower()
    if status not in ['approved', 'rejected']:
        await message.answer("Введите approved или rejected!")
        return
    
    data = await state.get_data()
    await update_join_status(data['user_id'], status)
    await message.answer(f"✅ Статус пользователя {data['user_id']} изменён на {status}")
    await state.clear()


@router.callback_query(lambda c: c.data == "admin_logs")
async def show_logs(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    
    logs = await get_pending_logs()
    
    if not logs:
        text = "📭 Нет pending логов."
    else:
        log = logs[0]
        text = f"""📤 Лог #{log['rowid']}

👤 Пользователь: {log['user_id']}
💰 Кошелёк: {log['wallet_address']}
💵 Баланс: {log['balance']}
📋 Сделка: {log['deal_type']}
📱 Мессенджер: {log['messenger']}
💲 Сумма: {log['amount']} USDT"""
    
    await callback.message.answer(text, reply_markup=log_request_kb())
    await callback.answer()


@router.callback_query(lambda c: c.data == "accept_log")
async def accept_log(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    
    logs = await get_pending_logs()
    if not logs:
        await callback.answer("Нет логов для принятия!", show_alert=True)
        return
    
    log = logs[0]
    log_id = log['rowid']
    
    await update_log_status(log_id, "accepted")
    
    try:
        await callback.bot.send_message(
            log['user_id'],
            "✅ Ваш лог принят! Свяжитесь с главным админом: @ник_админа"
        )
    except:
        pass
    
    await callback.message.edit_text("✅ Лог принят!")
    
    logs = await get_pending_logs()
    if logs:
        log = logs[0]
        text = f"""📤 Лог #{log['rowid']}

👤 Пользователь: {log['user_id']}
💰 Кошелёк: {log['wallet_address']}
💵 Баланс: {log['balance']}
📋 Сделка: {log['deal_type']}
📱 Мессенджер: {log['messenger']}
💲 Сумма: {log['amount']} USDT"""
        await callback.message.answer(text, reply_markup=log_request_kb())
    
    await callback.answer()


@router.callback_query(lambda c: c.data == "reject_log")
async def reject_log_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    
    logs = await get_pending_logs()
    if not logs:
        await callback.answer("Нет логов для отклонения!", show_alert=True)
        return
    
    log = logs[0]
    await state.update_data(log_id=log['rowid'])
    await callback.message.answer("Введите причину отклонения лога:")
    await state.set_state(RejectLog.reason)
    await callback.answer()


@router.message(RejectLog.reason)
async def reject_log_process(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    data = await state.get_data()
    log_id = data.get('log_id', 0)
    reason = message.text.strip()
    
    if log_id == 0:
        logs = await get_pending_logs()
        if logs:
            log_id = logs[0]['rowid']
    
    if log_id:
        await update_log_status(log_id, "rejected", reason)
        
        log = await get_log(log_id)
        if log:
            try:
                await message.bot.send_message(
                    log['user_id'],
                    f"❌ Ваш лог отклонён. Причина: {reason}"
                )
            except:
                pass
    
    await message.answer("✅ Лог отклонён!")
    await state.clear()