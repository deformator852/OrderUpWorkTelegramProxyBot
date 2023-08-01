from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# admin keyboards
admb1 = InlineKeyboardButton(text="Принять", callback_data="command_join_approve")
admb2 = InlineKeyboardButton(text="Отказать", callback_data="command_join_reject")

admin_choice_kb = InlineKeyboardMarkup()
admin_choice_kb.add(admb1).add(admb2)

# ---------------------------

adb1 = KeyboardButton("/change_wellcome_message")
adb2 = KeyboardButton("/change_actual_text")
adb3 = KeyboardButton("/sms_texting")
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
admin_kb.add(adb1, adb2, adb3)

# ---------------------------
# Повышение лимита прокси
achpkb1 = InlineKeyboardButton(text="Принять", callback_data="command_proxy_approve")
achpkb2 = InlineKeyboardButton(text="Отказать", callback_data="command_proxy_reject")

admin_choice_proxy_limit_kb = InlineKeyboardMarkup()
admin_choice_proxy_limit_kb.add(achpkb1).add(achpkb2)

# ---------------------------
# Повышение лимита аккаунтов
acalb1 = InlineKeyboardButton(text="Принять", callback_data="command_account_approve")
acalb2 = InlineKeyboardButton(text="Отказать", callback_data="command_account_reject")

admin_choice_account_limit_kb = InlineKeyboardMarkup()
admin_choice_account_limit_kb.add(acalb1).add(acalb2)
# ---------------------------
# Снятие денег с баланса

acgbb1 = InlineKeyboardButton(text="Принять", callback_data="command_balance_approve")
acgbb2 = InlineKeyboardButton(text="Отказать", callback_data="command_balance_reject")

admin_choice_get_balance_kb = InlineKeyboardMarkup()
admin_choice_get_balance_kb.add(acgbb1).add(acgbb2)
# ---------------------------
# user keyboards

state_back_button = InlineKeyboardButton(text="⬅️Назад", callback_data="command_state_back")
state_back_button_kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
state_back_button_kb.add(state_back_button)

# ---------------------------

userb1 = KeyboardButton("Мой профиль")
userb2 = KeyboardButton("Материалы для работы")
userb3 = KeyboardButton("Получить текст")

user_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
user_kb.add(userb1, userb2, userb3)
# ---------------------------
# Кнопки для получения прокси и аккаунта

get_proxy_button = InlineKeyboardButton(text="🌐Получить прокси", callback_data="command_get_proxy")
# get_account_button = InlineKeyboardButton(text="🔐Получить аккаунт", callback_data="command_get_account")

material_kb = InlineKeyboardMarkup()
material_kb.add(get_proxy_button)
# ---------------------------
mpkb1 = InlineKeyboardButton(text="🔗Привязка кошелька", callback_data="command_bind_wallet")
mpkb2 = InlineKeyboardButton(text="⬆️Повысить лимит прокси", callback_data="command_raise_proxy_limit")
mpkb3 = InlineKeyboardButton(text="💸Вывести средства", callback_data="command_get_balance")

my_profile_keyboard = InlineKeyboardMarkup()
my_profile_keyboard.add(mpkb1).add(mpkb2).add(mpkb3)
# ---------------------------
# Кнопки для получения прокси

ccpkb1 = InlineKeyboardButton(text="🇦🇺Австралия", callback_data="command_proxy_australia")
ccpkb2 = InlineKeyboardButton(text="🇩🇪Германия", callback_data="command_proxy_germany")
ccpkb3 = InlineKeyboardButton(text="🇨🇦Канада", callback_data="command_proxy_canada")
ccpkb4 = InlineKeyboardButton(text="🇨🇭Швейцария", callback_data="command_proxy_switzerland")
ccpkb5 = InlineKeyboardButton(text="🇺🇸США", callback_data="command_proxy_usa")
ccpkb6 = InlineKeyboardButton(text="🇩🇰Дания", callback_data="command_proxy_denmark")
ccpkb7 = InlineKeyboardButton(text="🇬🇧Великобритания", callback_data="command_proxy_great_britian")
ccpkb8 = InlineKeyboardButton(text="🇪🇸Испания", callback_data="command_proxy_spain")
ccpkb9 = InlineKeyboardButton(text="🇫🇷Франция", callback_data="command_proxy_france")
ccpkb10 = InlineKeyboardButton(text="🇧🇪Бельгия", callback_data="command_proxy_belgium")
ccpkb11 = InlineKeyboardButton(text="🇦🇹Австрия", callback_data="command_proxy_austria")
ccpkb12 = InlineKeyboardButton(text="🇳🇱Нидерланды", callback_data="command_proxy_netherlands")
ccpkb13 = InlineKeyboardButton(text="🇮🇹Италия",callback_data="command_proxy_italy")
choice_country_proxy_kb = InlineKeyboardMarkup()
choice_country_proxy_kb.add(ccpkb1,ccpkb2,ccpkb3).add(ccpkb4,ccpkb5,ccpkb6).add(ccpkb7,ccpkb8,ccpkb9).add(ccpkb10,ccpkb11,ccpkb12).add(ccpkb13)
# ---------------------------
