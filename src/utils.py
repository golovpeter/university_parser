import requests

from telebot import types
from itertools import islice
from bs4 import BeautifulSoup

from config import SNILS, SNILS_MIREA, MGSU_NUM


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


# TODO: убирать людей, которые подали согласие в другой КГ
def mirea_parser(url_arr):
    places = []

    for url in url_arr:
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'lxml')
        parse_table = soup.find_all('td', class_='fio')
        nums = [el.text for el in parse_table]

        if SNILS_MIREA in nums:
            places.append(int(nums.index(SNILS_MIREA)))

    return places


def mpei_parser(url_arr):
    places = []

    for url in url_arr:
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'lxml')
        parse_table = soup.find_all('tr')
        nums = [el.text for el in parse_table]
        del nums[1], nums[0]

        for i in range(len(nums)):
            if SNILS in nums[i]:
                places.append(int(i))

    return places


def mgsu_parser(url):
    mgsu_data = {'n_delo': MGSU_NUM}
    s = requests.Session()
    content = (s.post(url, data=mgsu_data)).text
    soup = BeautifulSoup(content, 'lxml')
    parse_table = soup.find_all('tr')

    nums = [(el.text.replace(' ', '').replace('\r', ' ').
             replace('\n', ' ')).split() for el in parse_table]
    del nums[0:7]
    places, dormitory = [el[3] for el in nums], [el[7] for el in nums]

    return places, dormitory


def create_string(faculties, budget_places, places):
    res_str = ''

    for i in range(len(faculties)):
        inter_str = ''

        if i != len(faculties) - 1:
            inter_str += faculties[i] + '\n' + f'Бюджетных мест: {budget_places[i]}' \
                         + '\n' + f'Место в конкурсном списке: {places[i]}' + '\n' + ' ' + '\n'
        else:
            inter_str += faculties[i] + '\n' + f'Бюджетных мест: {budget_places[i]}' \
                         + '\n' + f'Место в конкурсном списке: {places[i]}' + '\n'
        res_str += inter_str

    return res_str
