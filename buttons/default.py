from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


phone_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqamim 📞", request_contact=True)
        ]
    ], resize_keyboard=True
)

