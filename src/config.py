import os

import telebot

APP_URL = 'https://university-contest-parser.herokuapp.com/'

TOKEN = os.environ.get('BOT_TOKEN')
SNILS_MIREA = os.environ.get('SNILS_MIREA')
SNILS = os.environ.get('SNILS')
MGSU_NUM = os.environ.get('MGSU_NUM')

bot = telebot.TeleBot(TOKEN)
