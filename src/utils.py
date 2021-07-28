from itertools import islice

import requests
from bs4 import BeautifulSoup
from telebot import types

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


def mirea_parser(url_arr):
    places, agree_places = [], []
    dropout_counter, agree_counter, place = 0, 0, 0

    for url in url_arr:
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'lxml')
        snils_table = soup.find_all('td', class_='fio')
        status_table = soup.find_all('td', class_='status')

        nums = [[snils_table[i].text, status_table[i].text] for i in range(len(snils_table))]

        for el in nums:
            if 'Согласие на др. конкурсе' in el[1]:
                dropout_counter += 1
            if 'Рассматривается к зачислению' in el[1]:
                agree_counter += 1
            if el[0] == SNILS_MIREA:
                place = int(nums.index(el))

        places.append(place - dropout_counter)
        agree_places.append(agree_counter)

        place, dropout_counter, agree_counter = 0, 0, 0

    return places, agree_places


def mpei_parser(url_arr):
    places = []
    agree_places = ['-', '-', '-', '-', '-', '-', ]  # Временная затычка для МЭИ

    for url in url_arr:
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'lxml')
        parse_table = soup.find_all('tr')
        nums = [el.text for el in parse_table]
        del nums[1], nums[0]

        for i in range(len(nums)):
            if SNILS in nums[i]:
                places.append(int(i))

    return places, agree_places


def mgsu_parser(url):
    mgsu_data = {'n_delo': MGSU_NUM}
    s = requests.Session()
    content = (s.post(url, data=mgsu_data)).text
    soup = BeautifulSoup(content, 'lxml')
    parse_table = soup.find_all('tr')

    nums = [(el.text.replace(' ', '').replace('\r', ' ').
             replace('\n', ' ')).split() for el in parse_table]
    del nums[0:7]
    places = [el[3] for el in nums]
    places_with_consent = [el[4] for el in nums]

    return places, places_with_consent


def create_string(faculties, budget_places, places, agree_places):
    res_str = ''

    for i in range(len(faculties)):
        inter_str = ''

        if i != len(faculties) - 1:
            inter_str += faculties[i] + '\n' + f'Бюджетных мест: {budget_places[i]}' + '\n' \
                         + f'Место в конкурсном списке: {places[i]}' + '\n' \
                         + f'Согласий подано: {agree_places[i]}' + '\n' + ' ' + '\n'
        else:
            inter_str += faculties[i] + '\n' + f'Бюджетных мест: {budget_places[i]}' + '\n' \
                         + f'Место в конкурсном списке: {places[i]}' + '\n' \
                         + f'Согласий подано: {agree_places[i]}' + '\n'

        res_str += inter_str

    return res_str


def mgsu_create_string(faculties, budget_places, places, place_with_consent):
    res_str = ''

    for i in range(len(faculties)):
        inter_str = ''

        if i != len(faculties) - 1:
            inter_str += faculties[i] + '\n' + f'Бюджетных мест: {budget_places[i]}' + '\n' \
                         + f'Место в конкурсном списке: {places[i]}' + '\n' \
                         + f'Место с учётом согласий: {place_with_consent[i]}' + '\n' + ' ' + '\n'
        else:
            inter_str += faculties[i] + '\n' + f'Бюджетных мест: {budget_places[i]}' + '\n' \
                         + f'Место в конкурсном списке: {places[i]}' + '\n' \
                         + f'Место с учётом согласий: {place_with_consent[i]}' + '\n'

        res_str += inter_str

    return res_str
