from aiogram.fsm.state import State, StatesGroup


class LinkUser(StatesGroup):
    link = State()
    data = State()
    name = State()
    price = State()
    count = State()