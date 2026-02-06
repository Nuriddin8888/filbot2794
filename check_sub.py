from aiogram import Bot
from config import CHANNEL_ID

async def check_subbed_user(bot: Bot, user_id: int):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)

        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False

    except Exception:
        return False
