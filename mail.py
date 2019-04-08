import email
from classes.email import MailWrapper

from config import mail, app_password

from imaplib import IMAP4_SSL
from classes.imap import ImapGmailWrapper

imap = ImapGmailWrapper(mail, app_password)

imap.select_mail_box('inbox')

mails_id = imap.search('UNSEEN')

latest_email_id = int(mails_id[-1])

raw_email = imap.fetchs([latest_email_id])

mail_parser = MailWrapper(raw_email)

email = mail_parser.get_body_content()
sender = mail_parser.get_sender()
subject = mail_parser.get_subject()

print(email)