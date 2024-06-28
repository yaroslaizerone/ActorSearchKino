import os

from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from bot.bot_init import bot
from bot.keyboards.keyboards_method import StartMenu, find_actor_keyboard
from bot.kino_poisk_search import search_actor_by_name
from bot.states.user_state import UserState

router = Router()
API_KEY = token_bot = os.environ["KINO_KEY"]
actors = []
page_actor = 1


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        text="🎥 Привет, я Бот FullFilm!\n"
        "Я могу помочь тебе найти актёра по имени или даже по первой букве его имени. 📚\n"
        "Вот как я могу быть полезен:\n"
        "1. Поиск актёров по именам: Введи имя актёра, и я найду его для тебя. 👤\n"
        "2. Поиск по первой букве: Не помнишь имя полностью? Введи первую букву, и я предложу варианты. 🔤\n"
        "3. Информация о фильмах: Узнай, в каких фильмах снимался актёр. 🎬\n"
        "Давай начнём искать твоих любимых актёров! 🌟", reply_markup=StartMenu())


@router.message(UserState.wait_word_search)
async def search_actor(message: types.Message, state: FSMContext):
    actor_name = message.text
    search_results = search_actor_by_name(actor_name, API_KEY)
    global actors, page_actor
    page_actor = 0
    actors = search_results.get('docs', [])

    if actors:
        keyboard = find_actor_keyboard(actors, page_actor)
        page_actor = page_actor + 1
        await message.answer("🔎 Результаты поиска:", reply_markup=keyboard)
    else:
        await message.answer("😭 Актёр не найден.")


@router.callback_query(lambda c: c.data and c.data.startswith('actor'))
async def process_page(callback_query: types.CallbackQuery):
    global page_actor
    page_actor = int(callback_query.data.split('_')[1])
    keyboard = find_actor_keyboard(actors, page_actor)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)