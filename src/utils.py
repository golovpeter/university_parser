import requests

from telebot import types
from itertools import islice
from bs4 import BeautifulSoup
from config import bot

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


def mpei_parser(url):
    response = requests.get(url).content
    soup = BeautifulSoup(response, 'lxml')
    parse_table = soup.find_all('tr')
    nums = [el.text for el in parse_table]
    del nums[1], nums[0]

    for i in range(len(nums)):
        if SNILS in nums[i]:
            return int(i)


def info_send_message(message, faculties, url_faculties, budgate_places, parse_function):
    url = url_faculties[faculties.index(message.text)]
    budget_places = budgate_places[faculties.index(message.text)]
    place = parse_function(url)

    return bot.send_message(message.chat.id, f'Бюджетных мест: {budget_places} \nМесто в списке: {place}')