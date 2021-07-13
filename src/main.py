from config import bot

import handlers.start_handler
import handlers.text_handler

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
