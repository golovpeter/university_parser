from config import bot
from constants import *
from utils import *


@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.text in UNIVERSITIES:
        handle_university(message)
    elif message.text in MIREA_FACULTIES:
        handle_faculties(message)
    elif message.text == 'Назад':
        handle_return(message)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')


def handle_university(message):
    if message.text == 'РТУ МИРЭА':
        buttons = create_buttons(MIREA_FACULTIES, 1, has_return=True)
        bot.send_message(message.chat.id, 'Выбери факультет', reply_markup=buttons)


def handle_faculties(message):
    if message.text in MIREA_FACULTIES:
        url = MIREA_URL_FACULTIES[MIREA_FACULTIES.index(message.text)]
        budget_places = MIREA_BUDGET_PLACES[MIREA_FACULTIES.index(message.text)]
        place = mirea_parser(url)
        bot.send_message(message.chat.id, f'Бюджетных мест: {budget_places} \nМесто в списке: {place}')


def handle_return(message):
    buttons = create_buttons(UNIVERSITIES, 3, has_return=False)
    bot.send_message(message.chat.id, 'Выбери ВУЗ', reply_markup=buttons)
