from config import bot
from constants import *
from utils import *


@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.text in UNIVERSITIES:
        handle_university(message)
    elif message.text in MIREA_FACULTIES or message.text in MPEI_FACULTIES:
        handle_faculties(message)
    elif message.text == 'Назад':
        handle_return(message)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')


def handle_university(message):
    if message.text == 'РТУ МИРЭА':
        buttons = create_buttons(MIREA_FACULTIES, 1, has_return=True)
        bot.send_message(message.chat.id, 'Выбери факультет', reply_markup=buttons)

    if message.text == 'МЭИ':
        buttons = create_buttons(MPEI_FACULTIES, 1, has_return=True)
        bot.send_message(message.chat.id, 'Выбери факультет', reply_markup=buttons)


def handle_faculties(message):
    if message.text in MIREA_FACULTIES:
        info_send_message(message, MIREA_FACULTIES, MIREA_URL_FACULTIES, MIREA_BUDGET_PLACES, mirea_parser)

    if message.text in MPEI_FACULTIES:
        info_send_message(message, MPEI_FACULTIES, MPEI_URL_FACULTIES, MPEI_BUDGET_PLACES, mpei_parser)


def handle_return(message):
    buttons = create_buttons(UNIVERSITIES, 3, has_return=False)
    bot.send_message(message.chat.id, 'Выбери ВУЗ', reply_markup=buttons)
