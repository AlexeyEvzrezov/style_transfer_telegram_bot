from aiogram.dispatcher.filters.state import StatesGroup, State


class ImStates(StatesGroup):
    content = State()
    style = State()