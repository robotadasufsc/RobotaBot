from config import mail, app_password

from imaplib import IMAP4_SSL

from classes.email import MailWrapper

class ImapGmailWrapper:

	def __init__ (self, mail, app_password):
		self.imap = IMAP4_SSL(host='imap.gmail.com', port=993)
		self.imap.login(mail, app_password)

	def select_mail_box(self, mail_box, read_only=True):
		self.imap.select(mail_box, read_only)

	def get_last_email_content(self, search_criteria):
		last_id = self.get_last_email_id(search_criteria)
		raw_email = self.fetchs([last_id])
		mail_parser = MailWrapper(raw_email)
		clean_mail = mail_parser.get_body_content()

		return clean_mail

	def get_last_email_id(self, search_criteria):
		emails_id = self.search(search_criteria)

		return int(emails_id[-1])

	def search(self, criteria, charset=None):
		try:
			_, mails_id = self.imap.search(charset, '(' + criteria + ')')
		except:
			print('bleh')

		return mails_id[0].split()

	def fetchs(self, mail_ids, mail_part='RFC822'):
		fetched_list = list()
		for mail_id in mail_ids:
			fetched = self.single_fetch(mail_id, mail_part)
			fetched_list.append(fetched)

		if len(fetched_list) == 1:
			fetched_list = fetched_list[0]

		return fetched_list

	def single_fetch(self, mail_id, mail_part='RFC822'):
		mail_id = str(mail_id)

		if self.is_full_email(mail_part):
			raw_fetch = self._fetch(mail_id, mail_part)
			fetched = self.format_fetched_RFC822_mail(raw_fetch)
		else:
			fetched = self._fetch(mail_id, mail_part)

		return fetched

	def _fetch(self, mail_id, mail_part='RFC822'):
		try:
			fetched = self.imap.fetch(mail_id, '(' + mail_part + ')')
		except:
			print('bleh, something went wrong')

		return fetched

	def format_fetched_RFC822_mail(self, raw_fetch):
		_, (clean_fetch, *_) = raw_fetch
		clean_fetch = clean_fetch[1]

		return clean_fetch
		 
	@staticmethod
	def is_full_email(criteria):
		return criteria == 'RFC822' or criteria == 'BODY[]'