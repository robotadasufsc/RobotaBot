import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters

from classes.dollar import Dollar
from classes.datasheets import Datasheets

from exchange import get_quote

def start(bot, update):
    mensagem = "Olá! Sou o RobotaBot.\n\n"
    mensagem += "Por enquanto sou meio limitado e apenas procuro por e-mails novos na nossa conta do gmail, mas tenha paciência comigo, prometo melhorar :')."
    bot.send_message(update.message.chat_id, mensagem)

def exchange(bot, update, args):
    if not args:
        bot.send_message(update.message.chat_id, 'Insira uma moeda para pesquisar a cotação.\n`/cotacao <moeda>`', reply_to_message=update.message.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
        return
    elif len(args) > 1:
	    bot.send_message(update.message.chat_id, 'Insira apenas uma moeda para ser pesquisada.\n`/cotacao <moeda>`', reply_to_message=update.message.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

    value_in_real = get_quote(args[0].upper())
    if not value_in_real:
        bot.send_message(update.message.chat_id, 'Moeda não reconhecida.\n\nVocê pode procurar pelas siglas desejadas aqui: https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html')
        return

    bot.send_message(update.message.chat_id, 'R${:.4f}'.format(value_in_real))

def dollar(bot, update):
    dollar = Dollar()
    if dollar.cotation is not None:
        bot.send_message(update.message.chat_id, 'Cotação: R${}'.format(dollar.cotation))
    else:
        bot.send_message(update.message.chat_id, 'Cotação indisponível no momento.')

def datasheets(bot, update, args):
    if not args:
        bot.send_message(update.message.chat_id, 'Insira um componente para ser pesquisado\n`/datacheetos <componente1> <componente2> ...`', reply_to_message=update.message.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
        return

    components = ' '.join(args)
    message = components + ':\n\n'

    sheets = Datasheets(components)
    for s in sheets.sheets:
        message += '{}\n\n'.format(s)

    bot.send_message(update.message.chat_id, message)

def check_message(bot, update):
    corrected_words = list()

    message = update.message.text.split()
    message_id = update.message.message_id

    for word in message:
        if 'u' in word or 'ú' in word or 'U' in word or 'Ú' in word:
            word = word.replace('u', 'v')
            word = word.replace('ú', 'v')
            word = word.replace('U', 'V')
            word = word.replace('Ú', 'V')
            word = word + '*'
            corrected_words.append(word)

            corrected_string = ', '.join(corrected_words)

    if corrected_words:
        bot.send_message(update.message.chat_id, corrected_string, reply_to_message_id=message_id)

HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('dolar', dollar),
    CommandHandler('datacheetos', datasheets, pass_args=True),
    CommandHandler('datafandangos', datasheets, pass_args=True),
    CommandHandler('databiluzitos', datasheets, pass_args=True),
    CommandHandler('cotacao', exchange, pass_args=True),
    #MessageHandler(Filters.text, check_message),
]
