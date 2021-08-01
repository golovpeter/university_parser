from itertools import islice

import requests
from bs4 import BeautifulSoup
from telebot import types

from config import SNILS, SNILS_MIREA, MGSU_NUM

from constants import MIREA_URL_FACULTIES


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
    places, places_with_consent = [], []
    place, dropout_counter, agree_counter, place_with_consent = 0, 0, 0, 0

    for url in url_arr:
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'lxml')
        snils_table = soup.find_all('td', class_='fio')
        status_table = soup.find_all('td', class_='status')
        sum_table = soup.find_all('td', class_='sum')
        sum_table = [sum_table[i].text for i in range(0, len(sum_table), 2)]

        nums = [[snils_table[i].text, sum_table[i], status_table[i].text] for i in range(len(snils_table))]

        for el in nums:
            if 'Согласие на др. конкурсе' in el[2] and int(el[1]) >= 244:
                dropout_counter += 1

            if 'Рассматривается к зачислению' in el[2]:
                agree_counter += 1
                if int(el[1]) < 244 and place_with_consent == 0:
                    place_with_consent = agree_counter

            if el[0] == SNILS_MIREA:
                place = int(nums.index(el))

        places.append(place - dropout_counter)
        places_with_consent.append(place_with_consent)

        place, dropout_counter, agree_counter, place_with_consent = 0, 0, 0, 0

    return places, places_with_consent


def mpei_parser(url_arr):
    places = []
    places_with_consent = ['-', '-', '-', '-', '-', '-']  # Временная затычка для М  ЭИ

    for url in url_arr:
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'lxml')
        parse_table = soup.find_all('tr')
        nums = [el.text for el in parse_table]
        del nums[1], nums[0]

        for i in range(len(nums)):
            if SNILS in nums[i]:
                places.append(int(i))

    return places, places_with_consent


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


def create_string(faculties, budget_places, places, place_with_consent):
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
