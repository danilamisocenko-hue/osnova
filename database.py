import aiosqlite
from typing import Optional, Dict, Any

DB_PATH = "db.sqlite3"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            nickname TEXT,
            description TEXT,
            join_requested INTEGER DEFAULT 0,
            mentor TEXT DEFAULT NULL
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS mentor_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            mentor TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending', -- pending/accepted/denied
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        await db.commit()


async def ensure_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        if not row:
            await db.execute(
                "INSERT INTO users(user_id, nickname, description, join_requested, mentor) VALUES(?,?,?,?,?)",
                (user_id, None, None, 0, None)
            )
            await db.commit()


async def set_join_requested(user_id: int, value: bool = True):
    await ensure_user(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET join_requested=? WHERE user_id=?",
            (1 if value else 0, user_id)
        )
        await db.commit()


async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    await ensure_user(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT user_id, nickname, description, join_requested, mentor FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        if not row:
            return None
        return {
            "user_id": row[0],
            "nickname": row[1],
            "description": row[2],
            "join_requested": bool(row[3]),
            "mentor": row[4],
        }


async def set_user_mentor(user_id: int, mentor: str):
    await ensure_user(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET mentor=? WHERE user_id=?", (mentor, user_id))
        await db.commit()


async def create_mentor_request(user_id: int, mentor: str) -> int:
    await ensure_user(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO mentor_requests(user_id, mentor, status) VALUES(?,?, 'pending')",
            (user_id, mentor)
        )
        await db.commit()
        return cur.lastrowid


async def set_mentor_request_status(user_id: int, mentor: str, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE mentor_requests SET status=? WHERE user_id=? AND mentor=? AND status='pending'",
            (status, user_id, mentor)
        )
        await db.commit()


async def has_join_requested(user_id: int) -> bool:
    u = await get_user(user_id)
    return bool(u and u.get("join_requested"))
