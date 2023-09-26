import asyncio
import logging
import os
import requests
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
from docx import Document 

from translations import _
from create_doc import save_document

class Candidate_States(StatesGroup):
    Desired_positions = State()
    Full_name = State()
    Profile_photo = State()
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
    Facebook = State()
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
    Special_degree = State()
    
    Year_of_Education = State()
    Postgraduate_name = State()
    Postgraduate_special = State()
    Postgraduate_degree = State()
    Postgraduate_date = State()
    
    Course_name = State()
    Course_date = State()
    Course_place = State()
    Course_photo = State()
    
    Tattoo_discribe = State()
    Tattoo_photo = State()
    
    Work_exp = State()
    Work_name = State()
    Work_place = State()
    Work_position = State()
    Work_responsibilities = State()

    Other_work_exp = State()
    Other_work_name = State()
    Other_work_place = State()
    Other_work_position = State()
    Other_work_responsibilities = State()
    
    Now_work_exp = State()
    Now_work_name = State()
    Now_work_place = State()
    Now_work_position = State()
    Now_work_responsibilities = State()
    
    Comp_programs = State()
    Hoste_program = State()
    Finance_program = State()
    Travel_program = State()
    Graph_program = State()
    
    Car_category = State()
    Added_language = State()
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
TOKEN = "6439782775:AAGjeVKXRcGFuJih7ZkEo12xyDI-udRz2N4"
bot = Bot(token=TOKEN)

# Диспетчер
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT )

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    lang_kb = InlineKeyboardBuilder()
    en = types.InlineKeyboardButton(text = 'english', callback_data = 'lang_en')
    ru = types.InlineKeyboardButton(text = 'русский', callback_data = 'lang_ru')
    lang_kb.row(ru,en)
    await state.clear()
    await message.answer("Выбирите язык / Choose language :",
                         reply_markup = lang_kb.as_markup()
                         )
    
