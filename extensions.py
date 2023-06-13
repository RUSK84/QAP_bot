import json
import requests
from config import keys

#исключения
class ConvertionException(Exception):
    pass

class CryptoConvertor:
    @staticmethod
    def get_price(guote: str, base: str, amount: str):

        if guote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        # проверка на соответствие введенных названий валют с названиями записаными в программе
        try:
            guote_ticker = keys[guote]
        except KeyError:
            raise ConvertionException(f'Валюта внесена не верно {guote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Валюта внесена не верно {base}')

        # проверка на корректность введения колличества валюты (должны быть только цифры)
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Введите колличество цифрами {amount}')

        #если цена за еденицу
        # r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={guote_ticker}&tsyms={base_ticker}')
        # total_base = json.loads(r.content)[keys[base]]
        #цена с учетом колличества
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={guote_ticker}&tsyms={base_ticker}')
        total_base = float(json.loads(r.content)[keys[base]])*amount


        return total_base
