from aiogram.fsm.state import State, StatesGroup


class AddProduct(StatesGroup):
    link_user = State()
    data = State()
    link = State()
    yes_add = State()
    no_add = State()


class LookProduct(StatesGroup):
    start_look = State()


class DelProduct(StatesGroup):
    start_del = State()
