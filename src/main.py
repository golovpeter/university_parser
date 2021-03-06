import logging
import os
import time
import telebot

from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler

from config import bot, TOKEN, APP_URL
from utils import parser

import handlers.start_handler
import handlers.text_handler

server = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(func=parser, trigger="interval", seconds=3600)
scheduler.start()


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/", methods=['GET'])
def web_hook():
    bot.remove_webhook()

    # Pause between telegram api operations
    time.sleep(1)

    bot.set_webhook(url=APP_URL + TOKEN)
    return "!", 200


if __name__ == '__main__':
    if "HEROKU" in list(os.environ.keys()):
        # Heroku start
        logger = telebot.logger
        telebot.logger.setLevel(logging.INFO)

        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    else:
        # Local start
        bot.polling(none_stop=True, interval=0)
