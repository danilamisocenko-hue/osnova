from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="📱 Профиль", callback_data="menu:profile")
    kb.button(text="💬 Чаты", callback_data="menu:chats")
    kb.button(text="👨‍🏫 Наставники", callback_data="menu:mentors")
    kb.button(text="ℹ️ О проекте", callback_data="menu:about")
    kb.adjust(2, 2)
    return kb.as_markup()


def profile_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="✏️ Изменить ник", callback_data="profile:edit_nick")
    kb.button(text="📝 Изменить описание", callback_data="profile:edit_desc")
    kb.button(text="⬅️ Назад", callback_data="menu:home")
    kb.adjust(2, 1)
    return kb.as_markup()


def chats_section_kb(manual, team_chat, payouts, docs, spheres, tools, examples):
    kb = InlineKeyboardBuilder()
    kb.button(text="📘 Мануал", url=manual)
    kb.button(text="💬 Чат команды", url=team_chat)
    kb.button(text="💰 Выплаты", url=payouts)
    kb.button(text="📄 Документы", url=docs)
    kb.button(text="🎯 Сферы и направления", url=spheres)
    kb.button(text="🛠 Инструменты", url=tools)
    kb.button(text="📝 Примеры переписок", url=examples)
    kb.button(text="⬅️ Назад", callback_data="menu:home")
    kb.adjust(2, 2, 2, 1, 1)
    return kb.as_markup()


def mentors_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="👨 Carlo", callback_data="mentor:info:carlo")
    kb.button(text="⬅️ Назад", callback_data="menu:home")
    kb.adjust(1, 1)
    return kb.as_markup()


def mentor_info_kb(mentor: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Подать заявку", callback_data=f"mentor:req:{mentor}")
    kb.button(text="⬅️ Назад", callback_data="menu:mentors")
    kb.adjust(1, 1)
    return kb.as_markup()


def mentor_request_admin_kb(user_id: int, mentor: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Принять", callback_data=f"mentor_accept:{user_id}:{mentor}")
    kb.button(text="❌ Отклонить", callback_data=f"mentor_deny:{user_id}:{mentor}")
    kb.adjust(2)
    return kb.as_markup()


def access_kb(channel_link: str, chat_link: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="📢 Подписаться на канал", url=channel_link)
    kb.button(text="💬 Подать заявку в чат", url=chat_link)
    kb.adjust(1, 1)
    return kb.as_markup()
