import os
import aiosqlite
from datetime import datetime

DB_NAME = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY, username TEXT, nickname TEXT DEFAULT '',
                approved INTEGER DEFAULT 0, profits REAL DEFAULT 0.0,
                profits_count INTEGER DEFAULT 0, description TEXT DEFAULT '',
                join_date TEXT DEFAULT '', mentor TEXT DEFAULT NULL
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS mentors (
                name TEXT PRIMARY KEY, description TEXT, percentage REAL
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS mentor_requests (
                user_id INTEGER, mentor_name TEXT, status TEXT DEFAULT 'pending',
                PRIMARY KEY (user_id, mentor_name)
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS join_requests (
                user_id INTEGER PRIMARY KEY, username TEXT, status TEXT DEFAULT 'pending',
                source TEXT DEFAULT '', experience TEXT DEFAULT '', time TEXT DEFAULT ''
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                wallet_address TEXT,
                balance TEXT,
                deal_type TEXT,
                deal_item TEXT,
                messenger TEXT,
                screenshot TEXT,
                amount REAL,
                status TEXT DEFAULT 'pending',
                reason TEXT DEFAULT ''
            )
        ''')
        
        await db.execute("DELETE FROM mentors WHERE name = 'tsar'")
        
        carlo_desc = """Привет! Меня зовут Carlo.

Я наставник в CAMORRA TEAM, и моя главная цель — привести тебя к твоему первому (или сотому) результату без выгорания и тупняка.

Немного фактов обо мне:
Более 4 лет я в этой сфере не как наблюдатель, а как игрок. Достигнутый объем кассы — 164.000$. Эти цифры — доказательство того, что моя система работает.

Как я буду тебя вести:

- Всегда на связи: Ты не остаешься один на один с вопросами. Я онлайн с 09:00 до 01:00 МСК.
- Понятный план: Никакой абстракции. Только четкие шаги: куда идти, что писать, как закрывать.
- Работа над качеством: Хочешь, чтобы твои сообщения цепляли? Сделаем анализ диалогов и прокачаем твою убедительность.
- Ежедневная подпитка: Каждый день (пн-вс) скидываю актуальные мысли, тренды и советы, чтобы держать тебя в фокусе.
- Только рабочие инструменты: Делюсь проверенными ссылками, контактами и ресурсами, на которых реально зарабатывать.

Я готов выложиться ради тебя на 100%, но помни: мои знания — это трамплин. Прыгнешь ты или нет, зависит только от твоего желания.

Если готов действовать — идем со мной."""
        
        await db.execute(
            "INSERT OR REPLACE INTO mentors (name, description, percentage) VALUES (?, ?, ?)",
            ("carlo", carlo_desc, 10.0)
        )
        
        await db.commit()
        print("✅ БД готова")

async def is_approved(user_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT approved FROM users WHERE id = ?", (user_id,))
        row = await cursor.fetchone()
        return row and row[0] == 1

async def get_user(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None

async def update_nickname(user_id: int, nickname: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET nickname = ? WHERE id = ?", (nickname, user_id))
        await db.commit()

async def update_description(user_id: int, description: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET description = ? WHERE id = ?", (description, user_id))
        await db.commit()

async def add_profits(user_id: int, amount: float):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET profits = profits + ?, profits_count = profits_count + 1 WHERE id = ?", (amount, user_id))
        await db.commit()

async def get_all_students() -> list:
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT mentor, nickname, id, username FROM users WHERE approved = 1 AND mentor IS NOT NULL ORDER BY mentor")
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]

async def get_join_request(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM join_requests WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None

async def create_join_request(user_id: int, username: str, source: str, experience: str, time: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR REPLACE INTO join_requests (user_id, username, source, experience, time) VALUES (?, ?, ?, ?, ?)", (user_id, username, source, experience, time))
        await db.commit()

async def update_join_status(user_id: int, status: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE join_requests SET status = ? WHERE user_id = ?", (status, user_id))
        if status == 'approved':
            join_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            await db.execute(
                "INSERT OR IGNORE INTO users (id, username, nickname, approved, join_date) VALUES (?, ?, ?, 0, '')",
                (user_id, "Без username", f"Worker{user_id}")
            )
            await db.execute(
                "UPDATE users SET approved = 1, join_date = ? WHERE id = ?",
                (join_date, user_id)
            )
        await db.commit()

async def get_mentor(name: str) -> dict | None:
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM mentors WHERE name = ?", (name,))
        row = await cursor.fetchone()
        return dict(row) if row else None

async def update_mentor_desc(name: str, description: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE mentors SET description = ? WHERE name = ?", (description, name))
        await db.commit()

async def create_mentor_request(user_id: int, mentor_name: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR REPLACE INTO mentor_requests (user_id, mentor_name) VALUES (?, ?)", (user_id, mentor_name))
        await db.commit()

async def update_mentor_status(user_id: int, mentor_name: str, status: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE mentor_requests SET status = ? WHERE user_id = ? AND mentor_name = ?", (status, user_id, mentor_name))
        if status == 'accepted':
            await db.execute("UPDATE users SET mentor = ? WHERE id = ?", (mentor_name, user_id))
        await db.commit()

async def add_log(user_id: int, wallet_address: str, balance: str, deal_type: str, deal_item: str, messenger: str, screenshot_file_id: str, amount: float):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO logs (user_id, wallet_address, balance, deal_type, deal_item, messenger, screenshot, amount, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, wallet_address, balance, deal_type, deal_item, messenger, screenshot_file_id, amount, "pending")
        )
        await db.commit()

async def get_pending_logs():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM logs WHERE status = 'pending' ORDER BY rowid DESC")
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]

async def get_user_logs_count(user_id: int) -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM logs WHERE user_id = ? AND status = 'accepted'", (user_id,))
        row = await cursor.fetchone()
        return row[0] if row else 0

async def update_log_status(log_id: int, status: str, reason: str = ""):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE logs SET status = ?, reason = ? WHERE rowid = ?", (status, reason, log_id))
        await db.commit()

async def get_log(log_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM logs WHERE rowid = ?", (log_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None