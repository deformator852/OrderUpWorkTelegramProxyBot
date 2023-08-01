from aiogram.dispatcher import FSMContext
from create_bot import bot
from aiogram import types, Dispatcher
from keyboards import bot_keyboards
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import re
import asyncpg

# DATABASE data
USER = ''
PASSWORD = ''
HOST = ''
PORT = ''
DATABASE = ''


class ChangeWelcomeMessage(StatesGroup):
    WaitingForNewMessage = State()


class RejectAnswerMessage(StatesGroup):
    WaitingForRejectMessage = State()


class GetWallet(StatesGroup):
    WaitingForWallet = State()


class GetNewProxyLimit(StatesGroup):
    WaitingForNewProxyLimit = State()


class GetNewAccountLimit(StatesGroup):
    WaitingForNewAccountLimit = State()


class GetBalance(StatesGroup):
    WaitingForBalance = State()


class RejectBalanceMessage(StatesGroup):
    WaitingForRejectBalanceMessage = State()


class ChangeActualText(StatesGroup):
    WaitingForNewActualText = State()


class SmsTexting(StatesGroup):
    WaitingForSmsTexting = State()


async def connect_db(user, password, host, port, database):
    connection = await asyncpg.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )
    return connection


# message handlers
async def command_start(message: types.Message):
    try:
        connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
        admin = await connection.fetchrow(f"SELECT user_id FROM admins WHERE user_id = {message.from_user.id}")
        if not admin:
            result = await connection.fetch(f"SELECT status FROM users WHERE user_id = {message.from_user.id};")
            if result:
                if int(result[0]["status"]) == 2:
                    await bot.send_message(message.from_user.id, "Вы уже авторизованы!",
                                           reply_markup=bot_keyboards.user_kb)
                if int(result[0]["status"]) == 1:
                    await bot.send_message(message.from_user.id, "🔻Вам доступ запрещен🔻")
            else:
                await bot.send_message(message.from_user.id, "🔹 Ваша заявка отправлена!")
                admins = await connection.fetchrow("SELECT user_id FROM admins")
                for adm in admins:
                    await bot.send_message(str(adm),
                                           f"Пользователь c ID: {message.from_user.id} хочет присоединиться",
                                           reply_markup=bot_keyboards.admin_choice_kb)

        if admin:
            await bot.send_message(message.from_user.id, "Админ подключился", reply_markup=bot_keyboards.admin_kb)
    finally:
        await connection.close()


async def change_wellcome_message(message: types.Message):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    if await connection.fetchrow(f"SELECT user_id FROM admins WHERE user_id = {message.chat.id}"):
        await ChangeWelcomeMessage.WaitingForNewMessage.set()
        await bot.send_message(message.from_user.id, "Введите новый текст для поздравительного сообщения: ")


async def change_actual_text(message: types.Message):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    if await connection.fetch(f"SELECT user_id FROM admins WHERE user_id = {message.from_user.id}"):
        try:
            current_actual_text = await connection.fetchrow(f"SELECT actual_text FROM actual_text ")
        except:
            pass
        await bot.send_message(message.from_user.id,
                               f"Текущий актуальный текст:\n {current_actual_text['actual_text']}")
        await ChangeActualText.WaitingForNewActualText.set()
        await bot.send_message(message.from_user.id, "Введите новый текст:")


async def sms_texting(message: types.Message, state: FSMContext):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    if await connection.fetch(f"SELECT user_id FROM admins WHERE user_id = {message.from_user.id}"):
        await SmsTexting.WaitingForSmsTexting.set()
        await bot.send_message(message.from_user.id, "Введите сообщение для рассылки:")


async def command_get_text(message: types.Message):
    if message.text == "Получить текст":
        connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
        if await connection.fetch(f"SELECT user_id FROM approved_users WHERE user_id = {message.from_user.id}"):
            actual_text = await connection.fetchrow("SELECT actual_text FROM actual_text")
            await bot.send_message(message.from_user.id, "📝Актуальный текст для фото:📝")
            await bot.send_message(message.from_user.id, actual_text["actual_text"])


async def handle_sms_texting_message(message: types.Message, state: FSMContext):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    users = await connection.fetchrow(f"SELECT user_id FROM approved_users")
    for user in users:
        await bot.send_message(user, message.text)
    await bot.send_message(message.from_user.id, "Сообщение всем разослано!")
    await state.finish()


