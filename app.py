import requests
from flask import Flask

import config

app = Flask(__name__)

# TODO: get the chats id which the bot is inserted in

@app.route("/")

def index():
	return "Nothing to see here, keep moving mate."

@app.route("/<token>")

def verify_token(token):
	if token != config.TOKEN:
		return "Invalid URL"
	else:
		message = 'Shalom Adonai, brothers. New message in the inbox, check it out'
		url = config.urlTelegram + 'sendMessage?chat_id=' + config.chatId + '&text=' + message
		request = requests.post(url)
		return "Message sent, boi"