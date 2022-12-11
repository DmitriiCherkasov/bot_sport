from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from get_from_env_function import get_from_env
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import time
import os
import pytz


path = os.path.dirname(os.path.abspath(__file__))
tz = pytz.timezone('Etc/GMT-2')
football_url = "https://www.birebin.com/iddaa-programi-futbol?GroupType=date"


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def time_difference(match_time: str) -> int:
    match_hour, match_minute = map(int, match_time.split(':'))
    current_hour, current_minute = map(int, datetime.now(tz).strftime("%H:%M").split(':'))
    difference = (match_hour * 60 + match_minute) - (current_hour * 60 + current_minute)
    return difference


try:
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    service = Service(path + "/chromedriver.exe")
    browser = webdriver.Chrome(service=service, options=chrome_options)
except Exception as ex:
    print(ex)
    browser.close()
    browser.quit()


bot = Bot(token=get_from_env("TOKEN"))
dp = Dispatcher(bot)


async def on_start(_):
    print('Бот онлайн')


@dp.message_handler(commands=['start'], state=None)
async def greetings(message: types.Message):
    await message.answer(text='Bot is working...')
    try:
        while True:
            browser.get(football_url)
            time.sleep(3)
            list_of_elements = browser.find_elements(By.CLASS_NAME, 'bullettin-event')
            for element in list_of_elements:
                bet = element.text.split()
                match_time = bet[0]
                name = bet[1:-9]
                ust = bet[-4]
                alt = bet[-5]
                if isfloat(ust) and isfloat(alt):
                    full_name = ''
                    for word in name:
                        full_name = full_name + word + ' '
                    # if 1.8 >= float(alt) >= 1.7 and 1.5 >= float(ust) >= 1.4:
                    if 3 >= float(alt) >= 2 and 2 >= float(ust) >= 1:
                        if time_difference(match_time=match_time) <= 2:
                            print(f'{match_time} / {full_name} / alt: {alt} ust: {ust}')
                            print(time_difference(match_time=match_time))
                            await message.answer(text=f'<u>{match_time}</u> \n '
                                                      f'<i>{full_name}</i> \n '
                                                      f'<b>alt: {alt} ust: {ust}</b>', parse_mode="HTML")
                    # elif 1.5 >= float(alt) >= 1.4 and 1.8 >= float(ust) >= 1.7:
                    elif 2 >= float(alt) >= 1 and 3 >= float(ust) >= 2:
                        if time_difference(match_time=match_time) <= 2:
                            print(f'{match_time} / {full_name} / alt: {alt} ust: {ust}')
                            print(time_difference(match_time=match_time))
                            await message.answer(text=f'<u>{match_time}</u> \n '
                                                      f'<i>{full_name}</i> \n '
                                                      f'<b>alt: {alt} ust: {ust}</b>', parse_mode="HTML")
            time.sleep(60)
    except Exception as ex:
        print(ex)
        # browser.close()
        # browser.quit()


executor.start_polling(dp, skip_updates=True, on_startup=on_start)