async def handle_new_welcome_message(message: types.Message, state: FSMContext):
    new_welcome_message = message.text
    try:
        connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    except Exception as e:
        await bot.send_message(message.from_user.id, f"Ошибка подключения к базе данных!Текст ошибки: {e}")
        await state.finish()
        await connection.close()
        return
    try:
        await connection.execute("UPDATE wellcome_message SET message = ($1);", new_welcome_message)
    except Exception as e:
        await bot.send_message(message.from_user.id,
                               f"Ошибка подключения записи нового поздравительного сообщения!Текст ошибки: {e}")
        await connection.close()
        await state.finish()
        return
    await bot.send_message(message.from_user.id, "Вы успешно поменяли поздравительное сообщение!")
    await connection.close()
    await state.finish()


async def handle_new_actual_text(message: types.Message, state: FSMContext):
    new_actual_text = message.text
    try:
        connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    except:
        await bot.send_message(message.from_user.id,
                               "Ошибка подключения к базе данных при попытке добавить новый актуальный текст")
        await connection.close()
        await state.finish()
        return
    try:
        await connection.execute("""
        INSERT INTO actual_text (id, actual_text)
        VALUES ($1, $2)
        ON CONFLICT (id) DO UPDATE
        SET actual_text = $2
    """, 1, new_actual_text)
        await bot.send_message(message.from_user.id, "Новый актуальный текст добавлен в базу данных!")
    except:
        await bot.send_message(message.from_user.id, "Ошибка при попытке добавить новый актуальный текст!")
        await connection.close()
        await state.finish()
        return
    await state.finish()

async def handle_reject_join_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    await bot.send_message(user_id, "🔴 Ваша заявка была отвергнута!")
    await bot.send_message(user_id, "Причина отказа: " + message.text)
    await state.finish()


async def handle_wallet_message(message: types.Message, state: FSMContext):
    wallet_message = message.text
    match_wallet_message = re.match(r"\w+\w+\s\w{7,}", wallet_message)
    if match_wallet_message:
        connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
        try:
            await connection.fetch("UPDATE approved_users SET wallet = $1 WHERE user_id = $2", wallet_message,
                                   message.from_user.id)
            await bot.send_message(message.from_user.id, "Вы успешно привязали кошелек!")
        except:
            await connection.close()

    else:
        await bot.send_message(message.from_user.id, "Вы неверно ввели данные для привязки, попробуйте снова!",
                               reply_markup=bot_keyboards.user_kb)

    await state.finish()


async def handle_proxy_limit_message(message: types.Message, state: FSMContext):
    new_proxy_limit_message = message.text
    if new_proxy_limit_message.isdigit():
        new_proxy_limit_message = int(new_proxy_limit_message)
        if (new_proxy_limit_message < 1) or (new_proxy_limit_message > 3):
            await bot.send_message(message.from_user.id, "Вы ввели неправильное количество прокси!")
        else:
            await bot.send_message(message.from_user.id, "Заявка на повышение лимитов прокси отправлена✅")
            connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
            admin = await connection.fetchrow(f"SELECT * FROM admins ORDER BY random() LIMIT 1;")
            if admin:
                await bot.send_message(str(admin["user_id"]),
                                       f"Пользователь с ID: {message.from_user.id} хочет увеличить лимит прокси до:{new_proxy_limit_message}",
                                       reply_markup=bot_keyboards.admin_choice_proxy_limit_kb)
    await state.finish()


async def handle_reject_balance_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    await bot.send_message(user_id, "🔴 Ваша заявка была отвергнута!")
    await bot.send_message(user_id, "Причина отказа: " + message.text)
    await state.finish()


async def handle_get_balance_message(message: types.Message, state: FSMContext):
    balance = message.text
    if balance.isdigit():
        connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
        result = await connection.fetch(
            f"SELECT balance, CASE WHEN wallet IS NULL THEN NULL ELSE wallet END as wallet FROM approved_users WHERE user_id = {message.from_user.id}"
        )
        if int(balance) > result[0]["balance"]:
            await bot.send_message(message.from_user.id, "Недостаточно баланса на счету!")
            await state.finish()
            return None
        if result[0]["wallet"] == None:
            await bot.send_message(message.from_user.id, "К вашем аккаунту не привязан кошелек!")
            await state.finish()
            return
        if int(balance) == 0:
            await bot.send_message(message.from_user.id, "Сума снятия не может быть равна 0!")
            await state.finish()
            return None
        await bot.send_message(message.from_user.id,
                               "Ваш запрос на снятие денег с баланса отправлен на обработку администратору!")
        admin = await connection.fetchrow(f"SELECT * FROM admins ORDER BY random() LIMIT 1;")
        if admin:
            await bot.send_message(str(admin["user_id"]),
                                   f"Пользователь с ID: {message.from_user.id} отправил запрос на снятие баланса с кошелька: {result[0]['wallet']} на сумму {balance}",
                                   reply_markup=bot_keyboards.admin_choice_get_balance_kb)
        await state.finish()

    else:
        await bot.send_message(message.from_user.id, "Вы ввели некоректное значение!")
        await state.finish()
    await state.finish()


