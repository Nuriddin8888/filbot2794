from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_LINK

def sub_keyboard(not_subbed):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text="📢 Kanalga kirish",
            url=CHANNEL_LINK
        )
    ])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")
    ])

    return keyboard
