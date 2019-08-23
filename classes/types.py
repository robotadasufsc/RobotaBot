from typing import NamedTuple

class ComponentDatasheet(NamedTuple):
    name: str
    link: str

class MailSenderSubject(NamedTuple):
    sender: str
    subject: str