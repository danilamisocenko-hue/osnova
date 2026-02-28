from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 Профиль", callback_data="menu_profile")
    builder.button(text="💬 Чаты команды", callback_data="menu_chats")
    builder.button(text="🤖 Боты", callback_data="menu_bots")
    builder.button(text="👨‍🏫 Наставники", callback_data="menu_mentors")
    builder.button(text="ℹ️ О проекте", callback_data="menu_about")
    builder.adjust(2, 3)
    return builder.as_markup()

def profile_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✏️ Изменить никнейм", callback_data="edit_nickname")
    builder.button(text="📝 Изменить описание", callback_data="edit_description")
    builder.button(text="📤 Передать лог", callback_data="transfer_log")
    builder.button(text="⬅️ Назад", callback_data="menu_back")
    builder.adjust(2, 2)
    return builder.as_markup()

def chats_kb(chat_link: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Чат команды", url=chat_link)
    builder.button(text="⬅️ Назад", callback_data="menu_back")
    builder.adjust(1)
    return builder.as_markup()

def chats_section_kb(
    manual_link: str,
    team_chat_link: str,
    payouts_link: str,
    docs_link: str,
    spheres_link: str,
    tools_link: str,
    examples_link: str,
):
    """Раздел «Чаты» — быстрые кнопки на материалы/ресурсы."""
    builder = InlineKeyboardBuilder()
    builder.button(text="📘 Мануал", url=manual_link)
    builder.button(text="💬 Чат команды", url=team_chat_link)
    builder.button(text="💰 Выплаты", url=payouts_link)
    builder.button(text="📄 Документы", url=docs_link)
    builder.button(text="🎯 Сферы и направления", url=spheres_link)
    builder.button(text="🛠 Инструменты", url=tools_link)
    builder.button(text="📝 Примеры переписок", url=examples_link)
    builder.button(text="⬅️ Назад", callback_data="menu_back")
    builder.adjust(2, 2, 2, 1, 1)
    return builder.as_markup()

def bots_kb(checker: str, parser: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="🔍 Чекер", url=checker)
    builder.button(text="📊 Парсер", url=parser)
    builder.button(text="⬅️ Назад", callback_data="menu_back")
    builder.adjust(2, 1)
    return builder.as_markup()

def mentors_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="👨 Carlo", callback_data="mentor_carlo")
    builder.button(text="⬅️ Назад", callback_data="menu_back")
    builder.adjust(1, 1)
    return builder.as_markup()

def mentor_info_kb(mentor_name: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Подать заявку", callback_data="req_mentor_" + mentor_name)
    builder.button(text="⬅️ Назад", callback_data="menu_mentors")
    builder.adjust(1)
    return builder.as_markup()

def admin_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="👥 Список учеников", callback_data="admin_students")
    builder.button(text="💰 Добавить профиты", callback_data="admin_profits")
    builder.button(text="📝 Изменить наставника", callback_data="admin_mentor_desc")
    builder.button(text="📖 Изменить о проекте", callback_data="admin_about")
    builder.button(text="🔄 Изменить статус", callback_data="admin_status")
    builder.button(text="📥 Логи", callback_data="admin_logs")
    builder.button(text="⬅️ Выход", callback_data="menu_back")
    builder.adjust(2, 2, 2, 1)
    return builder.as_markup()

def back_admin_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data="admin_back")
    builder.adjust(1)
    return builder.as_markup()

def join_request_kb(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Одобрить", callback_data="approve_" + str(user_id))
    builder.button(text="❌ Отклонить", callback_data="reject_" + str(user_id))
    builder.adjust(2)
    return builder.as_markup()

def mentor_request_kb(user_id: int, mentor: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Принять", callback_data="accept_" + str(user_id) + "_" + mentor)
    builder.button(text="❌ Отклонить", callback_data="deny_" + str(user_id) + "_" + mentor)
    builder.adjust(2)
    return builder.as_markup()

def log_request_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Принять", callback_data="accept_log")
    builder.button(text="❌ Отклонить", callback_data="reject_log")
    builder.adjust(2)
    return builder.as_markup()
