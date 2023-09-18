import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class Candidate_States(StatesGroup):
    Desired_positions = State()
    Full_name = State()
    Date_of_birth = State()
    Place_of_birth = State()
    Marital_status = State()
    Have_any_children = State()
    Height = State()
    Weight = State()
    City_of_residence = State()
    Current_location = State()
    Nationality = State()
    Have_travel_passport = State()
    COVID = State()

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
TOKEN = "6439782775:AAGjeVKXRcGFuJih7ZkEo12xyDI-udRz2N4"
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    lang_kb = InlineKeyboardBuilder()
    en = types.InlineKeyboardButton(text = 'english', callback_data = 'lang_en')
    ru = types.InlineKeyboardButton(text = 'русский', callback_data = 'lang_ru')
    lang_kb.row(ru,en)
    await message.answer("Выбирите язык / Choose language :",
                         reply_markup = lang_kb.as_markup()
                         )
    
@dp.callback_query(lambda c: c.data and c.data.startswith('lang'))
async def choose_lang(callback: types.CallbackQuery):
    await callback.message.answer(callback.data)
# Запуск процесса поллинга новых апдейтов
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())