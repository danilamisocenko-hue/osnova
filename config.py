import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

# --- ОБЯЗАТЕЛЬНО ЗАПОЛНИ ---
# ID канала (пример: -1001234567890)
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1000000000000"))
# ID чата/группы команды (пример: -1009876543210)
TEAM_CHAT_ID = int(os.getenv("TEAM_CHAT_ID", "-1000000000000"))

# Ссылки для кнопок (можно @username или https://t.me/...)
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/your_channel")
TEAM_CHAT_LINK = os.getenv("TEAM_CHAT_LINK", "https://t.me/your_chat")

MANUAL_LINK = os.getenv("MANUAL_LINK", "https://t.me/your_manual_post")
PAYOUTS_LINK = os.getenv("PAYOUTS_LINK", "https://t.me/your_payouts")
DOCS_LINK = os.getenv("DOCS_LINK", "https://t.me/your_docs")
SPHERES_LINK = os.getenv("SPHERES_LINK", "https://t.me/your_spheres")
TOOLS_LINK = os.getenv("TOOLS_LINK", "https://t.me/your_tools")
EXAMPLES_LINK = os.getenv("EXAMPLES_LINK", "https://t.me/your_examples")

# Админы (через запятую в .env: ADMINS=111,222,333)
_raw = os.getenv("ADMINS", "")
ADMINS = {int(x.strip()) for x in _raw.split(",") if x.strip().isdigit()}

# Если не хочешь через .env — можно прямо тут:
# ADMINS = {7788251820, 8042059176, 1132436519}

ABOUT_TEXT = os.getenv(
    "ABOUT_TEXT",
    "О проекте… (тут твой текст)"
)

# Картинки (если у тебя через file_id — оставь свои)
MAIN_MENU_IMAGE = os.getenv("MAIN_MENU_IMAGE", "")
PROFILE_IMAGE = os.getenv("PROFILE_IMAGE", "")
CHATS_IMAGE = os.getenv("CHATS_IMAGE", "")
MENTORS_IMAGE = os.getenv("MENTORS_IMAGE", "")
BOTS_IMAGE = os.getenv("BOTS_IMAGE", "")
ABOUT_IMAGE = os.getenv("ABOUT_IMAGE", "")

# Боты/ссылки если надо
CHECKER_LINK = os.getenv("CHECKER_LINK", "")
PARSER_LINK = os.getenv("PARSER_LINK", "")
