from create_bot import *
from aiogram import executor
from handlers.bot_handlers import register_message_handlers, register_callback_query_handlers
from handlers.bot_handlers_country_proxy import register_choice_country_proxy

register_choice_country_proxy(dp)
register_callback_query_handlers(dp)
register_message_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
