import requests
import json
from tgbot_config import keys

class APIException(Exception):
    pass

class CriptoConvertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException('Невозможно сконвертировать одну и ту же валюту')

        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote} \nСписок доступных для конвертации валют по команде /values')

        try:
            base_tiker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}Список доступных для конвертации валют по команде /values')

        try:
            amount == float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount},проверьте формат значения и ввода')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiker}&tsyms={base_tiker}')
        total_base = json.loads(r.content)[keys[base]] * float(amount)
        return total_base