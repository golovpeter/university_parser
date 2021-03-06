import requests

from itertools import islice
from bs4 import BeautifulSoup
from telebot import types

from constants import MIREA_URL_FACULTIES, MPEI_URL_FACULTIES, MGSU_URL
from config import SNILS, SNILS_MIREA, MGSU_NUM
from cache import *


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

        mirea_places.append(place - dropout_counter)
        mirea_places_with_consent.append(place_with_consent)

        place, dropout_counter, agree_counter, place_with_consent = 0, 0, 0, 0


def mpei_parser(url_arr):
    dropout_counter = 0
    snils_found = False

    for url in url_arr:
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'lxml')
        parse_table = soup.find_all('tr')
        nums = [el.text for el in parse_table]
        del nums[1], nums[0]

        for i in range(len(nums)):
            if 'Согласие в другой КГ' in nums[i] and snils_found != False:
                dropout_counter += 1

            if SNILS in nums[i]:
                snils_found = True
                mpei_places.append(int(i - 1) - dropout_counter)

        dropout_counter = 0


def mgsu_parser(url):
    mgsu_data = {'n_delo': MGSU_NUM}
    s = requests.Session()
    content = (s.post(url, data=mgsu_data)).text
    soup = BeautifulSoup(content, 'lxml')
    parse_table = soup.find_all('tr')

    nums = [(el.text.replace(' ', '').replace('\r', ' ').
             replace('\n', ' ')).split() for el in parse_table]
    del nums[0:7]

    [mgsu_places.append(el[3]) for el in nums]
    [mgsu_places_with_consent.append(el[4]) for el in nums]


def clear_cache():
    mirea_places.clear()
    mirea_places_with_consent.clear()
    mpei_places.clear()
    mgsu_places.clear()
    mgsu_places_with_consent.clear()


def parser():
    clear_cache()
    mirea_parser(MIREA_URL_FACULTIES)
    mpei_parser(MPEI_URL_FACULTIES)
    mgsu_parser(MGSU_URL)


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
