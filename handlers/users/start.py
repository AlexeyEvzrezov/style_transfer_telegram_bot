from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f'Здравствуйте, {message.from_user.full_name}!\n'
        'Здесь вы можете переносить стили одних изображений на другие.\n'
        'Нажмите /run, чтобы начать!'
    )


@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message):
    await message.answer('/start - начало работы\n'
                         '/run - перенос стиля')
