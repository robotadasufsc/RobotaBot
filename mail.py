import requests

from classes.email import MailWrapper
from classes.imap import ImapGmailWrapper

import config

def check_gmail():

    imap = ImapGmailWrapper(config.mail, config.app_password)
    imap.select_mail_box('inbox')
    possible_new_email_id = int(imap.get_last_email_id('UNSEEN'))

    file_reader = open('recent_mail.txt', 'r')
    if file_reader.readable():
        current_mail_id = int(file_reader.read())
        print('current: {}'.format(current_mail_id))
        print('possbile: {}'.format(possible_new_email_id))

        if possible_new_email_id > current_mail_id:
            latest_email_id = possible_new_email_id
            number_of_new_mails = latest_email_id - current_mail_id

            file_reader.close()

            save_latest_email_id(latest_email_id)

            raw_email = imap.fetchs([latest_email_id])

            mail_parser = MailWrapper(raw_email)
            sender = mail_parser.get_sender()

            if number_of_new_mails > 1:
                message = 'Shalom Adonai, irmãos. {} novo(s) email(s), deem uma olhada.'.format(number_of_new_mails) 
            else:
                message = 'Shalom Adonai, irmãos. Novo email, deem uma olhada.\n\nRemetente: {}'.format(number_of_new_mails, sender) 

            send_message(message)

def save_latest_email_id(latest_email_id):
    file_writer = open('recent_mail.txt', 'w')
    file_writer.write(str(latest_email_id))
    file_writer.close()

def send_message(message):
    url = config.url_telegram + 'sendMessage?chat_id=' + config.chat_id + '&text=' + message
    request = requests.post(url)

check_gmail()