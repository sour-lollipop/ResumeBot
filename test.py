import asyncio
import logging
import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile, InputFile
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import html
from aiogram import F
from docx import Document 
from send_doc import send_email
from translations import _
from create_doc import save_document

class Candidate_States(StatesGroup):
    Add_Photo = State()
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
TOKEN = "6681000920:AAGZKsmxgKs3nRry-Gkjgm3a64HlhjdK48U"
bot = Bot(token=TOKEN)

# Диспетчер
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT )

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.update_data(language = 'ru')
    data  = await state.get_data()
    more_phote_kb = InlineKeyboardBuilder()
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'Added_More_Photo_Yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'Added_More_Photo_No')
    more_phote_kb.row(yes, no)
    await message.answer(_('Есть ли еще какие-то фотографии, которые вы бы хотели добавить?', data['language']),
                                  reply_markup = more_phote_kb.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('Added_More_Photo'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    if callback.data.split('_')[3] == 'Yes':
        await callback.message.edit_text(_('Отправьте одно фото', data['language']))
        await state.set_state(Candidate_States.Add_Photo)
    else:
        await callback.message.edit_text('THE END')

@dp.message(F.photo,Candidate_States.Add_Photo)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await bot.download(
        message.photo[-1],
        destination=f"{message.photo[-1].file_id}.jpg"
    )
    data  = await state.get_data()

    await state.update_data(more_Photo = f"{message.photo[-1].file_id}.jpg")

    more_phote_kb = InlineKeyboardBuilder()
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'secondAdded_More_Photo_Yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'secondAdded_More_Photo_No')
    more_phote_kb.row(yes, no)
    await message.answer(_('Есть ли еще какие-то фотографии, которые вы бы хотели добавить?', data['language']),
                                  reply_markup = more_phote_kb.as_markup())

# Запуск процесса поллинга новых апдейтов
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())