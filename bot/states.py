from aiogram.fsm.state import State, StatesGroup


class DateState(StatesGroup):
    wait_name = State()
    wait_mail = State()
    wait_date = State()