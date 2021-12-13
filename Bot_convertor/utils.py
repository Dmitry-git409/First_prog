import requests
import json
import config


class ConvertionExeptions(Exception):
    pass


class RateConverter:
    @staticmethod
    def converts(quote, base, amount):
        if quote.lower() == base.lower():
            raise ConvertionExeptions(f'Конвертируемые валюты одинаковы {quote} и {base}')
        try:
            quote_ticker = config.coin_base[quote.lower()]
        except KeyError:
            raise ConvertionExeptions(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = config.coin_base[base.lower()]
        except KeyError:
            raise ConvertionExeptions(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeptions(f'Не корректная величина {amount}')
        r = requests.get(f'https://freecurrencyapi.net/api/v2/latest?apikey='
                         f'{config.API_KEY}&base_currency={quote_ticker}')
        text = json.loads(r.content)['data'][base_ticker]
        return text
