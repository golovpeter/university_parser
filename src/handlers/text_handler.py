from config import bot
from constants import *
from utils import *


@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.text in UNIVERSITIES:
        handle_university(message)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')


def handle_university(message):
    if message.text == UNIVERSITIES[0]:
        bot.send_message(message.chat.id,
                         create_string(MIREA_FACULTIES, MIREA_BUDGET_PLACES, mirea_parser(MIREA_URL_FACULTIES)))

    if message.text == UNIVERSITIES[1]:
        bot.send_message(message.chat.id,
                         create_string(MPEI_FACULTIES, MPEI_BUDGET_PLACES, mpei_parser(MPEI_URL_FACULTIES)))

    if message.text == UNIVERSITIES[2]:
        bot.send_message(message.chat.id,
                         create_string(MGSU_FACULTIES, MGSU_BUDGET_PLACES, mgsu_parser(MGSU_URL)[0]))
