import os

import telebot

TOKEN = os.environ.get('BOT_TOKEN', '1176140428:AAHBGNoRYcdFKEUhLGg7eO7dYF-6B-8ZaS8')
APP_URL = 'https://university-contest-parser.herokuapp.com/'
SNILS_MIREA = os.environ.get('SNILS_MIREA')
SNILS = os.environ.get('SNILS')

bot = telebot.TeleBot(TOKEN)
