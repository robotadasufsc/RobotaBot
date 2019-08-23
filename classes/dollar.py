import requests
from requests.exceptions import HTTPError

from bs4 import BeautifulSoup

class Dollar:
    def __init__(self):
        self.url = 'http://www.dolarhoje.net.br/'

        self.cotation = self.get_cotation()

    def get_cotation(self):
        try:
            res = requests.get(self.url)
            res.raise_for_status()
        except HTTPError as err:
            print('HTTP error {}'.format(err))
            return
        except Exception as err:
            print('Another error {}'.format(err))
            return

        soup = BeautifulSoup(res.text, 'html.parser')
        tag = soup.findAll('input', {'id' : 'moeda'})

        if tag is None:
            return
        return tag[0]['value'].replace(',' , '.')
