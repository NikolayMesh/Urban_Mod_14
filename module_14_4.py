from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from  aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import TokenBot
from crud_functions import get_all_products, get_title_products


bot = Bot(token = TokenBot.api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton( text= 'Информация')
button2 = KeyboardButton( text= 'Рассчитать')
button3 = KeyboardButton( text= 'Купить')
kb.row(button, button2)
kb.row(button3)

ki = InlineKeyboardMarkup()
button3 = InlineKeyboardButton( text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton( text='Формулы расчёта', callback_data='formulas')
ki.row(button3,button4)


catalog_kb =  types.InlineKeyboardMarkup(row_width=4)
title = get_title_products()
for product in title:
    catalog_kb.row(types.InlineKeyboardButton(text=f'{product[0]}', callback_data="product_buying"))

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    activity = State()
    gender = State()

@dp.message_handler(commands =['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = kb)

@dp.message_handler(text =['Информация'])
async def inform(message):
    await message.answer("Информация о боте.")

@dp.message_handler(text =['Рассчитать'])
async def main_menu(message):
    await message.answer("Выбери опцию:",reply_markup = ki )

@dp.message_handler(text =['Купить'])
async def get_buying_list(message):
    products = get_all_products()

    if not products:
        await message.answer("Нет доступных продуктов.")
        return

    for product in products:
        product_id, title, description, price = product
        product_info = f'Название: {title} | Описание: {description} | Цена: {price}'
        await message.answer(product_info)

        try:
            with open(f'{product_id}.jpeg', 'rb') as img:
                await message.answer_photo(photo=img)
        except FileNotFoundError:
            await message.answer("Изображение не найдено.")

    await message.answer("Выберите продукт для покупки:", reply_markup=catalog_kb)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call: types.CallbackQuery):
    await call.answer("Вы успешно приобрели продукт!")
    await call.message.answer("Спасибо за покупку!")



@dp.callback_query_handler(text =['formulas'])
async def get_formulas(call):
    await call.message.answer("для мужчин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A;\n"
                              "для женщин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161) x A.\n"
                              "A – это уровень активности человека, его различают обычно по пяти степеням "
                              "физических нагрузок в сутки:\n"
                              "1 - Минимальная активность: A = 1,2.\n"
                              "2 - Слабая активность: A = 1,375.\n"
                              "3 - Средняя активность: A = 1,55.\n"
                              "4 - Высокая активность: A = 1,725.\n"
                              "5 - Экстра-активность: A = 1,9.")
    await call.answer()

@dp.callback_query_handler(text =['calories'])
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_weight(message, state):
    await state.update_data(weight = message.text)
    await message.answer("Выберите свою активность: Минимальная - 1, Слабая - 2 , Средняя - 3, Высокая - 4, Экстра - 5")
    await UserState.activity.set()

@dp.message_handler(state=UserState.activity)
async def set_weight(message, state):
    await state.update_data(activity = message.text)
    await message.answer("Введите свой пол: Мужчина- 1, Женщина - 0  ")
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender=message.text)

    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    activity = int(data['activity'])
    gender = float(data['gender'])

    if gender:
        if activity == 1:
            calories = (10 * weight + 6.25 * growth - 5 * age + 5) * 1.2
        elif activity == 2:
            calories = (10 * weight + 6.25 * growth - 5 * age + 5) * 1.375
        elif activity == 3:
            calories = (10 * weight + 6.25 * growth - 5 * age + 5) * 1.55
        elif activity == 4:
            calories = (10 * weight + 6.25 * growth - 5 * age + 5) * 1.725
        else:
            calories = (10 * weight + 6.25 * growth - 5 * age + 5) * 1.9
    else:
        if activity == 1:
            calories = (10 * weight + 6.25 * growth - 5 * age - 161) * 1.2
        elif activity == 2:
            calories = (10 * weight + 6.25 * growth - 5 * age - 161) * 1.375
        elif activity == 3:
            calories = (10 * weight + 6.25 * growth - 5 * age - 161) * 1.55
        elif activity == 4:
            calories = (10 * weight + 6.25 * growth - 5 * age - 161) * 1.725
        else:
            calories = (10 * weight + 6.25 * growth - 5 * age - 161) * 1.9

    await message.answer(f'Ваша норма калорий: {calories:.2f} ккал.')

    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)