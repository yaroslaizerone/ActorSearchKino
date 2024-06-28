from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    wait_word_search = State()


