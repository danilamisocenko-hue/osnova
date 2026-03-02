import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

# --- ОБЯЗАТЕЛЬНО ЗАПОЛНИ ---
# ID канала (пример: -1001234567890)
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1001778858497"))
# ID чата/группы команды (пример: -1009876543210)
TEAM_CHAT_ID = int(os.getenv("TEAM_CHAT_ID", "-1003194899292"))

# Ссылки для кнопок (можно @username или https://t.me/...)
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/+BnWTyWGtwVszMGQy")
TEAM_CHAT_LINK = os.getenv("TEAM_CHAT_LINK", "https://t.me/+seEr0-t4iDJkZmFi")

MANUAL_LINK = os.getenv("MANUAL_LINK", "https://telegra.ph/Manualy-komandy-𝐶𝐴𝑀𝑂𝑅𝑅𝐴-𝑇𝐸𝐴𝑀-11-21")
PAYOUTS_LINK = os.getenv("PAYOUTS_LINK", "https://t.me/+LqhNOS_Fna0wMzIy")
DOCS_LINK = os.getenv("DOCS_LINK", "https://t.me/+c6y-N-Ng8CA2NWRl")
SPHERES_LINK = os.getenv("SPHERES_LINK", "https://t.me/+TOhK7La87YU1YTdl")
TOOLS_LINK = os.getenv("TOOLS_LINK", "https://t.me/+cicKFe3d7gdiZjll")
EXAMPLES_LINK = os.getenv("EXAMPLES_LINK", "https://t.me/+aqKTc9bQHho0OTFk")

# Админы (через запятую в .env: ADMINS=111,222,333)
_raw = os.getenv("ADMINS", "")
ADMINS = {int(x.strip()) for x in _raw.split(",") if x.strip().isdigit()}

# Если не хочешь через .env — можно прямо тут:
 ADMINS = {7788251820, 8042059176,}

ABOUT_TEXT = os.getenv(
    "ABOUT_TEXT",
    "Добро пожаловать в Проект CAMORRA!

Рады приветствовать вас в официальном канале нашего Проекта.
Мы фокусируемся на самом актуальном и перспективном направлении рынка.

Наша структура предлагает:

· Обучение для участников любого уровня (от новичков до профи).
· Выстроенную систему действий для быстрого и гарантированного результата.

Важно: Для оптимизации работы, пожалуйста, внимательно изучите закрепленные материалы (мануал) перед обращением к администрации.

Желаем вам высокой продуктивности и достижения целей!"
)

# Картинки (если у тебя через file_id — оставь свои)
MAIN_MENU_IMAGE = os.getenv("MAIN_MENU_IMAGE", "AgACAgIAAxkBAAIBFWmXITLkwchxI9KLG2ueK0bH7s_OAAJCFGsbTamwSCmGnS4LGlZIAQADAgADeQADOgQ")
PROFILE_IMAGE = os.getenv("PROFILE_IMAGE", "AgACAgIAAxkBAAIBE2mXISw_V0d47jvc3jhyLaUKIHw0AAJDFGsbTamwSMCGySgd7peyAQADAgADeQADOgQ")
CHATS_IMAGE = os.getenv("CHATS_IMAGE", ""AgACAgIAAxkBAAIBD2mXISWtgywZJQnjrFmrPgTboCKqAAI_FGsbTamwSIbiSpXdsTOzAQADAgADeQADOgQ")
MENTORS_IMAGE = os.getenv("MENTORS_IMAGE", "AgACAgIAAxkBAAIBDWmXISHFpoxmpUB2VF2mTNEZ7xV9AAJAFGsbTamwSFrnGTTGM1k0AQADAgADeQADOgQ")
BOTS_IMAGE = os.getenv("BOTS_IMAGE", "AgACAgIAAxkBAAIBC2mXIQfgIsoabShUHrkSGnepU_76AAJBFGsbTamwSO39UhADcbJVAQADAgADeQADOgQ")
ABOUT_IMAGE = os.getenv("ABOUT_IMAGE", "AgACAgIAAxkBAAIBEWmXISmf9x3YMdHtwIsSMgGu2oxbAAI-FGsbTamwSGJovmLt-BWDAQADAgADeQADOgQ")

# Боты/ссылки если надо
CHECKER_LINK = os.getenv("CHECKER_LINK", "@Chekercamorra_bot")
PARSER_LINK = os.getenv("PARSER_LINK", "")


