import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env!")

CHAT_LINK = "https://t.me/camorra_team_bot"
# Раздел «Чаты» / материалы (замени на свои ссылки)
MANUAL_LINK = "https://telegra.ph/Manualy-komandy-𝐶𝐴𝑀𝑂𝑅𝑅𝐴-𝑇𝐸𝐴𝑀-11-21"  # Мануал (поставь ссылку на пост/файл/канал)
PAYOUTS_LINK = "https://t.me/+LqhNOS_Fna0wMzIy"  # Выплаты
DOCS_LINK = "https://t.me/+c6y-N-Ng8CA2NWRl"     # Документы
SPHERES_LINK = "https://t.me/+TOhK7La87YU1YTdl"  # Сферы и направления
TOOLS_LINK = "https://t.me/+cicKFe3d7gdiZjll"    # Инструменты
EXAMPLES_LINK = "https://t.me/+aqKTc9bQHho0OTFk" # Примеры переписок
CHECKER_LINK = "https://t.me/Chekercamorra_bot"
PARSER_LINK = "https://t.me/your_parser_link"

ABOUT_TEXT = """Добро пожаловать в Проект CAMORRA!

Рады приветствовать вас в официальном канале нашего Проекта.
Мы фокусируемся на самом актуальном и перспективном направлении рынка.

Наша структура предлагает:

· Обучение для участников любого уровня (от новичков до профи).
· Выстроенную систему действий для быстрого и гарантированного результата.

Важно: Для оптимизации работы, пожалуйста, внимательно изучите закрепленные материалы (мануал) перед обращением к администрации.

Желаем вам высокой продуктивности и достижения целей!"""

ADMINS = [7788251820, 8042059176, 1132436519]

MAIN_MENU_IMAGE = "AgACAgIAAxkBAAIBFWmXITLkwchxI9KLG2ueK0bH7s_OAAJCFGsbTamwSCmGnS4LGlZIAQADAgADeQADOgQ"
PROFILE_IMAGE = "AgACAgIAAxkBAAIBE2mXISw_V0d47jvc3jhyLaUKIHw0AAJDFGsbTamwSMCGySgd7peyAQADAgADeQADOgQ"
ABOUT_IMAGE = "AgACAgIAAxkBAAIBEWmXISmf9x3YMdHtwIsSMgGu2oxbAAI-FGsbTamwSGJovmLt-BWDAQADAgADeQADOgQ"
CHATS_IMAGE = "AgACAgIAAxkBAAIBD2mXISWtgywZJQnjrFmrPgTboCKqAAI_FGsbTamwSIbiSpXdsTOzAQADAgADeQADOgQ"
MENTORS_IMAGE = "AgACAgIAAxkBAAIBDWmXISHFpoxmpUB2VF2mTNEZ7xV9AAJAFGsbTamwSFrnGTTGM1k0AQADAgADeQADOgQ"
BOTS_IMAGE = "AgACAgIAAxkBAAIBC2mXIQfgIsoabShUHrkSGnepU_76AAJBFGsbTamwSO39UhADcbJVAQADAgADeQADOgQ"

