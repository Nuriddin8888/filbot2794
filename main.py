import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardRemove

from config import TOKEN
from buttons.default import phone_btn
from database import init_db, add_user, get_user

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))


dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    user = get_user(user_id)
    if user:
        await message.answer("Film kodini yuboring")
    else:
        await message.answer(f"Assalomu alaykum hurmatli <b>{full_name}</b>\nRo'yxatdan o'ting👇", reply_markup=phone_btn)



@dp.message(F.contact)
async def get_user_conatct(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    phone_number = message.contact.phone_number
    add_user(user_id, full_name, username, phone_number)
    await message.answer("<b><i>Ro'yxatdan o'tdingiz🥳🥳🥳</i>\nFilm kodini yuboring</b>", reply_markup=ReplyKeyboardRemove())


async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())