import random

from aiogram import types

MOVIES_PER_PAGE = 10
ACTORS_PER_PAGE = 10
start_buttons = ["❓Как мы работаем?", "🤸‍♂️Поиск актёра", ]


def StartMenu():
    buttons = [
        [
            types.InlineKeyboardButton(text=start_buttons[0], callback_data="info"),
            types.InlineKeyboardButton(text=start_buttons[1], callback_data="start_search")
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
    return keyboard


def find_actor_keyboard(actors, page):
    buttons = []
    start = page * ACTORS_PER_PAGE
    end = start + ACTORS_PER_PAGE
    print(f"{len(actors)}-l, {start}-s, {end}-e ")
    for actor in actors[start:end]:
        if actor['sex'] == "Мужской":
            button = types.InlineKeyboardButton(text="🕺 " + actor['name'], callback_data=str(actor['id']))
        else:
            button = types.InlineKeyboardButton(text="💃 " + actor['name'], callback_data=str(actor['id']))
        buttons.append([button])

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"actor_{page - 1}"))
    if end < len(actors):
        navigation_buttons.append(types.InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"actor_{page + 1}"))

    if navigation_buttons:
        buttons.append(navigation_buttons)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
    return keyboard


def create_movie_buttons(movies, page):
    start = page * MOVIES_PER_PAGE
    end = start + MOVIES_PER_PAGE
    movies_page = movies[start:end]
    print(f"{len(movies)}-l, {start}-s, {end}-e ")

    buttons = []
    for movie in movies_page:
        movie_name = movie.get('name') or movie.get('alternativeName') or 'Unknown'
        button = types.InlineKeyboardButton(text=get_random_emoji() + " " + movie_name,
                                            callback_data=f"movie_{movie['id']}")
        buttons.append([button])

    navigation_buttons = []
    if page > 0 and movies != []:
        navigation_buttons.append(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page - 1}"))
    if end < len(movies):
        navigation_buttons.append(types.InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page_{page + 1}"))

    if navigation_buttons:
        buttons.append(navigation_buttons)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
    return keyboard


def get_random_emoji():
    emojis = ["😀", "😂", "😅", "😊", "😍", "😎", "😜", "🤩", "🥳", "😇", "😉", "😋", "😌", "😔", "😢", "😭", "😡", "😱", "🤯 ", "😴", "😷",
              "🤒", "🤕", "🤑", "🤠", "😈", "👻", "💀", "👽", "🤖", "🎃", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿", "😾", "🙈", "🙉",
              "🙊", "🐵 ", "🐶", "🐱", "🐭", "🐹", "🐰", "🦊"]
    return random.choice(emojis)
