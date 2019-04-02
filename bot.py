from config import TOKEN
from telegram.ext import Updater, CommandHandler
import logging

updater = Updater(token=TOKEN)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="I'm RobotaBot, hey!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
