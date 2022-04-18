from email import header
import logging
import time
from asyncio.log import logger
from pprint import pprint

import requests

import email_log
from utils import compare_values, convert_values, send_message

USDT_RUB_PAIR = {}
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36'
}
email_logger = logging.getLogger('email_logger')

def get_data(resource=None):

    if resource == 'binance':
        try:
            request = requests.get(
                'https://api.binance.com/api/v3/ticker/price?symbol=USDTRUB', headers=HEADERS)
        except requests.exceptions.ConnectionError:
            return None

        data = request.json()

        USDT_RUB_PAIR['binance'] = {}
        USDT_RUB_PAIR['binance']['buy'] = data.setdefault('price', 0)
        USDT_RUB_PAIR['binance']['sell'] = data.setdefault('price', 0)

        return True

    if resource == 'kucoin':
        try:
            request = requests.get(
                'https://www.kucoin.com/_api/dispatch/v1/quotes?fiatCurrency=RUB&cryptoCurrency=USDT&quoteType=CRYPTO&source=WEB&side=BUY&platform=KUCOIN&lang=en_US', headers=HEADERS)
            request_sell = requests.get(
                'https://www.kucoin.com/_api/dispatch/v1/quotes?fiatCurrency=RUB&cryptoCurrency=USDT&quoteType=CRYPTO&source=WEB&side=SELL&platform=KUCOIN&lang=en_US', headers=HEADERS)
        except requests.exceptions.ConnectionError:
            return None
        data = request.json()
        data_sell = request_sell.json()

        try:
            USDT_RUB_PAIR['kucoin'] = {'buy': data['data']['quotes'][0]['price'],
                                       'sell':  data_sell['data']['quotes'][0]['price']}

        except:
            USDT_RUB_PAIR['kucoin'] = {'buy': 0, 'sell': 0}
        return True


def main():
    first_run = True
    message_sent = time.time()
    while True:
        binance = get_data('binance')
        kucoin = get_data('kucoin')

        if binance is None or kucoin is None:
            email_logger.critical('REQUEST FAILED')
            time.sleep(15)
            continue

        converted_to_float = convert_values('buy', USDT_RUB_PAIR)
        converted_to_float_sell = convert_values('sell', USDT_RUB_PAIR)
        print(converted_to_float)
        print(converted_to_float_sell)
        if first_run:
            kucoin_previous_value = converted_to_float[1][1]
            kucoin_previous_value_sell = converted_to_float_sell[1][1]
            first_run = False

        if compare_values(converted_to_float[1][1], kucoin_previous_value) or \
            compare_values(converted_to_float_sell[1][1], kucoin_previous_value_sell):
                current_time = time.time()
                if current_time - message_sent > 60:
                    send_message(converted_to_float[0][1], converted_to_float[1][1], converted_to_float_sell[1][1], 'bare.brann@yandex.ru')
                    send_message(converted_to_float[0][1], converted_to_float[1][1], converted_to_float_sell[1][1], 'Info@dashewski.ru')
                    email_logger.debug('MESSAGE SENT')
                    message_sent = time.time()

        kucoin_previous_value = converted_to_float[1][1]
        kucoin_previous_value_sell = converted_to_float_sell[1][1]
        email_logger.debug(f'SUCCESS {USDT_RUB_PAIR}')
        time.sleep(15)


if __name__ == '__main__':
    main()
