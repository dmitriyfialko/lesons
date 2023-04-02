import platform
import asyncio
import logging
from sys import argv
from datetime import datetime, timedelta
from pprint import pprint

import aiohttp


async def requests(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logging.error(f'Error status {response.status} for {url}')
        except aiohttp.ClientConnectorError as err:
            logging.error(f'Connection Error: {err}')
        except aiohttp.ContentTypeError as err:
            logging.error(f'Content Type Error: {err}')
    return None


async def get_date_list(days) -> list:
    ls = []
    tm = datetime.now()
    while days > 0:
        ls.append(f'{tm.day:02}.{tm.month:02}.{tm.year}')
        tm = tm - timedelta(days=1)
        days -= 1
    return ls


async def parsing(response: tuple, date: str):
    for day in response:
        if day and day.get('date') == date:
            return {
                date: {
                    v['currency']: {'sale': v['saleRate'], 'purchase': v['purchaseRate']}
                    for v in day['exchangeRate'] if v['currency'] in ['USD', 'EUR']
                }
            }
    return {date: 'Error'}


async def get_exchange(days):
    url = 'https://api.privatbank.ua/p24api/exchange_rates'
    date_list = await get_date_list(days)
    requests_list = [requests(f'{url}?date={date}') for date in date_list]
    exchange = await asyncio.gather(*requests_list)

    lst = [parsing(exchange, day) for day in date_list]
    result = await asyncio.gather(*lst)

    return result


async def start():
    try:
        n = int(argv[1])
        if not 0 < n <= 10:
            raise ValueError
    except (IndexError, ValueError):
        logging.error('Incorrect number of days. Specify from 1 to 10')
        return None
    exchange = await get_exchange(n)
    return exchange


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    if r := asyncio.run(start()):
        pprint(r)

