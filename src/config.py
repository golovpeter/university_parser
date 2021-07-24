import os

import telebot

# TOKEN = os.environ.get('BOT_TOKEN')
TOKEN = "1887025124:AAGvIxRPEmIrsSVjRHuNxilDYKFL3w0gQLg"
APP_URL = 'https://university-contest-parser.herokuapp.com/'
SNILS_MIREA = os.environ.get('SNILS_MIREA')
SNILS = os.environ.get('SNILS')

bot = telebot.TeleBot(TOKEN)
