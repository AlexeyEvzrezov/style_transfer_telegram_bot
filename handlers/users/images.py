from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType

from loader import dp, bot
from models.train import run_nst
from states import ImStates


@dp.message_handler(Command('run'))
async def start_nst(message: types.Message):
    await message.answer('Загрузите изображение, на которое вы хотите перенести стиль')
    await ImStates.content.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=ImStates.content)
async def get_content(message: types.Message, state: FSMContext):
    content_img = await bot.download_file_by_id(message.photo[-1].file_id)
    await state.update_data(content=content_img)
    await message.answer('Загрузите изображение, стиль которого вы хотите перенести')
    await ImStates.style.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=ImStates.style)
async def get_style_ans(message: types.Message, state: FSMContext):
    images = await state.get_data()
    content_img = images.get('content')
    style_img = await bot.download_file_by_id(message.photo[-1].file_id)
    await message.answer('Работа началась, это не так быстро')
    byte_img = run_nst(content_img.getvalue(), style_img.getvalue())
    await message.answer_photo(photo=byte_img)
    await state.finish()


# @dp.message_handler(content_types=types.ContentType.PHOTO)
# async def handle_docs_photo(message: types.Message):
#     img = await bot.download_file_by_id(message.photo[-1].file_id)
#     byte_img = imload(img.getvalue())
#
#     await message.answer(text='sdhsdjddj')
#     await message.answer_photo(photo=byte_img)

