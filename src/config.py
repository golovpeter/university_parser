import os

import telebot

APP_URL = 'https://university-contest-parser.herokuapp.com/'

TOKEN = '1176140428:AAHBGNoRYcdFKEUhLGg7eO7dYF-6B-8ZaS8'
SNILS_MIREA = os.environ.get('SNILS_MIREA')
SNILS = os.environ.get('SNILS')
MGSU_NUM = os.environ.get('MGSU_NUM')

bot = telebot.TeleBot(TOKEN)