@dp.callback_query(lambda c: c.data and c.data.startswith('lang'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    language = callback.data.split('_')[1]
    await state.update_data(language = language)
    await callback.message.edit_text(_('Напишите желаемые должности',language))
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
    # await message.answer(_('Отправьте фото своего профиля, как показано здесь:', data['language']))
    
    image_from_pc = FSInputFile("userquest.jpg")
    await message.answer_photo(
        image_from_pc,
        caption=_('Отправьте фото своего профиля, как показано здесь:', data['language'])
    )
    await state.set_state(Candidate_States.Profile_photo)

@dp.message(F.photo,Candidate_States.Profile_photo)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await bot.download(
        message.photo[-1],
        destination=f"{message.photo[-1].file_id}.jpg"
    )
    await state.update_data(profile_Photo = f"{message.photo[-1].file_id}.jpg")
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

    await callback.message.edit_text(_('Есть ли у вас дети?',data['language']), 
                                  reply_markup=child_KB.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('child'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    Have_any_children = callback.data.split('_')[1]
    await state.update_data(have_any_children = Have_any_children)
    data  = await state.get_data()
    await callback.message.edit_text(_('Введите свой рост (см)', data['language']))
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
    covid_Y = types.InlineKeyboardButton(text = _('Да',data['language']), callback_data = 'covid_Yes')
    covid_N = types.InlineKeyboardButton(text = _('Нет',data['language']), callback_data = 'covid_No')
    covid_KB.row(covid_Y, covid_N)
    await callback.message.edit_text(_('Вы получили вакцину от COVID?',data['language']), 
                                  reply_markup=covid_KB.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('covid'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    covid = callback.data.split('_')[1]
    await state.update_data(covid_access = covid)
    data  = await state.get_data()
    if covid == 'Yes':
        await callback.message.edit_text(_('Отправьте сертификат вакцинации',data['language']))
        await state.set_state(Candidate_States.COVID_Photo)
    else:
        await callback.message.edit_text(_('Введите ваш номер мобильного телефона',data['language'])) 
        await state.set_state(Candidate_States.Phone_Number)


@dp.message(F.photo, Candidate_States.COVID_Photo)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await bot.download(
        message.photo[-1],
        destination=f"{message.photo[-1].file_id}.jpg"
    )
    await state.update_data(COVID_Photo = f"{message.photo[-1].file_id}.jpg")
    data  = await state.get_data()
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
    await message.answer(_('Введите ваш Facebook', data['language']))
    await state.set_state(Candidate_States.Facebook)

@dp.message(Candidate_States.Facebook)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(Facebook = message.text)
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
    await message.answer(_('Введите Контактные данные родственника на случай чрезвычайной ситуации', data['language'])+
                            '\n'+_('Введите имя вашего родственника', data['language']))
    # await message.answer(_('Введите имя вашего родственника', data['language']))
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
    await callback.message.edit_text(_('Предпочитаете ли страну ОАЭ для переезда и работы?', data['language']),
                                  reply_markup = UAE_kb.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('UAE'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(UAE = callback.data.split('_')[1])
    Bahrain_kb = InlineKeyboardBuilder()
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'Bahrain_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'Bahrain_no')
    Bahrain_kb.row(yes,no)
    await callback.message.edit_text(_('Предпочитаете ли страну Бахрейн для переезда и работы?', data['language']),
                                  reply_markup = Bahrain_kb.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('Bahrain'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(Bahrain = callback.data.split('_')[1])
    Oman_kb = InlineKeyboardBuilder()
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'Oman_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'Oman_no')
    Oman_kb.row(yes,no)
    await callback.message.edit_text(_('Предпочитаете ли страну Оман для переезда и работы?', data['language']),
                                  reply_markup = Oman_kb.as_markup())
    
@dp.callback_query(lambda c: c.data and c.data.startswith('Oman'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(Oman = callback.data.split('_')[1])
    await callback.message.edit_text(_('Оброзование', data['language'])+'\n'+
                                     _('Какая степень у вас была получена (бакалавр, магистр, специалист и т.д.)?', data['language']))
    await state.set_state(Candidate_States.Education_degree)

@dp.message(Candidate_States.Education_degree)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(education_stepen = message.text)
    data  = await state.get_data()
    await message.answer(_('В каком вузе или колледже  вы учились?', data['language']))
    await state.set_state(Candidate_States.University_name)

@dp.message(Candidate_States.University_name)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(university_name = message.text)
    data  = await state.get_data()
    await message.answer(_('Какая у вас специализация или факультет?', data['language']))
    await state.set_state(Candidate_States.Special_degree)

@dp.message(Candidate_States.Special_degree)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(special_degree = message.text)
    data  = await state.get_data()
    await message.answer(_('В какие годы вы учились в университете? (год начала - год окончания)', data['language']))
    await state.set_state(Candidate_States.Year_of_Education)

@dp.message(Candidate_States.Year_of_Education)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(year_of_Education = message.text)
    data  = await state.get_data()
    postgraduate_KB = InlineKeyboardBuilder() 
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'postgraduate_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'postgraduate_no')
    postgraduate_KB.row(yes,no)
    await message.answer(_('Есть ли у вас Последипломное образование?', data['language']),
                         reply_markup = postgraduate_KB.as_markup())
    
# ********************************
# ********************************
# ********************************
@dp.callback_query(lambda c: c.data and c.data.startswith('postgraduate'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(postgraduate_access = callback.data.split('_')[1])
    if 'yes' == callback.data.split('_')[1]:
        await callback.message.answer(_('В каком учебном заведении вы продолжали образование после получения степени?', data['language']))
        await state.set_state(Candidate_States.Postgraduate_name)
    else:
        course_KB = InlineKeyboardBuilder() 
        yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'course_yes')
        no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'course_no')
        course_KB.row(yes,no)
        await callback.message.edit_text(_('Проходили ли вы какие-либо дополнительные курсы или тренинги?', data['language']),
                            reply_markup = course_KB.as_markup())

@dp.message(Candidate_States.Postgraduate_name)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(postgraduate_name = message.text)
    data  = await state.get_data()
    await message.answer(_('Какая у вас была специализация?', data['language']))
    await state.set_state(Candidate_States.Postgraduate_special)

@dp.message(Candidate_States.Postgraduate_special)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(postgraduate_special = message.text)
    data  = await state.get_data()
    await message.answer(_('Какую степень вы получили? (например, кандидат наук, доктор наук)', data['language']))
    await state.set_state(Candidate_States.Postgraduate_degree)

@dp.message(Candidate_States.Postgraduate_degree)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(postgraduate_degree = message.text)
    data  = await state.get_data()
    await message.answer(_('В какие годы вы учились? (год начала - год окончания)', data['language']))
    await state.set_state(Candidate_States.Postgraduate_date)

@dp.message(Candidate_States.Postgraduate_date)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(postgraduate_date = message.text)
    data  = await state.get_data()

    course_KB = InlineKeyboardBuilder() 
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'course_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'course_no')
    course_KB.row(yes,no)
    await message.answer(_('Проходили ли вы какие-либо дополнительные курсы или тренинги?', data['language']),
                        reply_markup = course_KB.as_markup())
# ****************************
@dp.callback_query(lambda c: c.data and c.data.startswith('course'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(course_access = callback.data.split('_')[1])
    if 'yes'==callback.data.split('_')[1]:
        await callback.message.answer(_('Введите один курс, которы вы прошли', data['language']))
        await state.set_state(Candidate_States.Course_name)
    else:
        tattoo_KB = InlineKeyboardBuilder() 
        yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'tattoo_yes')
        no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'tattoo_no')
        tattoo_KB.row(yes,no)
        await callback.message.edit_text(_('Есть ли у вас татуировки или пирсинг?', data['language']),
                            reply_markup = tattoo_KB.as_markup())

@dp.message(Candidate_States.Course_name)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(сourse_name = message.text)
    data  = await state.get_data()
    await message.answer(_('Когда вы проходили данный курс или тренинг?', data['language']))
    await state.set_state(Candidate_States.Course_date)

@dp.message(Candidate_States.Course_date)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(course_date = message.text)
    data  = await state.get_data()
    await message.answer(_('Где вы проходили данный курс или тренинг?', data['language']))
    await state.set_state(Candidate_States.Course_place)

@dp.message(Candidate_States.Course_place)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(Course_place = message.text)
    data  = await state.get_data()
    doc_course_KB = InlineKeyboardBuilder() 
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'doc_course_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'doc_course_no')
    doc_course_KB.row(yes,no)
    await message.answer(_('Есть ли у вас сертефикаты подтверждающие прохождение курсов?', data['language']),
                         reply_markup = doc_course_KB.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('doc_course'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(doc_course_access = callback.data.split('_')[2])
    data  = await state.get_data()
    if 'yes'==callback.data.split('_')[2]:
        await callback.message.answer(_('Отправьте одно фото', data['language']))
        await state.set_state(Candidate_States.Course_photo)
    else:
        tattoo_KB = InlineKeyboardBuilder() 
        yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'tattoo_yes')
        no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'tattoo_no')
        tattoo_KB.row(yes,no)
        await callback.message.edit_text(_('Есть ли у вас татуировки или пирсинг?', data['language']),
                            reply_markup = tattoo_KB.as_markup())

@dp.message(F.photo, Candidate_States.Course_photo)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await bot.download(
        message.photo[-1],
        destination=f"{message.photo[-1].file_id}.jpg"
    )
    await state.update_data(Course_Photo = f"{message.photo[-1].file_id}.jpg")
    data  = await state.get_data()
    tattoo_KB = InlineKeyboardBuilder() 
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'tattoo_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'tattoo_no')
    tattoo_KB.row(yes,no)
    await message.answer(_('Есть ли у вас татуировки или пирсинг?', data['language']),
                        reply_markup = tattoo_KB.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('tattoo'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(tattoo_access = callback.data.split('_')[1])
    if 'yes'==callback.data.split('_')[1]:
        await callback.message.answer(_('Опишите татуировку или пирсинг', data['language']))
        await state.set_state(Candidate_States.Tattoo_discribe)
    else:
        await callback.message.edit_text(_('Опишите ваш опыт работы', data['language'])+'\n'+
                                         _('Официальный и не официальный начиная с последнего или текущего места работы', data['language']))
        await state.set_state(Candidate_States.Work_exp)
# ********************************
@dp.message(Candidate_States.Tattoo_discribe)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(tattoo_discribe = message.text)
    data  = await state.get_data()
    await message.answer(_('Отправьте одно фото', data['language']))
    await state.set_state(Candidate_States.Tattoo_photo)

@dp.message(F.photo, Candidate_States.Tattoo_photo)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await bot.download(
        message.photo[-1],
        destination=f"{message.photo[-1].file_id}.jpg"
    )
    await state.update_data(tattoo_Photo = f"{message.photo[-1].file_id}.jpg")
    data  = await state.get_data()
    await message.answer(_('Опишите ваш опыт работы', data['language'])+'\n'+
                            _('Официальный и не официальный начиная с последнего или текущего места работы', data['language']))
    await state.set_state(Candidate_States.Work_exp)

@dp.message(Candidate_States.Work_exp)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(work_exp = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите имя компании', data['language']))
    await state.set_state(Candidate_States.Work_name)

@dp.message(Candidate_States.Work_name)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(work_name = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите местоположение компании', data['language']))
    await state.set_state(Candidate_States.Work_place)

@dp.message(Candidate_States.Work_place)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(work_place = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите вашу должность', data['language']))
    await state.set_state(Candidate_States.Work_position)

@dp.message(Candidate_States.Work_position)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(work_position = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите ваши обязанности', data['language']))
    await state.set_state(Candidate_States.Work_responsibilities)

@dp.message(Candidate_States.Work_responsibilities)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(work_responsibilities = message.text)
    data  = await state.get_data()
    other_work_KB = InlineKeyboardBuilder()
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'other_work_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'other_work_no')
    other_work_KB.row(yes,no)
    await message.answer(_('Кроме вышеупомянутой работы, есть ли у вас ещё опыт работы?', data['language']),
                         reply_markup=other_work_KB.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('other_work'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(other_work_access = callback.data.split('_')[2])
    if 'yes'==callback.data.split('_')[2]:
        await callback.message.edit_text(_('Опишите ваш опыт работы', data['language']))
        await state.set_state(Candidate_States.Other_work_exp)
    else:
        now_work_KB = InlineKeyboardBuilder()
        yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'now_work_yes')
        no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'now_work_no')
        now_work_KB.row(yes,no)
        await callback.message.answer(_('Работаете ли вы сейчас?', data['language']),
                            reply_markup=now_work_KB.as_markup())

@dp.message(Candidate_States.Other_work_exp)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(other_work_exp = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите имя компании', data['language']))
    await state.set_state(Candidate_States.Other_work_name)

@dp.message(Candidate_States.Other_work_name)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(other_work_name = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите местоположение компании', data['language']))
    await state.set_state(Candidate_States.Other_work_place)
    
@dp.message(Candidate_States.Other_work_place)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(other_work_place = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите вашу должность', data['language']))
    await state.set_state(Candidate_States.Other_work_position)

@dp.message(Candidate_States.Other_work_position)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(other_work_position = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите ваши обязанности', data['language']))
    await state.set_state(Candidate_States.Other_work_responsibilities)

@dp.message(Candidate_States.Other_work_responsibilities)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(other_work_responsibilities = message.text)
    data  = await state.get_data()
    now_work_KB = InlineKeyboardBuilder()
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'now_work_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'now_work_no')
    now_work_KB.row(yes,no)
    await message.answer(_('Работаете ли вы сейчас?', data['language']),
                        reply_markup=now_work_KB.as_markup())


# *********************************************
@dp.callback_query(lambda c: c.data and c.data.startswith('now_work'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(now_work_access = callback.data.split('_')[2])
    if 'yes'==callback.data.split('_')[2]:
        await callback.message.edit_text(_('Опишите ваш опыт работы', data['language']))
        await state.set_state(Candidate_States.Now_work_exp)
    else:
        await state.set_state(Candidate_States.Comp_programs)


@dp.message(Candidate_States.Now_work_exp)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(now_work_exp = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите имя компании', data['language']))
    await state.set_state(Candidate_States.Now_work_name)

@dp.message(Candidate_States.Now_work_name)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(now_work_name = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите местоположение компании', data['language']))
    await state.set_state(Candidate_States.Now_work_place)

@dp.message(Candidate_States.Now_work_place)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(now_work_place = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите вашу должность', data['language']))
    await state.set_state(Candidate_States.Now_work_position)

@dp.message(Candidate_States.Now_work_position)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(now_work_position = message.text)
    data  = await state.get_data()
    await message.answer(_('Введите ваши обязанности', data['language']))
    await state.set_state(Candidate_States.Now_work_responsibilities)

@dp.message(Candidate_States.Now_work_responsibilities)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(now_work_responsibilities = message.text)
    data  = await state.get_data()
    await message.answer(_('Работали ли вы с компьютерными программами для гостеприимства?', data['language'])+'\n'+
                            _('Если да, напишите название, если нет введите "нет"', data['language']))
    await state.set_state(Candidate_States.Hoste_program)


# **************************************
@dp.message(Candidate_States.Comp_programs)
async def save_desired_positions(message: types.Message, state: FSMContext):
    # await state.update_data(work_responsibilities = message.text)
    data  = await state.get_data()
    await message.answer(_('Работали ли вы с компьютерными программами для гостеприимства?', data['language'])+'\n'+
                            _('Если да, напишите название, если нет введите "нет"', data['language']))
    await state.set_state(Candidate_States.Hoste_program)

@dp.message(Candidate_States.Hoste_program)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(hoste_program = message.text)
    data  = await state.get_data()
    await message.answer(_('Работали ли вы с компьютерными программами для финансов?', data['language'])+'\n'+
                            _('Если да, напишите название, если нет введите "нет"', data['language']))
    await state.set_state(Candidate_States.Finance_program)

@dp.message(Candidate_States.Finance_program)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(finance_program = message.text)
    data  = await state.get_data()
    await message.answer(_('Работали ли вы с компьютерными программами для путешествий и бронирования?', data['language'])+'\n'+
                            _('Если да, напишите название, если нет введите "нет"', data['language']))
    await state.set_state(Candidate_States.Travel_program)


@dp.message(Candidate_States.Travel_program)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(travel_program = message.text)
    data  = await state.get_data()
    await message.answer(_('Работали ли вы с компьютерными программами для графики и дизайна?', data['language'])+'\n'+
                            _('Если да, напишите название, если нет введите "нет"', data['language']))
    await state.set_state(Candidate_States.Graph_program)

@dp.message(Candidate_States.Graph_program)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(graph_program = message.text)
    data  = await state.get_data()
    car_KB = InlineKeyboardBuilder() 
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'car_yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'car_no')
    car_KB.row(yes,no)
    await message.answer(_('Есть ли у вас Водительские права', data['language']),
                         reply_markup = car_KB.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('car'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(car_access = callback.data.split('_')[1])
    if 'yes'==callback.data.split('_')[1]:
        await callback.message.edit_text(_('Напишите категорию водительских прав', data['language']))
        await state.set_state(Candidate_States.Car_category)
    else:
        russian_KB = InlineKeyboardBuilder() 
        basic = types.InlineKeyboardButton(text = _('Базовый', data['language']), callback_data = 'russian_Basic')
        elementary = types.InlineKeyboardButton(text = _('Элементарный', data['language']), callback_data = 'russian_Elementary')
        lowerInt = types.InlineKeyboardButton(text = _('Ниже среднего', data['language']), callback_data = 'russian_Lower Intermediate')
        intermediate = types.InlineKeyboardButton(text = _('Средний', data['language']), callback_data = 'russian_Intermediate')
        upperInt = types.InlineKeyboardButton(text = _('Выше среднего', data['language']), callback_data = 'russian_Upper Intermediate')
        advanced = types.InlineKeyboardButton(text = _('Продвинутый', data['language']), callback_data = 'russian_Advanced')
        fluent = types.InlineKeyboardButton(text = _('Носитель', data['language']), callback_data = 'russian_Fluent')
        russian_KB.row(basic, elementary, lowerInt, intermediate, upperInt, advanced, fluent).adjust(3,3)
        await callback.message.edit_text(_('Знание языков', data['language'])+'\n'
                                         +_('На каком уровне вы знаете русский язык?', data['language']),
                                      reply_markup = russian_KB.as_markup())

@dp.message(Candidate_States.Car_category)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(car_category = message.text)
    data  = await state.get_data()
    russian_KB = InlineKeyboardBuilder() 
    basic = types.InlineKeyboardButton(text = _('Базовый', data['language']), callback_data = 'russian_Basic')
    elementary = types.InlineKeyboardButton(text = _('Элементарный', data['language']), callback_data = 'russian_Elementary')
    lowerInt = types.InlineKeyboardButton(text = _('Ниже среднего', data['language']), callback_data = 'russian_Lower Intermediate')
    intermediate = types.InlineKeyboardButton(text = _('Средний', data['language']), callback_data = 'russian_Intermediate')
    upperInt = types.InlineKeyboardButton(text = _('Выше среднего', data['language']), callback_data = 'russian_Upper Intermediate')
    advanced = types.InlineKeyboardButton(text = _('Продвинутый', data['language']), callback_data = 'russian_Advanced')
    fluent = types.InlineKeyboardButton(text = _('Носитель', data['language']), callback_data = 'russian_Fluent')
    russian_KB.row(basic, elementary, lowerInt, intermediate, upperInt, advanced, fluent).adjust(3,3)
    await message.answer(_('Знание языков', data['language'])+'\n'
                                         +_('На каком уровне вы знаете русский язык?', data['language']),
                                    reply_markup = russian_KB.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('russian'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(russian = callback.data.split('_')[1])

    english_KB = InlineKeyboardBuilder() 
    basic = types.InlineKeyboardButton(text = _('Базовый', data['language']), callback_data = 'english_Basic')
    elementary = types.InlineKeyboardButton(text = _('Элементарный', data['language']), callback_data = 'english_Elementary')
    lowerInt = types.InlineKeyboardButton(text = _('Ниже среднего', data['language']), callback_data = 'english_Lower Intermediate')
    intermediate = types.InlineKeyboardButton(text = _('Средний', data['language']), callback_data = 'english_Intermediate')
    upperInt = types.InlineKeyboardButton(text = _('Выше среднего', data['language']), callback_data = 'english_Upper Intermediate')
    advanced = types.InlineKeyboardButton(text = _('Продвинутый', data['language']), callback_data = 'english_Advanced')
    fluent = types.InlineKeyboardButton(text = _('Носитель', data['language']), callback_data = 'english_Fluent')
    english_KB.row(basic, elementary, lowerInt, intermediate, upperInt, advanced, fluent).adjust(3,3)
    await callback.message.edit_text(_('На каком уровне вы знаете английски язык?', data['language']),
                                      reply_markup = english_KB.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('english'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(english = callback.data.split('_')[1])
    other_lang_KB = InlineKeyboardBuilder() 
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'other_lang_access_Yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'other_lang_access_No')
    other_lang_KB.row(yes, no)
    await callback.message.edit_text(_('Знаете ли вы дополнительный язык?', data['language']),
                                      reply_markup = other_lang_KB.as_markup())
    
@dp.callback_query(lambda c: c.data and c.data.startswith('other_lang_access'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(other_lang_access = callback.data.split('_')[3])

    if 'Yes' == callback.data.split('_')[3]:
        await callback.message.edit_text(_('Введите дополнительный язык', data['language']))
        await state.set_state(Candidate_States.Added_language)
    else:
        know_about_as_KB = InlineKeyboardBuilder()
        google = types.InlineKeyboardButton(text = 'Google search' , callback_data = 'know_about_as_Google')
        facebook = types.InlineKeyboardButton(text = 'Facebook' , callback_data = 'know_about_as_Facebook')
        instagram = types.InlineKeyboardButton(text = 'Instagram' , callback_data = 'know_about_as_Instagram')
        vk = types.InlineKeyboardButton(text = 'Vk.com' , callback_data = 'know_about_as_Vk')
        friends = types.InlineKeyboardButton(text =  _('Через рекомендацию друзей', data['language']) , callback_data = 'know_about_as_Friends')
        other_source = types.InlineKeyboardButton(text =  _('Другие источники поиска работы', data['language']) , callback_data = 'know_about_as_Other')
        know_about_as_KB.row(google, facebook, instagram, vk, friends, other_source).adjust(3,3)
        await callback.message.edit_text(_('Откуда вы о нас узнали?', data['language']),
                                    reply_markup = know_about_as_KB.as_markup())
        
@dp.message(Candidate_States.Added_language)
async def save_desired_positions(message: types.Message, state: FSMContext):
    await state.update_data(added_language = message.text)
    data  = await state.get_data()

    added_language_KB = InlineKeyboardBuilder() 
    basic = types.InlineKeyboardButton(text = _('Базовый', data['language']), callback_data = 'other_lang_level_Basic')
    elementary = types.InlineKeyboardButton(text = _('Элементарный', data['language']), callback_data = 'other_lang_level_Elementary')
    lowerInt = types.InlineKeyboardButton(text = _('Ниже среднего', data['language']), callback_data = 'other_lang_level_Lower Intermediate')
    intermediate = types.InlineKeyboardButton(text = _('Средний', data['language']), callback_data = 'other_lang_level_Intermediate')
    upperInt = types.InlineKeyboardButton(text = _('Выше среднего', data['language']), callback_data = 'other_lang_level_Upper Intermediate')
    advanced = types.InlineKeyboardButton(text = _('Продвинутый', data['language']), callback_data = 'other_lang_level_Advanced')
    fluent = types.InlineKeyboardButton(text = _('Носитель', data['language']), callback_data = 'other_lang_level_Fluent')
    added_language_KB.row(basic, elementary, lowerInt, intermediate, upperInt, advanced, fluent).adjust(3,3)
    await message.answer(_('На каком уровне вы облодаете дополнительнм языком?', data['language']),
                                      reply_markup = added_language_KB.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('other_lang_level'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(other_lang_level = callback.data.split('_')[3])
    know_about_as_KB = InlineKeyboardBuilder()
    google = types.InlineKeyboardButton(text = 'Google search' , callback_data = 'know_about_as_Google')
    facebook = types.InlineKeyboardButton(text = 'Facebook' , callback_data = 'know_about_as_Facebook')
    instagram = types.InlineKeyboardButton(text = 'Instagram' , callback_data = 'know_about_as_Instagram')
    vk = types.InlineKeyboardButton(text = 'Vk.com' , callback_data = 'know_about_as_Vk')
    friends = types.InlineKeyboardButton(text =  _('Через рекомендацию друзей', data['language']) , callback_data = 'know_about_as_Friends')
    other_source = types.InlineKeyboardButton(text =  _('Другие источники поиска работы', data['language']) , callback_data = 'know_about_as_Other')
    know_about_as_KB.row(google, facebook, instagram, vk, friends, other_source).adjust(3,3)
    await callback.message.edit_text(_('Откуда вы о нас узнали?', data['language']),
                                reply_markup = know_about_as_KB.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('know_about_as'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.update_data(know_about_as = callback.data.split('_')[3])
    agree_24_kb = InlineKeyboardBuilder()
    yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'agree_24_Yes')
    no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'Delete_data')
    agree_24_kb.row(yes, no)
    await callback.message.edit_text(_('Я согласен подписать контракт с работодателем минимум на 24 месяца', data['language']),
                                  reply_markup = agree_24_kb.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('agree_24'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    if 'Yes'==callback.data.split('_')[2]:
        true_info_kb = InlineKeyboardBuilder()
        yes = types.InlineKeyboardButton(text = _('Да', data['language']), callback_data = 'true_info_Yes')
        no = types.InlineKeyboardButton(text = _('Нет', data['language']), callback_data = 'Delete_data')
        true_info_kb.row(yes, no)
        await callback.message.edit_text(_('Я подтверждаю, что вся информация, указанная в этом резюме, соответствует действительности.', data['language']),
                                      reply_markup = true_info_kb.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('true_info'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    if 'Yes'==callback.data.split('_')[2]:
        send_kb = InlineKeyboardBuilder()
        save = types.InlineKeyboardButton(text = _('Отправить', data['language']), callback_data = 'Save_data')
        restart = types.InlineKeyboardButton(text = _('Заново', data['language']), callback_data = 'Delete_data')
        send_kb.row(save, restart)
        first_block =( 
            f'{ _("ФИО", data["language"])} : {data["full_name"]} \n'
            f'{ _("Желаемые должности", data["language"])} : {data["desired_positions"]} \n'
            # f'profile_Photo : {data["profile_Photo"]} \n'
            f'{ _("Дата рождения", data["language"])} : {data["date_of_birth"]} \n'
            f'{ _("Место рождения", data["language"])} : {data["place_of_birth"]} \n'
            f'{ _("Семейное положение", data["language"])} : {data["married"]} \n'
            f'{ _("Наличие детей", data["language"])} : {data["have_any_children"]} \n'
            f'{ _("Рост (cm)", data["language"])} : {data["height"]} \n'
            f'{ _("Вес (kg)", data["language"])} : {data["weight"]} \n'
            f'{ _("Город проживания", data["language"])} : {data["city_of_residence"]} \n'
            f'{ _("Текущее местоположение", data["language"])} : {data["current_location"]} \n'
            f'{ _("Национальность", data["language"])} : {data["nationality"]} \n'
            f'{ _("Гражданство", data["language"])} : {data["nationality_country"]} \n'
            f'{ _("Наличие загранпасспорт", data["language"])} : {data["haveP_"]} \n'
            )
        if data["covid_access"]=="Yes":
            second_block = f'{_("Вакцинация от COVID", data["language"])} : {_("Да", data["language"])} \n'
            covid_photo = data["COVID_Photo"]
        else: 
            second_block = f'{_("Вакцинация от COVID", data["language"])} : {_("Нет", data["language"])} \n'
        third_block =(
            f'{_("Номер мобильного телефона", data["language"])} : {data["phone_Number"]} \n'
            f'{_("Наличие мессенджеров (Whatsapp, Viber...)", data["language"])} : {data["messenger"]} \n'
            f'Email : {data["email"]} \n'
            f'instagram : {data["instagram"]} \n'
            f'Facebook : {data["Facebook"]} \n'
            f'linkedIn : {data["linkedIn"]} \n'
            f'vkontakte : {data["vkontakte"]} \n'
            f'{_("Имя вашего родственника", data["language"])} : {data["name_cousen"]} \n'
            f'{_("Телефон вашего родственника", data["language"])} : {data["phone_Number_cousen"]} \n'
            f'{_("Тип  отношения с родственником", data["language"])} : {data["relative_cousen"]} \n'
            f'{_("Имя Отца", data["language"])} : {data["father_name"]} \n'
            f'{_("Имя матери", data["language"])} : {data["mother_name"]} \n'
            f'{_("Катар для переезда и работы", data["language"])} : {data["gatar"]} \n'
            f'{_("ОАЭ для переезда и работы", data["language"])} : {data["UAE"]} \n'
            f'{_("Бахрейн для переезда и работы", data["language"])} : {data["Bahrain"]} \n'
            f'{_("Оман для переезда и работы", data["language"])} : {data["Oman"]} \n'
            f'{_("Оброзование (степень)", data["language"])} : {data["education_stepen"]} \n'
            f'{_("Наименование вуза или колледжа", data["language"])} : {data["university_name"]} \n'
            f'{_("Специализация или факультет", data["language"])} : {data["special_degree"]} \n'
            f'{_("Годы обучения", data["language"])} : {data["year_of_Education"]} \n'
        )
        if data["postgraduate_access"]=="yes":
            foure_block = (
            f'{_("Годы Наличие Последипломное образование (степень)", data["language"])} : {data["postgraduate_degree"]} \n'
            f'{_("Наименование вуза или колледжа (Последипломное образование)", data["language"])} : {data["postgraduate_name"]} \n'
            f'{_("Специализация или факультет (Последипломное образование)", data["language"])} : {data["postgraduate_special"]} \n'
            f'{_("Годы обучения (Последипломное образование)", data["language"])} : {data["postgraduate_date"]} \n'
            )
        else: 
            foure_block = 'have not postgraduate \n'
        
        if data["course_access"]=="yes":
            fifth_block = (
            f'{_("Дополнительные курсы", data["language"])} : {data["сourse_name"]} \n'
            f'{_("Время прохождения курса", data["language"])} : {data["course_date"]} \n'
            f'{_("Место прохождения курса", data["language"])} : {data["Course_place"]} \n'
            )
            if data["doc_course_access"]=="yes":
                fifth_block+=f'{_("Наличие сертификата пройденного курса", data["language"])} : {_("Да", data["language"])} \n'
                Course_Photo = data["Course_Photo"]
            else:
                fifth_block+=f'{_("Наличие сертификата пройденного курса", data["language"])} : {_("Нет", data["language"])} \n'

        else: 
            fifth_block = 'have not course \n'

        if data["tattoo_access"]=="yes":
            six_block = f'{_("Описание тату или пирсинга", data["language"])} : {data["tattoo_discribe"]} \n'
            tattoo_Photo= data["tattoo_Photo"]
        else: 
            six_block = 'have not tattoo \n'

        seventh_block = (
            f'{_("Опыт работы", data["language"])} : {data["work_exp"]} \n'
            f'{_("Имя компании", data["language"])} : {data["work_name"]} \n'
            f'{_("Местоположение компании", data["language"])} : {data["work_place"]} \n'
            f'{_("Должность", data["language"])} : {data["work_position"]} \n'
            f'{_("Ваши обязанности", data["language"])} : {data["work_responsibilities"]} \n'
            )
        
        if data["other_work_access"]=="yes":
            eithg_block = (
            f'{_("Опыт работы", data["language"])} : {data["other_work_exp"]} \n'
            f'{_("Имя компании", data["language"])} : {data["other_work_name"]} \n'
            f'{_("Местоположение компании", data["language"])} : {data["other_work_place"]} \n'
            f'{_("Должность", data["language"])} : {data["other_work_position"]} \n'
            f'{_("Ваши обязанности", data["language"])} : {data["other_work_responsibilities"]} \n'
            )
        else: 
            eithg_block = 'have not other work \n'
        
        if data["now_work_access"]=="yes":
            nine_block = (
            f'{_("Работа (сечас)", data["language"])}\n'
            f'{_("Опыт работы", data["language"])} : {data["now_work_exp"]} \n'
            f'{_("Имя компании", data["language"])} : {data["now_work_name"]} \n'
            f'{_("Местоположение компании", data["language"])} : {data["now_work_place"]} \n'
            f'{_("Должность", data["language"])} : {data["now_work_position"]} \n'
            f'{_("Ваши обязанности", data["language"])} : {data["now_work_responsibilities"]} \n'
            )
        else: 
            nine_block = 'have not other work \n'
        
        tenth_block = (
            f'{_("Компьютерные программы, с которыми вы работаете", data["language"])} \n'
            f'{_("для гостеприимства", data["language"])} : {data["hoste_program"]} \n'
            f'{_("для финансов", data["language"])} : {data["finance_program"]} \n'
            f'{_("для путешествий и бронирования", data["language"])} : {data["travel_program"]} \n'
            f'{_("для графики и дизайн", data["language"])} : {data["graph_program"]} \n'
            )
        
        if data["car_access"]=="yes":
            car_category = f'{_("Категория водительских прав", data["language"])} : {data["car_category"]} \n'
            eleventh_block = f'car_category : {data["car_category"]} \n'
        else: 
            eleventh_block = 'have not car passport \n'

        twelvth_block = (
            f'{_("Уровень русского языка", data["language"])} : {data["russian"]} \n'
            f'{_("Уровень английского языка", data["language"])} : {data["english"]} \n'
            )

        if data["other_lang_access"]=="Yes":
            third_block = (
            f'{_("Дополнительный язык", data["language"])} : {data["added_language"]} \n'
            f'{_("Уровень дополнительного языка", data["language"])} : {data["other_lang_level"]} \n'
            )
        else: 
            third_block = 'have not other lang \n'
        
        fourth_block =  f'know_about_as : {data["know_about_as"]} \n'
        fifth_block = f'{_("Дата создания заявки", data["language"])} : {callback.message.date.strftime("%d %B %H:%M")} \n'

        message_data = (first_block + second_block + third_block + foure_block + fifth_block + 
                        six_block + seventh_block + eithg_block + nine_block + tenth_block +
                        eleventh_block + twelvth_block + third_block + fifth_block )
        await state.update_data(resume_creating_date = callback.message.date.strftime("%d %B %H:%M"))
        
        print('Ваши данные \n'+f'{message_data}')
        print('\n data_set: \n')
        print(data)
        await callback.message.edit_text(_('Ваши данные', data['language'])+f'\n{message_data}',reply_markup = send_kb.as_markup())

@dp.callback_query(lambda c: c.data and c.data.startswith('Save_data'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    msg = f'Новое резюме: {data["full_name"] }'
    # url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id=450142398&text={msg}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id=836047649&text={msg}"
    print(requests.get(url).json())
    save_document(data, callback.message.from_user.id)

    
    await callback.message.edit_text(_('Ваше резюме успешно отправлено!', data['language']))

@dp.callback_query(lambda c: c.data and c.data.startswith('Delete_data'))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.clear()
    await callback.message.edit_text(_('Введите данные заново.', data['language'])+'\n'+_('Введите /start', data['language']))

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
    
def replace_text(doc, old_text, new_text):
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if old_text in paragraph.text:
                        inline = paragraph.runs
                        for i in range(len(inline)):
                            if old_text in inline[i].text:
                                text = inline[i].text.replace(old_text, new_text)
                                inline[i].text = text

if __name__ == "__main__":
    asyncio.run(main())