async def command_my_profile(message: types.Message):
    if message.text == "Мой профиль":
        connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
        result = await connection.fetch(
            f"SELECT id,balance,proxy_limit FROM approved_users WHERE user_id = {message.from_user.id};")
        if result:
            await bot.send_message(message.from_user.id, f"""
👨‍💻Ваш профиль:\n
🔑ID:{result[0][0]}
💰Баланс:{result[0][1]}$
❌Лимит прокси:{result[0][2]}
""", reply_markup=bot_keyboards.my_profile_keyboard)
            await connection.close()
        else:
            await bot.send_message(message.from_user.id, "Вы не авторизованы!")


async def command_materials_for_work(message: types.Message):
    if message.text == "Материалы для работы":
        connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
        if await connection.fetch(f"SELECT user_id FROM approved_users WHERE user_id = {message.from_user.id}"):
            await bot.send_message(message.from_user.id, "🗃 Выберите вариант:", reply_markup=bot_keyboards.material_kb)
        else:
            await bot.send_message(message.from_user.id, "Вы не авторизованы!")


# -------------
async def command_raise_proxy_limit(callback: types.CallbackQuery, state: FSMContext):
    await GetNewProxyLimit.WaitingForNewProxyLimit.set()
    await bot.send_message(callback.message.chat.id, "✔️Напишите желаемое количество прокси (от 1 до 3): ",
                           reply_markup=bot_keyboards.state_back_button_kb)


async def command_state_back(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, "Вы вернулись назад!",
                           reply_markup=bot_keyboards.user_kb)
    await state.finish()


async def command_get_balance(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, "💸 Введите сумму вывода:")
    await GetBalance.WaitingForBalance.set()


# callback handlers
async def command_join_reject(callback: types.CallbackQuery, state: FSMContext):
    data = callback.message
    text = data["text"]
    match = re.search(r"ID: (\d+)", text)
    user_id = int(match.group(1))
    try:
        connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    except Exception as e:
        await bot.send_message(callback.message.chat.id,
                               f"Ошибка подключения к базе данных при попытке добавить нового пользователя!Текст ошибки: e")
    result = await connection.fetchrow(f"SELECT status FROM users WHERE user_id = '{user_id}'")
    if result:
        if result["status"] == 1:
            await bot.send_message(callback.message.chat.id, "Этому пользователю уже было отказано в доступе!")
            await connection.close()
            await state.finish()
            return

        elif result["status"] == 2:
            await bot.send_message(callback.message.chat.id, "Этот пользователь уже добавлен в базу данных!")
            await connection.close()
            await state.finish()
            return

    try:
        await connection.fetch(f"INSERT INTO users (user_id,status) VALUES({user_id},1);")
    except Exception as e:
        await bot.send_message(callback.message.chat.id, "Ошибка во время записи отказа в доступе к боту!")
        await connection.close()
        await state.finish()

    await RejectAnswerMessage.WaitingForRejectMessage.set()
    await state.update_data(user_id=user_id)
    await bot.send_message(callback.message.chat.id, f"Причина отказа пользователю: ")
    await connection.close()


