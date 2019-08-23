import requests

base_coin = 'BRL'

def get_quote(coin):
    r = requests.get('https://api.exchangeratesapi.io/latest?base=' + base_coin)
    exchange_values = r.json()['rates']

    if coin not in exchange_values:
        return False

    return 1 / exchange_values[coin]
