from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder

from bot.bot_init import bot as image_bot, bot
from bot.handlers.handler_func import API_KEY
from bot.keyboards.keyboards_method import create_movie_buttons
from bot.kino_poisk_search import get_actor_by_id, get_movie_by_id
from bot.states.user_state import UserState

callback_router = Router()
page = 1
movies = []


@callback_router.callback_query(F.data == "info")
async def InfoBot(callback: types.CallbackQuery):
    faq_text = (
        "📋 FAQ:\n\n"
        "1. Как начать пользоваться ботом?\n"
        "   Для начало просто введите команду /start и следуйте инструкциям.\n\n"
        "2. Как найти актёра?\n"
        "   Нажмите кнопку '🤸‍♂️Поиск актёра' и введите имя или фамилию актёра.\n\n"
        "3. Как узнать информацию о фильме?\n"
        "   После того как вы найдёте актёра, нажмите на его имя, чтобы увидеть список фильмов. "
        "Нажмите на название фильма для получения подробной информации."
    )
    await callback.message.answer(faq_text)


@callback_router.callback_query(F.data == "start_search")
async def InfoBot(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Для того, чтобы найти актёра, вам необходимо указать ориентир для его поиска."
                                  " 🔍 Это может быть фамилия или имя."
                                  " Если вы не знаете полного имени или фамилии, можете указать фразу. 💬\n\n"
                                  "🔴 Укажите данные для поиска:")
    await state.set_state(UserState.wait_word_search)


@callback_router.callback_query(lambda c: c.data.isdigit())
async def process_actor_callback(callback_query: types.CallbackQuery, state: FSMContext):
    global page
    page = 0
    info_message = ""

    actor_id = callback_query.data
    actor_info = get_actor_by_id(actor_id, API_KEY)
    name = actor_info.get('name')
    if name:
        info_message = info_message + f"👤 Имя: {name}\n"
    en_name = actor_info.get('enName')
    if en_name:
        info_message = info_message + f"🇬🇧 Имя на английском: {en_name}\n"
    birthday = actor_info.get('birthday')

    if birthday:
        birthday = birthday.split('T')[0]
        info_message = info_message + f"👶 Дата рождения: {birthday}\n"

    birth_place = actor_info.get('birthPlace')
    if birth_place:
        birth_place = ", ".join([place['value'] for place in birth_place])
        info_message = info_message + f"🏠 Место рождения: {birth_place}\n"

    age = actor_info.get('age')
    if age:
        info_message = info_message + f"🔟 Возраст: {age}\n"

    sex = actor_info.get('sex', "Пол не указан")
    if sex:
        info_message = info_message + f"🎚 Пол: {sex}\n"

    global movies
    movies = actor_info.get('movies', [])
    photo_url = actor_info.get('photo')

    if movies:
        info_message = info_message + "🎥 Фильмы:"
    else:
        info_message = info_message + "📛 Актёр не снимался в фильмах"

    keyboard = create_movie_buttons(movies, page)
    page = page + 1

    if photo_url:
        await image_bot.send_photo(chat_id=callback_query.from_user.id, photo=photo_url,
                                   caption=info_message, reply_markup=keyboard)
    else:
        await image_bot.send_message(callback_query.from_user.id, info_message, reply_markup=keyboard)


@callback_router.callback_query(lambda c: c.data.startswith("movie_"))
async def process_movie_callback(callback_query: types.CallbackQuery):
    movie_id = callback_query.data.split("_")[1]
    movie_info = get_movie_by_id(movie_id, API_KEY)

    movie_message = ""

    title = movie_info.get('name') or movie_info.get('alternativeName')
    if title:
        movie_message = movie_message + f"🎬 Название: {title}\n"

    year = movie_info.get('year')
    if year:
        movie_message = movie_message + f"📅 Год: {year}\n"
    description = movie_info.get('description')
    if description:
        short_description = ""
        for i in range(0, 4):
            try:
                short_description = short_description + description.split('.')[i]
            except IndexError:
                print("Егор")

        short_description = short_description + "..."
        print(short_description)
        movie_message = movie_message + f"📝 Описание: {short_description}\n"
    slogan = movie_info.get('slogan')
    if slogan:
        movie_message = movie_message + f"💬 Слоган: {slogan}\n"
    rating_kp = movie_info.get('rating', {}).get('kp')
    if rating_kp:
        movie_message = movie_message + f"⭐ Рейтинг Кинопоиск: {rating_kp}\n"
    rating_imdb = movie_info.get('rating', {}).get('imdb')
    if rating_imdb:
        movie_message = movie_message + f"🌟 Рейтинг IMDb: {rating_imdb}\n"
    movie_length = movie_info.get('movieLength')
    if movie_length:
        movie_message = movie_message + f"⏱️ Длительность: {movie_length} минут\n"
    genres = ", ".join([genre['name'] for genre in movie_info.get('genres', [])])
    if genres:
        movie_message = movie_message + f"🎭 Жанры: {genres}\n"
    countries = ", ".join([country['name'] for country in movie_info.get('countries', [])])
    if countries:
        movie_message = movie_message + f"🌍 Страны: {countries}"
    poster_url = movie_info.get('poster', {}).get('url')

    if poster_url:
        media_group = MediaGroupBuilder(caption=movie_message)
        media_group.add(type="photo", media=poster_url)
        await callback_query.message.answer_media_group(media=media_group.build())
    else:
        await image_bot.send_message(callback_query.from_user.id, movie_message)


@callback_router.callback_query(lambda c: c.data.startswith("page_"))
async def process_page_callback(callback_query: types.CallbackQuery, state: FSMContext):
    page = int(callback_query.data.split('_')[1])
    keyboard = create_movie_buttons(movies, page)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
