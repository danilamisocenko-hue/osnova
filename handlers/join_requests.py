from aiogram import Router, types
from config import TEAM_CHAT_ID
from database import set_join_requested, ensure_user

router = Router()


@router.chat_join_request()
async def on_join_request(req: types.ChatJoinRequest):
    if req.chat.id != TEAM_CHAT_ID:
        return

    user_id = req.from_user.id
    await ensure_user(user_id)
    await set_join_requested(user_id, True)
