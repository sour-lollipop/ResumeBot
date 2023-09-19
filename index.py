import asyncio
import logging
import locale
import sys
import os
from translations import _

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "6439782775:AAGjeVKXRcGFuJih7ZkEo12xyDI-udRz2N4"

locale.setlocale(locale.LC_ALL, '')
'ru_RU.utf8'
# Configure logging
logging.basicConfig(level = logging.INFO)
# Initialize bot and storage
bot = Bot(token = TOKEN )
dp = Dispatcher(bot, storage = MemoryStorage())

class Candidate_States(StatesGroup):
    Desired_positions = State()
    Full_name = State()
    Date_of_birth = State()
    Place_of_birth = State()
    Marital_status = State()
    # Have_any_children = State()
    Height = State()
    Weight = State()
    City_of_residence = State()
    Current_location = State()
    Nationality = State()
    Nationality_country = State()
    # Have_travel_passport = State()
    # COVID = State()

# Start with change language
# Buttons for change language
ru = InlineKeyboardButton(text = 'русский', callback_data = 'lang_ru')
en = InlineKeyboardButton(text = 'english', callback_data = 'lang_en')
lang_KB = InlineKeyboardMarkup(row_width = 1).row(ru, en)
# ***********
@dp.message_handler(commands=['start'], state='*')
async def start_command(msg: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(msg.from_user.id,
                           text = 'Выбирите язык / Choose language :',
                           reply_markup=lang_KB
                           )
    
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('lang'))
async def choose_lang(callback_query: types.CallbackQuery, state: FSMContext):
    language = callback_query.data.split('_')[1]
    await state.update_data(language = language)
    await callback_query.message.answer(_('Напишите желаемые должности',language))
    await state.set_state(Candidate_States.Desired_positions)
# ********************************************************************

@dp.message_handler(commands=['text'], state=Candidate_States.Desired_positions)
async def save_desired_positions(msg: types.Message, state: FSMContext):
    await state.update_data(desired_positions = msg.text)
    data  = await state.get_data()
    print(data['language'])
    await bot.send_message(msg.from_user.id, _('Введите свое ФИО', data['language']))
    await state.set_state(Candidate_States.Full_name)

@dp.message_handler(commands=['text'], state=Candidate_States.Full_name)
async def save_full_name(msg: types.Message, state: FSMContext):
    await state.update_data(full_name = msg.text)
    data  = await state.get_data()
    await bot.send_message(msg.from_user.id, _('Введите свою дату рождения', data['language']))
    await state.set_state(Candidate_States.Date_of_birth)

@dp.message_handler(commands=['text'], state=Candidate_States.Date_of_birth)
async def save_date_of_birth(msg: types.Message, state: FSMContext):
    await state.update_data(date_of_birth = msg.text)
    data  = await state.get_data()
    await bot.send_message(msg.from_user.id, _("Введите место вашего рождения", data['language']))
    await Candidate_States.Place_of_birth.set()

@dp.message_handler(commands=['text'], state=Candidate_States.Place_of_birth)
async def save_place_of_birth(msg: types.Message, state: FSMContext):
    await state.update_data(place_of_birth = msg.text)
    data  = await state.get_data()

    # Buttons for change language
    married = InlineKeyboardButton(text = _("Замужем / Женат", data['language']), callback_data = 'married')
    not_married = InlineKeyboardButton(text = _("Не Замужем / Не Женат", data['language']), callback_data = 'married_N')
    marry_KB = InlineKeyboardMarkup(row_width = 1).row(married, not_married)

    await bot.send_message(msg.from_user.id, _("Ваше семейное положение", data['language']), reply_markup = marry_KB)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('married'))
async def choose_lang(callback_query: types.CallbackQuery, state: FSMContext):
    married = callback_query.data
    await callback_query.message.answer(married)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)