from bot import bot_init
from bot.handlers import handler_func
from bot.call_backs import call_backs_func


def setup():
    bot_init.dp.include_routers(handler_func.router, call_backs_func.callback_router)


if __name__ == '__main__':
    setup()
    bot_init.dp.run_polling(bot_init.bot)