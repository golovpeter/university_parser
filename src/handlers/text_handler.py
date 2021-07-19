from tabulate import tabulate

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
        table = split_arrays(MIREA_FACULTIES, MIREA_BUDGET_PLACES, mirea_parser(MIREA_URL_FACULTIES))
        bot.send_message(message.chat.id, '`' + tabulate(table, HEADER_TABLE, tablefmt="fancy_grid") + '`',
                         parse_mode='Markdown')

    if message.text == 'МЭИ':
        table = split_arrays(MPEI_FACULTIES, MPEI_BUDGET_PLACES, mpei_parser(MPEI_URL_FACULTIES))
        bot.send_message(message.chat.id, '`' + tabulate(table, HEADER_TABLE, tablefmt="fancy_grid") + '`',
                         parse_mode='Markdown')
