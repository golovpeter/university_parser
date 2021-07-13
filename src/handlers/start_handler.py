from telebot import types

from config import bot
from utils import create_buttons
from constants import UNIVERSITIES


@bot.message_handler(commands=['start'])
def start(message):
    buttons = create_buttons(UNIVERSITIES, 3, has_return=False)

    bot.send_message(message.chat.id, 'Выбери ВУЗ', reply_markup=buttons)