async def command_join_approve(callback: types.CallbackQuery):
    data = callback.message
    text = data["text"]
    match = re.search(r"ID: (\d+)", text)
    user_id = int(match.group(1))
    try:
        connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    except Exception as e:
        await bot.send_message(callback.message.chat.id,
                               f"Ошибка подключения к базе данных при попытке добавить нового пользователя!Текст ошибки: e")
        await bot.send_message(user_id,
                               "При попытке принять ваш запрос возникла ошибка!Попробуйте повторить запрос немного позже!")
        return

    try:
        check = await connection.fetch(f"SELECT status FROM users WHERE user_id = {user_id}")
        if check:
            if check[0]["status"] == 2:
                await bot.send_message(callback.message.chat.id, "Этот аккаунт уже добавлен в базу данных!")
                await connection.close()
                return
            elif check[0]["status"] == 1:
                await bot.send_message(callback.message.chat.id, "Этому пользователю уже было отказано в доступе!")
                await connection.close()
                return
    except Exception as e:
        await bot.send_message(callback.message.chat.id, "Ошибка при проверке есть ли аккаунт в бд")
        await connection.close()
        return
    try:
        await connection.fetch(
            f"INSERT INTO users (user_id,status) VALUES({user_id},2);")
    except Exception as e:
        await bot.send_message(callback.message.chat.id, "Ошибка с записью данных,аккаунт небыл добавлен.")
        await bot.send_message(user_id,
                               "При попытке принять ваш запрос возникла ошибка!Попробуйте повторить запрос немного позже!")
        await connection.close()
        return

    try:
        await connection.fetch(
            f"INSERT INTO approved_users (user_id,proxy_limit,balance,account_limit,proxy_count,account_count) VALUES({user_id},1,0,3,0,0);")
        wellcome_message_row = await connection.fetchrow("SELECT wellcome_message FROM wellcome_message")
        wellcome_message = wellcome_message_row[0]["message"]
        await bot.send_message(user_id, "🟢 Ваша заявка была принята!")
        await bot.send_message(user_id, wellcome_message)
        await bot.send_message(user_id, "🔑", reply_markup=bot_keyboards.user_kb)

    except Exception as e:
        await bot.send_message(callback.message.chat.id, "Ошибка с записью данных,аккаунт небыл добавлен")
        await connection.fetch(
            f"DELETE FROM users WHERE user_id = {user_id}")
        await connection.close()
        return

    await connection.close()


async def command_bind_wallet(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, """
🔗 Отправьте кошелёк TRC-20 в формате 
монета - адрес
Пример: TRX  TYMSMUMq8p12345678Q3PihXmkLj4M1234
    """, reply_markup=bot_keyboards.state_back_button_kb)
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    result = await connection.fetch(
        f"SELECT wallet, CASE WHEN wallet IS NOT NULL THEN 'notnull' ELSE 'isnull' END FROM approved_users WHERE user_id = {callback.from_user.id}")
    await connection.close()
    if result[0]["wallet"] != None:
        await bot.send_message(callback.from_user.id, f"Подключенный кошелёк: {result[0][0]}")
    await GetWallet.WaitingForWallet.set()


async def command_proxy_approve(callback: types.CallbackQuery):
    new_proxy_limit_message = callback.message.text
    match_id = re.search(r"ID: (\d+)", new_proxy_limit_message)
    user_id = int(match_id.group(1))
    limit = new_proxy_limit_message[-1]
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    await connection.fetch(f"UPDATE approved_users SET proxy_limit = {limit} WHERE user_id = {user_id};")
    await connection.close()
    await bot.send_message(user_id, f"Ваша заявка на повышение лимита прокси до {limit} была одобрена! ✅")


async def command_proxy_reject(callback: types.CallbackQuery):
    new_proxy_limit_message = callback.message.text
    match_id = re.search(r"ID: (\d+)", new_proxy_limit_message)
    user_id = int(match_id.group(1))
    limit = new_proxy_limit_message[-1]
    await bot.send_message(user_id, f"Ваша заявка на повышение лимита прокcи до {limit} была отвергнута ❌")


async def command_account_approve(callback: types.CallbackQuery):
    new_account_limit_message = callback.message.text
    match_id = re.search(r"ID: (\d+)", new_account_limit_message)
    user_id = int(match_id.group(1))
    limit = new_account_limit_message[-1]
    await bot.send_message(user_id, f"Ваша заявка на повышение лимита аккаунтов до {limit} была принята!✅")
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    await connection.fetch(f"UPDATE approved_users SET account_limit = {limit} WHERE user_id = {user_id};")
    await connection.close()


async def command_account_reject(callback: types.CallbackQuery):
    new_account_limit_message = callback.message.text
    match_id = re.search(r"ID: (\d+)", new_account_limit_message)
    user_id = int(match_id.group(1))
    limit = new_account_limit_message[-1]
    await bot.send_message(user_id, f"Ваша заявка на повышение лимита аккаунтов до {limit} была отвергнута ❌")


