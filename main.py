import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from config import TOKEN, ADMIN_ID
from buttons.default import phone_btn
from buttons.inline import sub_keyboard
from database import init_db, add_user, get_user, add_movie, get_movie_code
from state import AdminMovie
from movie_code import generate_move_code
from check_sub import check_subbed_user

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))


dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    # 1. OBUNA TEKSHIRISH
    is_sub = await check_subbed_user(bot, user_id)

    if not is_sub:
        await message.answer(
            "Botdan foydalanish uchun kanalga obuna bo'ling 👇",
            reply_markup=sub_keyboard([])
        )
        return

    # 2. REGISTRATSIYA TEKSHIRISH
    user = get_user(user_id)

    if user:
        await message.answer("Film kodini yuboring")
    else:
        await message.answer(
            f"Assalomu alaykum hurmatli <b>{full_name}</b>\nRo'yxatdan o'ting👇",
            reply_markup=phone_btn
        )



@dp.message(F.contact)
async def get_user_conatct(message: types.Message):

    user_id = message.from_user.id

    # 🔥 AVVAL OBUNA
    is_sub = await check_subbed_user(bot, user_id)

    if not is_sub:
        await message.answer(
            "Avval kanalga obuna bo'ling!",
            reply_markup=sub_keyboard([])
        )
        return

    # ✅ KEYIN REGISTRATSIYA
    full_name = message.from_user.full_name
    username = message.from_user.username
    phone_number = message.contact.phone_number

    add_user(user_id, full_name, username, phone_number)

    await message.answer(
        "<b><i>Ro'yxatdan o'tdingiz🥳🥳🥳</i>\nFilm kodini yuboring</b>",
        reply_markup=ReplyKeyboardRemove()
    )




@dp.callback_query(F.data == "check_sub")
async def check_subbed(callback: types.CallbackQuery):

    is_sub = await check_subbed_user(bot, callback.from_user.id)

    if is_sub:
        await callback.message.answer("Rahmat! Endi botdan foydalana olasiz ✅")
    else:
        await callback.answer("Hali ham obuna bo'lmadingiz!", show_alert=True)


@dp.message(Command("admin"))
async def admin_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if user_id == ADMIN_ID:
        await message.answer("Assalomu alaykum admin xush kelibsiz")
        await message.answer("Film videosini yuboring")
        await state.set_state(AdminMovie.movie_file)
    else:
        print("xato")


@dp.message(AdminMovie.movie_file, F.video)
async def get_movie_file(message: types.Message, state: FSMContext):
    movie_file = message.video.file_id
    await state.update_data(movie_file=movie_file)
    await message.answer("Film qabul qilindi\nTavsifini yuboring")
    await state.set_state(AdminMovie.movie_desc)



@dp.message(AdminMovie.movie_desc)
async def get_movie_desc(message: types.Message, state: FSMContext):
    movie_desc = message.text
    await state.update_data(movie_desc=movie_desc)

    data = await state.get_data()

    movie_file = data.get('movie_file')
    movie_desc = data.get('movie_desc')

    code = generate_move_code()

    lines = movie_desc.split('\n')
    new_lines = []

    for line in lines:
        new_lines.append(line)
        if line.startswith("⚡️ Janri:"):
            new_lines.append(f"\n🔢 KINO KODI: {code}\n")

    final_desc = '\n'.join(new_lines)
    add_movie(movie_file, final_desc, code)
    await message.answer_video(movie_file, caption=final_desc)
    await message.answer("film yuklandi")
    await state.clear()



@dp.message(F.text)
async def get_movie_code_by_ketmon(message: types.Message):

    user_id = message.from_user.id

    # 🔥 HAR SAFAR OBUNA TEKSHIRAMIZ
    is_sub = await check_subbed_user(bot, user_id)

    if not is_sub:
        await message.answer(
            "Film olishdan oldin kanalga obuna bo'ling!",
            reply_markup=sub_keyboard([])
        )
        return

    movie_code = message.text
    movie = get_movie_code(movie_code)

    if movie:
        await message.answer_video(video=movie[1], caption=movie[2])
    else:
        await message.answer("Film kodi mavjud emas")




async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())