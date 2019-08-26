import os
import requests

from classes.mail_wrapper import MailWrapper
from classes.imap import ImapGmailWrapper
from classes.types import MailSenderSubject

from config import mail, app_password, url_telegram, chat_id

def check_gmail():

    imap = ImapGmailWrapper(mail, app_password)
    imap.select_mail_box('inbox')
    new_email_id = int(imap.get_last_email_id('UNSEEN'))

    if not os.path.exists('recent_mail.txt'):
        save_latest_email_id(new_email_id)
        return

    file_reader = open('recent_mail.txt', 'r')
    if file_reader.readable():
        current_mail_id = int(file_reader.read())
        file_reader.close()

        if new_email_id > current_mail_id:
            save_latest_email_id(new_email_id)

            senders_subjects = []
            message = 'Shalom Adonai, irmãos. Novo(s) e-mail(s), deem uma olhada:\n'

            for mail_id in range(current_mail_id + 1, new_email_id + 1):
                raw_email = imap.fetchs([mail_id])

                mail_parser = MailWrapper(raw_email)

                senders_subjects.append(MailSenderSubject(mail_parser.get_sender(), mail_parser.get_subject()))

            for sender_subject in senders_subjects:
                message += '\nRemetente: {}\nTítulo: {}\n'.format(sender_subject.sender, sender_subject.subject)

            send_message(message)

def save_latest_email_id(new_email_id):
    file_writer = open('recent_mail.txt', 'w')
    file_writer.write(str(new_email_id))
    file_writer.close()

def send_message(message):
    url = url_telegram + 'sendMessage?chat_id=' + chat_id + '&text=' + message
    requests.post(url)

check_gmail()
