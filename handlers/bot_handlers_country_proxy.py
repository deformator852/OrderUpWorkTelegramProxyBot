from create_bot import bot
from aiogram import types, Dispatcher
import asyncpg
import datetime
import requests

PROXY_API_KEY = ""

# DATABASE data
USER = ''
PASSWORD = ''
HOST = ''
PORT = ''
DATABASE = ''


async def connect_db(user, password, host, port, database):
    connection = await asyncpg.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )
    return connection


async def command_proxy_australia(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'AU,Oceania',
                'type_filter': 'DCH',
                'sort': 'speed-desc',
                'area_filter': '25',
                'city': 'empty',
                'zip': 'empty',
                'country': 'empty',
                'page': '1'
            }

            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 600 and (float(proxy["price"]) >= 0.6 and float(proxy["price"]) <= 0.75)):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - Australia \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


async def command_proxy_germany(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'Europe',
                'type_filter': 'DCH',
                'sort': 'speed-desc',
                'area_filter': 'empty',
                'city': 'empty',
                'country': 'DE',
                'zip': 'empty',
                'page': '1'
            }
            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 180 and (float(proxy["price"]) >= 0.6 and float(proxy["price"]) <= 0.75)):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - Germany \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


async def command_proxy_canada(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'America',
                'type_filter': 'ISP',
                'sort': 'speed-desc',
                'area_filter': 'empty',
                'city': 'empty',
                'country': 'CA',
                'zip': 'empty',
                'page': '1'
            }
            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 600 and (
                            float(proxy["price"]) >= 0.6 and float(proxy["price"]) <= 0.75)):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - Canada \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


async def command_proxy_switzerland(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'Europe',
                'type_filter': 'DCH',
                'sort': 'speed-desc',
                'area_filter': 'empty',
                'city': 'empty',
                'country': 'CH',
                'zip': 'empty',
                'page': '1'
            }
            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 180 and (
                            float(proxy["price"]) >= 0.6 and float(proxy["price"]) <= 0.75)):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - Switzerland \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


async def command_proxy_usa(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'USA',
                'type_filter': 'DCH',
                'sort': 'speed-desc',
                'area_filter': 'empty',
                'city': 'empty',
                'country': 'empty',
                'zip': 'empty',
                'page': '1'
            }
            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 600 and (
                            float(proxy["price"]) >= 0.6 and float(proxy["price"]) <= 0.75)):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - USA \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


async def command_proxy_denmark(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'Europe',
                'type_filter': 'DCH',
                'sort': 'speed-desc',
                'area_filter': 'empty',
                'city': 'empty',
                'country': 'DK',
                'zip': 'empty',
                'page': '1'
            }
            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 180 and (
                            float(proxy["price"]) >= 0.6 and float(proxy["price"]) <= 0.75)):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - Denmark \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


async def command_proxy_great_britian(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'Europe',
                'type_filter': 'DCH',
                'sort': 'speed-desc',
                'area_filter': 'empty',
                'city': 'empty',
                'country': 'GB',
                'zip': 'empty',
                'page': '1'
            }
            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 180 and (
                            float(proxy["price"]) >= 0.6 and float(proxy["price"]) <= 0.75)):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - Great Britian \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


async def command_proxy_spain(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'Europe',
                'type_filter': 'DCH',
                'sort': 'speed-desc',
                'area_filter': 'empty',
                'city': 'empty',
                'country': 'ES',
                'zip': 'empty',
                'page': '1'
            }
            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 180 and (
                            float(proxy["price"]) >= 0.6 and float(proxy["price"]) <= 0.75)):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - Spain \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


async def command_proxy_france(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'Europe',
                'type_filter': 'DCH',
                'sort': 'speed-desc',
                'area_filter': 'empty',
                'city': 'empty',
                'country': 'FR',
                'zip': 'empty',
                'page': '1'
            }
            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 180 and (
                            float(proxy["price"]) >= 0.6 and float(proxy["price"]) <= 0.75)):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - France \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


async def command_proxy_belgium(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'Europe',
                'type_filter': 'ISP',
                'sort': 'speed-desc',
                'area_filter': 'empty',
                'city': 'empty',
                'country': 'BE',
                'zip': 'empty',
                'page': '1'
            }
            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 180):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - Belgium \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


async def command_proxy_austria(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'Europe',
                'type_filter': 'ISP',
                'sort': 'speed-desc',
                'area_filter': 'empty',
                'city': 'empty',
                'country': 'AT',
                'zip': 'empty',
                'page': '1'
            }
            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 180 and (
                            float(proxy["price"]) >= 0.6 and float(proxy["price"]) <= 0.75)):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - Austria \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


