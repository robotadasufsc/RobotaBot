import logging
import handler

from config import TOKEN

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_handler = CommandHandler('start', handler.start)
message_handler = MessageHandler(Filters.text, handler.check_message)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()