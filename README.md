Documentation: How to Install and Run a Telegram Bot with aiogram

This documentation provides a step-by-step guide on how to install and run a Telegram bot using the aiogram library, a powerful and flexible Python framework for developing Telegram bots.
Prerequisites

Before proceeding, make sure you have the following prerequisites installed on your system:

1.)Python (3.6 or higher)
2.)Pip (Python package manager)
3.)PostgreSQL

Step 1: Install dependencies

To install dependencies, open your terminal or command prompt and run the following command:
pip install -r requirements.txt


Step 2: fill out the variables 

1.)main.py
TOKEN = 'YOUR TELEGRAM TOKEN BOT'

2.)bot_handlers.py and bot_handlers_country_proxy.py
USER = ''
PASSWORD = ''
HOST = ''
PORT = ''
DATABASE = ''

3.)bot_handlers_country_proxy.py
PROXY_API_KEY = 'YOUR API KEY FOR PROXY SERVICE'

Step 3: running

open your terminal or command prompt and run the following command:
python3 main.py
