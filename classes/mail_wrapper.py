import email

from classes.subject_parser import SubjectParser

class MailWrapper:
    def __init__(self, mail):
        if isinstance(mail, bytes):
            self.mail = email.message_from_bytes(mail)
        elif isinstance(mail, str):
            self.mail = email.message_from_string(mail)

    def get_body_content(self):
        body_message = ''
        for part in self.mail.walk():
            if part.get_content_type() == 'text/plain':
                body_message = part.get_payload(decode=True).decode('utf-8')

        return body_message

    def get_mail(self):
        return self.mail

    def get_sender(self):
        return self.mail['from']

    def get_subject(self):
        subject = SubjectParser(self.mail['subject'])
        return subject.text