async def command_proxy_netherlands(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'Europe',
                'type_filter': 'DCH',
                'sort': 'speed-desc',
                'area_filter': 'empty',
                'city': 'empty',
                'country': 'NL',
                'zip': 'empty',
                'page': '1'
            }
            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 180 and (
                            float(proxy["price"]) >= 0.6 and float(proxy["price"]) <= 0.75)):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - Netherlands \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


async def command_proxy_italy(callback: types.CallbackQuery):
    connection = await connect_db(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    account = await connection.fetchrow(
        f"SELECT * FROM approved_users WHERE user_id = {callback.message.chat.id}")

    if account:
        if account["proxy_limit"] > account["proxy_count"]:
            url = 'http://167.172.208.205:7777/api_out/v1/search'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {PROXY_API_KEY}'
            }
            params = {
                'continent': 'Europe',
                'type_filter': 'DCH',
                'sort': 'speed-desc',
                'area_filter': 'empty',
                'city': 'empty',
                'country': 'IT',
                'zip': 'empty',
                'page': '1'
            }
            proxies_response = requests.get(url, headers=headers, params=params)
            if proxies_response.status_code == 200:
                proxies_data = proxies_response.json()
                for proxy in proxies_data:
                    if (proxy["ct"] == proxy["dns_ct"]) and (int(proxy["speed"]) >= 25000) and (
                            int(proxy["ping"]) <= 180 and (
                            float(proxy["price"]) >= 0.6 and float(proxy["price"]) <= 0.75)):
                        url = 'http://167.172.208.205:7777/api_out/v1/rent'
                        headers = {
                            'accept': 'application/json',
                            'Authorization': f'Bearer {PROXY_API_KEY}',  # Замените 'ваш_токен' на ваш реальный токен
                        }
                        params = {
                            'id_proxy': f'{proxy["id"]}'
                        }

                        proxy_rent_response = requests.get(url, headers=headers, params=params)
                        if proxy_rent_response.status_code == 200:
                            ip_address, port = proxy_rent_response.text.replace('\"', "").split(":")
                            await bot.send_message(callback.message.chat.id,
                                                   f"GEO - Italy \n🌐Proxy SOCKS5:\n⚡ IP: {ip_address} \n📍Port: {port} ")
                            await connection.fetch(f"UPDATE approved_users SET proxy_count = proxy_count + 1")
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            await connection.execute(
                                f"INSERT INTO logging_getting_proxy (user_id, ip, port, date) VALUES ({callback.message.chat.id}, 'ip', 5432, '{date}')")
                            await connection.close()
                            return

        else:
            await bot.send_message(callback.message.chat.id, "Ваш лимит прокси закончился!")
            await connection.close()


def register_choice_country_proxy(dp: Dispatcher):
    dp.register_callback_query_handler(command_proxy_australia,
                                       lambda callback_query: callback_query.data == "command_proxy_australia")
    dp.register_callback_query_handler(command_proxy_germany,
                                       lambda callback_query: callback_query.data == "command_proxy_germany")
    dp.register_callback_query_handler(command_proxy_canada,
                                       lambda callback_query: callback_query.data == "command_proxy_canada")
    dp.register_callback_query_handler(command_proxy_switzerland,
                                       lambda callback_query: callback_query.data == "command_proxy_switzerland")
    dp.register_callback_query_handler(command_proxy_usa,
                                       lambda callback_query: callback_query.data == "command_proxy_usa")
    dp.register_callback_query_handler(command_proxy_denmark,
                                       lambda callback_query: callback_query.data == "command_proxy_denmark")
    dp.register_callback_query_handler(command_proxy_great_britian,
                                       lambda callback_query: callback_query.data == "command_proxy_great_britian")
    dp.register_callback_query_handler(command_proxy_spain,
                                       lambda callback_query: callback_query.data == "command_proxy_spain")
    dp.register_callback_query_handler(command_proxy_france,
                                       lambda callback_query: callback_query.data == "command_proxy_france")
    dp.register_callback_query_handler(command_proxy_belgium,
                                       lambda callback_query: callback_query.data == "command_proxy_belgium")
    dp.register_callback_query_handler(command_proxy_austria,
                                       lambda callback_query: callback_query.data == "command_proxy_austria")
    dp.register_callback_query_handler(command_proxy_netherlands,
                                       lambda callback_query: callback_query.data == "command_proxy_netherlands")
    dp.register_callback_query_handler(command_proxy_italy,
                                       lambda callback_query: callback_query.data == "command_proxy_italy")