async def command_balance_approve(callback: types.CallbackQuery):
    balance_message = callback.message.text
    match_id = re.search(r"ID: (\d+)", balance_message)
    user_id = int(match_id.group(1))
    await bot.send_message(user_id, f"Ваша заявка на снятие баланса со счёта прийнята!")
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    database_balance = await connection.fetch(f"SELECT balance FROM approved_users WHERE user_id = {user_id};")
    match_balance = re.search(r'сумму (\d+)', balance_message)
    new_balance = database_balance[0]["balance"] - int(match_balance.group(1))
    await connection.fetch(f"UPDATE approved_users SET balance = {new_balance} WHERE user_id = {user_id};")
    await connection.close()


async def command_balance_reject(callback: types.CallbackQuery, state: FSMContext):
    balance_message = callback.message.text
    match_id = re.search(r"ID: (\d+)", balance_message)
    user_id = int(match_id.group(1))
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    if await connection.fetch(f"SELECT user_id FROM admins WHERE user_id = {callback.message.chat.id}"):
        await RejectBalanceMessage.WaitingForRejectBalanceMessage.set()
        await state.update_data(user_id=user_id)
        await bot.send_message(callback.message.chat.id, f"Причина отказа пользователю: ")


async def command_get_proxy(callback: types.CallbackQuery):
    await bot.send_message(callback.message.chat.id, "🌏Выберите страну прокси:",
                           reply_markup=bot_keyboards.choice_country_proxy_kb)


def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands="start")
    dp.register_message_handler(change_wellcome_message, commands="change_wellcome_message", state=None)
    dp.register_message_handler(handle_new_welcome_message, state=ChangeWelcomeMessage.WaitingForNewMessage)
    dp.register_message_handler(handle_reject_join_message, state=RejectAnswerMessage.WaitingForRejectMessage)
    dp.register_message_handler(handle_wallet_message, state=GetWallet.WaitingForWallet)
    dp.register_message_handler(handle_proxy_limit_message, state=GetNewProxyLimit.WaitingForNewProxyLimit)
    dp.register_message_handler(handle_sms_texting_message, state=SmsTexting.WaitingForSmsTexting)
    dp.register_message_handler(handle_new_actual_text, state=ChangeActualText.WaitingForNewActualText)
    dp.register_message_handler(command_my_profile, Text(equals="Мой профиль"))
    dp.register_message_handler(command_materials_for_work, Text(equals="Материалы для работы"))
    dp.register_message_handler(handle_get_balance_message, state=GetBalance.WaitingForBalance)
    dp.register_message_handler(handle_reject_balance_message,
                                state=RejectBalanceMessage.WaitingForRejectBalanceMessage)
    dp.register_message_handler(command_get_text, Text(equals="Получить текст"))
    dp.register_message_handler(change_actual_text, commands="change_actual_text")
    dp.register_message_handler(sms_texting, commands="sms_texting", state=None)


def register_callback_query_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(command_join_approve,
                                       lambda callback_query: callback_query.data == "command_join_approve", state=None)
    dp.register_callback_query_handler(command_join_reject,
                                       lambda callback_query: callback_query.data == "command_join_reject",
                                       state=None)
    dp.register_callback_query_handler(command_bind_wallet,
                                       lambda callback_query: callback_query.data == "command_bind_wallet", state=None)
    dp.register_callback_query_handler(command_proxy_approve,
                                       lambda callback_query: callback_query.data == "command_proxy_approve")
    dp.register_callback_query_handler(command_proxy_reject,
                                       lambda callback_query: callback_query.data == "command_proxy_reject")
    dp.register_callback_query_handler(command_raise_proxy_limit,
                                       lambda callback_query: callback_query.data == "command_raise_proxy_limit",
                                       state=None)
    dp.register_callback_query_handler(command_account_approve,
                                       lambda callback_query: callback_query.data == "command_account_approve")
    dp.register_callback_query_handler(command_account_reject,
                                       lambda callback_query: callback_query.data == "command_account_reject")
    dp.register_callback_query_handler(command_get_balance,
                                       lambda callback_query: callback_query.data == "command_get_balance", state=None)
    dp.register_callback_query_handler(command_balance_approve,
                                       lambda callback_query: callback_query.data == "command_balance_approve")
    dp.register_callback_query_handler(command_balance_reject,
                                       lambda callback_query: callback_query.data == "command_balance_reject",
                                       state=None)
    dp.register_callback_query_handler(command_get_proxy,
                                       lambda callback_query: callback_query.data == "command_get_proxy")
    dp.register_callback_query_handler(command_state_back,
                                       lambda callback_query: callback_query.data == "command_state_back",
                                       state="*")
