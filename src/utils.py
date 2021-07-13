import requests

from telebot import types
from itertools import islice
from bs4 import BeautifulSoup

from constants import *


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def create_buttons(arr, chunk_length, has_return=False):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    divided_objects = chunk(arr, chunk_length)

    for objects in divided_objects:
        keyboard.row(*list(objects))

    if has_return:
        keyboard.row('Назад')

    return keyboard


def mirea_parser(url):
    response = requests.get(url).content
    soup = BeautifulSoup(response, 'lxml')
    parse_table = soup.find_all('td', class_='fio')
    nums = [el.text for el in parse_table]

    if SNILS_MIREA in nums:
        return int(nums.index(SNILS_MIREA))
