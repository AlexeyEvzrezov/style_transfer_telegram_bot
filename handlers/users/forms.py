from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states import Form


@dp.message_handler(Command('form'))
async def fill_name(message: types.Message):
    await message.answer('Введите имя')
    await Form.Q1.set()


@dp.message_handler(state=Form.Q1)
async def fill_email(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name=answer)
    await message.answer('Введите e-mail')
    await Form.Q2.set()


@dp.message_handler(state=Form.Q2)
async def fill_phone(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(email=answer)
    await message.answer('Введите номер телефона')
    await Form.Q3.set()


@dp.message_handler(state=Form.Q3)
async def get_answers(message: types.Message, state: FSMContext):
    form_data = await state.get_data()
    name = form_data.get('name')
    email = form_data.get('email')
    phone = message.text

    await message.answer('Привет! Ты ввел следующие данные:')
    await message.answer(f'Имя: {name}\n'
                         f'Email: {email}\n'
                         f'Телефон: {phone}'
                         )

    await state.finish()

