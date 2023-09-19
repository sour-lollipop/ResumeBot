import asyncio
import logging
from translations import _
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import html
from aiogram import F
import os
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
    Nationality_country = State()
    Have_travel_passport = State()
    COVID_Photo = State()
    Phone_Number = State()
    Messenger = State()
    Email = State()
    Instagram = State()
    LinkedIn = State()
    Vkontakte = State()
    Name_cousen = State()
    Phone_Number_cousen = State()
    Relative_cousen = State()
    Father_name = State()
    Mother_name = State()
    Education_degree = State()
    University_name = State()
    

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
TOKEN = "6439782775:AAGjeVKXRcGFuJih7ZkEo12xyDI-udRz2N4"
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT )

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
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    language = callback.data.split('_')[1]
    await state.update_data(language = language)
    await callback.message.answer(_('Напишите желаемые должности',language))
    await state.set_state(Candidate_States.Desired_positions)

@dp.message(Candidate_States.Desired_positions)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(desired_positions = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите свое ФИО', data['language']))
    await state.set_state(Candidate_States.Full_name)

@dp.message(Candidate_States.Full_name)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(full_name = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите свою дату рождения', data['language']))
    await state.set_state(Candidate_States.Date_of_birth)

@dp.message(Candidate_States.Date_of_birth)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(date_of_birth = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите место вашего рождения', data['language']))
    await state.set_state(Candidate_States.Place_of_birth)

@dp.message(Candidate_States.Place_of_birth)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(place_of_birth = message.text)
    data  = await state.get_data()

    marry_KB = InlineKeyboardBuilder()
    married = types.InlineKeyboardButton(text = _("Замужем / Женат", data['language']), callback_data = 'married_Y')
    not_married = types.InlineKeyboardButton(text = _("Не Замужем / Не Женат", data['language']), callback_data = 'married_N')
    marry_KB.row(married, not_married)

    await message.answer(_('Ваше семейное положение', data['language']),
                         reply_markup = marry_KB.as_markup()
                         )
    
@dp.callback_query(lambda c: c.data and c.data.startswith('married'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    married = callback.data.split('_')[1]
    await state.update_data(married = married)
    data  = await state.get_data()

    child_KB = InlineKeyboardBuilder()
    child_Y = types.InlineKeyboardButton(text = _('Да',data['language']), callback_data = 'child_Y')
    child_N = types.InlineKeyboardButton(text = _('Нет',data['language']), callback_data = 'child_N')
    child_KB.row(child_Y, child_N)

    await callback.message.answer(_('Есть ли у вас дети?',data['language']), 
                                  reply_markup=child_KB.as_markup())
    # await state.set_state(Candidate_States.Have_any_children)

@dp.callback_query(lambda c: c.data and c.data.startswith('child'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    Have_any_children = callback.data.split('_')[1]
    await state.update_data(have_any_children = Have_any_children)
    data  = await state.get_data()
    await callback.message.answer(_('Введите свой рост (см)', data['language']))
    await state.set_state(Candidate_States.Height)

@dp.message(Candidate_States.Height)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(height = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите свой вес (кг)', data['language']))
    await state.set_state(Candidate_States.Weight)

@dp.message(Candidate_States.Weight)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(weight = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите ваш город проживания', data['language']))
    await state.set_state(Candidate_States.City_of_residence)

@dp.message(Candidate_States.City_of_residence)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(city_of_residence = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите ваше текущее местоположение', data['language']))
    await state.set_state(Candidate_States.Current_location)

@dp.message(Candidate_States.Current_location)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(current_location = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите ваше национальность', data['language']))
    await state.set_state(Candidate_States.Nationality)

@dp.message(Candidate_States.Nationality)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(nationality = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите ваше гражданство', data['language']))
    await state.set_state(Candidate_States.Nationality_country)

@dp.message(Candidate_States.Nationality_country)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(nationality_country = message.text)
    data  = await state.get_data()
    haveP_KB = InlineKeyboardBuilder()
    haveP_Y = types.InlineKeyboardButton(text = _('Да',data['language']), callback_data = 'haveP_Y')
    haveP_N = types.InlineKeyboardButton(text = _('Нет',data['language']), callback_data = 'haveP_N')
    haveP_KB.row(haveP_Y, haveP_N)

    await message.answer(_('У вас есть загранпаспорт?',data['language']), 
                                  reply_markup=haveP_KB.as_markup())

    
@dp.callback_query(lambda c: c.data and c.data.startswith('haveP'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    haveP_ = callback.data.split('_')[1]
    await state.update_data(haveP_ = haveP_)
    data  = await state.get_data()

    covid_KB = InlineKeyboardBuilder()
    covid_Y = types.InlineKeyboardButton(text = _('Да',data['language']), callback_data = 'covid_Y')
    covid_N = types.InlineKeyboardButton(text = _('Нет',data['language']), callback_data = 'covid_N')
    covid_KB.row(covid_Y, covid_N)
    await callback.message.answer(_('Вы получили вакцину от COVID?',data['language']), 
                                  reply_markup=covid_KB.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('covid'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    covid = callback.data.split('_')[1]
    await state.update_data(covid = covid)
    data  = await state.get_data()

    print('COVID: ', covid)
    if covid == 'Y':
        await callback.message.answer(_('Отправьте сертификат вакцинации',data['language']))
        await state.set_state(Candidate_States.COVID_Photo)
    else:
        await callback.message.answer(f'{data}')
        await callback.message.answer(_('Введите ваш номер мобильного телефона',data['language'])) 
        await state.set_state(Candidate_States.Phone_Number)


@dp.message(F.photo, Candidate_States.COVID_Photo)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await bot.download(
        message.photo[-1],
        destination=f"{message.photo[-1].file_id}.jpg"
    )
    await state.update_data(COVID_Photo = f"{message.photo[-1].file_id}.jpg")
    data  = await state.get_data()
    await message.answer(f'{data}')
    await message.answer(_('Введите ваш номер мобильного телефона',data['language'])) 
    await state.set_state(Candidate_States.Phone_Number)

@dp.message(Candidate_States.Phone_Number)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(phone_Number = message.text)
    data  = await state.get_data()
    await message.answer(_('У вас есть мессенджер?', data['language'])+'  \n Whatsapp, Telegram, Viber')
    await state.set_state(Candidate_States.Messenger)

@dp.message(Candidate_States.Messenger)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(messenger = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите ваш Адрес электронной почты', data['language']))
    await state.set_state(Candidate_States.Email)

@dp.message(Candidate_States.Email)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(email = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите ваш Instagram', data['language']))
    await state.set_state(Candidate_States.Instagram)

@dp.message(Candidate_States.Instagram)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(instagram = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите ваш LinkedIn', data['language']))
    await state.set_state(Candidate_States.LinkedIn)

@dp.message(Candidate_States.LinkedIn)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(linkedIn = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите ваш ВКонтакте', data['language']))
    await state.set_state(Candidate_States.Vkontakte)

@dp.message(Candidate_States.Vkontakte)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(vkontakte = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите Контактные данные родственника на случай чрезвычайной ситуации', data['language']))
    await message.answer(_('Введите имя вашего родственника', data['language']))
    await state.set_state(Candidate_States.Name_cousen)

@dp.message(Candidate_States.Name_cousen)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(name_cousen = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите номер телефон вашего родственника', data['language']))
    await state.set_state(Candidate_States.Phone_Number_cousen)

@dp.message(Candidate_States.Phone_Number_cousen)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(phone_Number_cousen = message.text)
    data  = await state.get_data()
    await message.answer(_('Как вы связаны с родственником? (Жена, Муж, Сын, Дядя и т.д.)', data['language']))
    await state.set_state(Candidate_States.Relative_cousen)

@dp.message(Candidate_States.Relative_cousen)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(relative_cousen = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите Имя Отца', data['language']))
    await state.set_state(Candidate_States.Father_name)

@dp.message(Candidate_States.Father_name)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(father_name = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите Имя матери', data['language']))
    await state.set_state(Candidate_States.Mother_name)

@dp.message(Candidate_States.Mother_name)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(mother_name = message.text)
    data  = await state.get_data()

    qatar_kb = InlineKeyboardBuilder()
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'gatar_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'gatar_no')
    qatar_kb.row(yes,no)
    await message.answer(_('Предпочитаете ли страну Катар для переезда и работы?', data['language']),
                         reply_markup = qatar_kb.as_markup()
                         )
        
@dp.callback_query(lambda c: c.data and c.data.startswith('gatar'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(gatar = callback.data.split('_')[1])
    UAE_kb = InlineKeyboardBuilder()
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'UAE_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'UAE_no')
    UAE_kb.row(yes,no)
    await callback.message.answer(_('Предпочитаете ли страну ОАЭ для переезда и работы?', data['language']),
                                  reply_markup = UAE_kb.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('UAE'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(UAE = callback.data.split('_')[1])
    Bahrain_kb = InlineKeyboardBuilder()
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'Bahrain_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'Bahrain_no')
    Bahrain_kb.row(yes,no)
    await callback.message.answer(_('Предпочитаете ли страну Бахрейн для переезда и работы?', data['language']),
                                  reply_markup = Bahrain_kb.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('Bahrain'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(Bahrain = callback.data.split('_')[1])
    Oman_kb = InlineKeyboardBuilder()
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'Oman_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'Oman_no')
    Oman_kb.row(yes,no)
    await callback.message.answer(_('Предпочитаете ли страну Оман для переезда и работы?', data['language']),
                                  reply_markup = Oman_kb.as_markup())
    
@dp.callback_query(lambda c: c.data and c.data.startswith('Oman'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(Oman = callback.data.split('_')[1])
    await callback.message.answer(_('Оброзование', data['language']))
    await callback.message.answer(_('Какая степень у вас была получена (бакалавр, магистр, специалист и т.д.)?', data['language']))
    await state.set_state(Candidate_States.Education_degree)

@dp.message(Candidate_States.Education_degree)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(education_stepen = message.text)
    data  = await state.get_data()
    await message.answer(_('В каком вузе или колледже  вы учились?', data['language']))
    await state.set_state(Candidate_States.University_name)

# @dp.message(Command('images'))
# async def upload_photo(message: types.Message):
#     file_ids = []
#     # Отправка файла по ссылке
#     image_from_url = URLInputFile("https://picsum.photos/seed/groosha/400/300")
#     result = await message.answer_photo(
#         image_from_url,
#         caption="Изображение по ссылке"
#     )
#     file_ids.append(result.photo[-1].file_id)
#     # Отправка файла по ссылке
#     image_from_url = URLInputFile("https://ru.visafoto.com/img/docs/zz_30x40.jpg")
#     result = await message.answer_photo(
#         image_from_url,
#         caption="Изображение по ссылке"
#     )
#     file_ids.append(result.photo[-1].file_id)

#     await message.answer("Отправленные файлы:\n"+"\n".join(file_ids))

# @dp.message(F.photo)
# async def download_photo(message: types.Message, bot: Bot):
    # await bot.download( message.photo[-1],
    #                     destination=f"{message.photo[-1].file_id}.jpg"
    # )

# Запуск процесса поллинга новых апдейтов
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())