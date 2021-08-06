from config import bot
from constants import *
from utils import *
from cache import *


@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.text in UNIVERSITIES:
        handle_university(message)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')


def handle_university(message):
    if message.text == UNIVERSITIES[0]:
        if len(mirea_places) == 0:
            bot.send_message(message.chat.id, 'Обновляется')
        else:
            bot.send_message(message.chat.id,
                             create_string(MIREA_FACULTIES, MIREA_BUDGET_PLACES, mirea_places, mirea_places_with_consent))

    if message.text == UNIVERSITIES[1]:
        if len(mpei_places) == 0:
            bot.send_message(message.chat.id, 'Обновляется')
        else:
            bot.send_message(message.chat.id,
                             create_string(MPEI_FACULTIES, MPEI_BUDGET_PLACES, mpei_places, mpei_places_with_consent))

    if message.text == UNIVERSITIES[2]:
        if len(mgsu_places) == 0:
            bot.send_message(message.chat.id, 'Обновляется')
        else:
            bot.send_message(message.chat.id,
                             create_string(MGSU_FACULTIES, MGSU_BUDGET_PLACES, mgsu_places, mgsu_places_with_consent))
