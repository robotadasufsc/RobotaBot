import re

class SubjectParser:
    def __init__(self, subject):
        if self.is_dirty(subject):
            self.subject = subject
            self.text = self.clean_subject()
        else:
            self.text = subject

    def clean_subject(self):
        self.clean_edges()
        self.clean_underlines()
        self.trade_utf8_enconding()

        return self.subject
    
    def clean_edges(self):
        self.subject = self.subject.replace('=?UTF-8?Q?', '')
        self.subject = self.subject.replace('?=', '')

    def clean_underlines(self):
        self.subject = self.subject.replace('_', ' ')

    def trade_utf8_enconding(self):
        self.trade_two_hex_codes()
        self.trade_one_hex_codes()
    
    def trade_two_hex_codes(self):
        two_hex_matches = re.findall(r'\=\w{2}\=\w{2}', self.subject)
        
        for two_hex_code in two_hex_matches:
            hex_codes = self.trade_equals_for_0x(two_hex_code)
            byte_array_hex_codes = self.trade_hex_codes_to_bytearray(hex_codes)
            utf8_letter = str(byte_array_hex_codes, 'utf-8')

            self.subject = self.subject.replace(two_hex_code, utf8_letter)

    def trade_one_hex_codes(self):
        one_hex_matches = re.findall(r'\=\w{2}', self.subject)

        for one_hex_code in one_hex_matches:
            hex_code = self.trade_equals_for_0x(one_hex_code)
            byte_array_hex_code = self.trade_hex_codes_to_bytearray(hex_code)
            utf8_letter = str(byte_array_hex_code, 'utf8')

            self.subject = self.subject.replace(one_hex_code, utf8_letter)

    @staticmethod
    def trade_equals_for_0x(two_hex_codes):
        m = re.findall(r'\=\w{2}', two_hex_codes)
        return [x.replace('=', '0x') for x in m]

    @staticmethod
    def trade_hex_codes_to_bytearray(hex_codes):
        return bytes(int(x, 0) for x in hex_codes)

    @staticmethod
    def is_dirty(subject):
        return '=?UTF-8?Q?' in subject

s = input()

o = SubjectParser(s)
print(o.text)