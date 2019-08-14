import logging
from handler import HANDLERS

from config import TOKEN

from telegram.ext import Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(TOKEN)

for h in HANDLERS:
    updater.dispatcher.add_handler(h)

updater.start_polling()