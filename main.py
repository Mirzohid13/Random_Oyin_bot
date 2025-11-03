import asyncio
from os import getenv
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyMarkupUnion, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8582477766:AAGbQhib2jl8AiGZcrQkiPti3_-cu61vzfY"

dp = Dispatcher()

button=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🎲Boshlash🎲")]
], resize_keyboard=True)

# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Asslomu aleykum {message.from_user.full_name} \n🎲 Oyinni boshlash uchun pasdagi tugmani bosing.",reply_markup=button)


class GameStates(StatesGroup):
    waiting_for_number = State()


@dp.message(F.text == "🎲Boshlash🎲")
async def random_oyin(msg: Message, state: FSMContext):
    n = random.randint(1, 100)
    await state.update_data(random_number=n)
    await state.set_state(GameStates.waiting_for_number)
    await msg.answer("Men 1 dan 100 gacha son o'yladim. Toping!")


@dp.message(GameStates.waiting_for_number)
async def check_number(msg: Message, state: FSMContext):
    try:
        m = int(msg.text)
        data = await state.get_data()
        n = data['random_number']

        if n == m:
            await msg.answer("🎉 Tabriklaymiz! To'g'ri topdingiz!")
            await state.clear()
        elif n > m:
            await msg.answer("⬆️ Kattaroq son kiriting")
        else:
            await msg.answer("⬇️ Kichikroq son kiriting")
    except ValueError:
        await msg.answer("❌ Iltimos, faqat son kiriting!")

# Run the bot
async def main() -> None:
    print("Bot ishga tushdi")
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
