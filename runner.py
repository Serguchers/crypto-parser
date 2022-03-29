from pprint import pprint
import requests

USDT_RUB_PAIR = {}
USD_RUB_PAIR = {}
USDT_USD_PAIR = {}
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36'}
HEADERS_HUOBI = {
    
}


def get_data(resource=None):

    if resource == 'binance':
        try:
            request = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=USDTRUB', headers=HEADERS)
        except requests.exceptions.ConnectionError:
            return None

        data = request.json()
        
        USDT_RUB_PAIR['binance'] = {}
        USDT_RUB_PAIR['binance']['buy'] = data.setdefault('price', 0)
        USDT_RUB_PAIR['binance']['sell'] = data.setdefault('price', 0)
        
        return True

    if resource == 'exmpo':
        data = requests.get('https://api.exmo.com/v1.1/ticker', headers=HEADERS).json()
        
        try:
            USDT_RUB_PAIR['exmpo'] = {'buy': data['USDT_RUB']['sell_price'],
                                      'sell': data['USDT_RUB']['buy_price']}

            USD_RUB_PAIR['exmpo'] = {'buy': data['USD_RUB']['sell_price'],
                                     'sell': data['USD_RUB']['buy_price']}

            USDT_USD_PAIR['exmpo'] = {'buy': data['USDT_USD']['sell_price'],
                                      'sell': data['USDT_USD']['buy_price']}
        except:
            USDT_RUB_PAIR['exmpo'] = {'buy': 0, 'sell': 0}
            USD_RUB_PAIR['exmpo'] = {'buy': 0, 'sell': 0}
            USDT_USD_PAIR['exmpo'] = {'buy': 0, 'sell': 0}

    if resource == 'f2c':
        try:
            request = requests.get('https://api.aax.com/common/v2/market/rfqPrice?base=USDT&quote=RUB', headers=HEADERS)
        except requests.exceptions.ConnectionError:
            return None
            
        data = request.json()

        try:
            USDT_RUB_PAIR['AAX'] = {'buy': data['data']['prices'][0]['buy'],
                                    'sell': data['data']['prices'][0]['sell']}
        except:
            USDT_RUB_PAIR['AAX'] = {'buy': 0, 'sell': 0}
        
        return True

    if resource == 'kucoin':
        data = requests.get('https://www.kucoin.com/_api/dispatch/v1/quotes?fiatCurrency=RUB&cryptoCurrency=USDT&amount=100&quoteType=CRYPTO&source=WEB&side=BUY&platform=KUCOIN&lang=en_US', headers=HEADERS).json()
        data_sell = requests.get('https://www.kucoin.com/_api/dispatch/v1/quotes?fiatCurrency=RUB&cryptoCurrency=USDT&amount=100&quoteType=CRYPTO&source=WEB&side=SELL&platform=KUCOIN&lang=en_US',
                                 headers=HEADERS).json()
        
        try:
            USDT_RUB_PAIR['kucoin_qiwi'] = {'buy': data['data']['quotes'][1]['price'],
                                            'sell': data_sell['data']['quotes'][1]['price']}
            USDT_RUB_PAIR['kucoin_payeer'] = {'buy': data['data']['quotes'][4]['price'],
                                              'sell': data_sell['data']['quotes'][4]['price']}
            USDT_RUB_PAIR['kucoin_ADVcash'] = {'buy': data['data']['quotes'][5]['price'],
                                               'sell': data_sell['data']['quotes'][5]['price']}
        except:
            USDT_RUB_PAIR['kucoin_qiwi'] = {'buy': 0, 'sell': 0}
            USDT_RUB_PAIR['kucoin_payeer'] = {'buy': 0, 'sell': 0}
            USDT_RUB_PAIR['kucoin_ADVcash'] = {'buy': 0, 'sell': 0}

    if resource == 'yobit':
        data = requests.get('https://yobit.net/api/3/ticker/usd_rur-usdt_rur-usdt_usd', headers=HEADERS).json()
        
        try:
            USDT_RUB_PAIR['yobit'] = {'buy': data['usdt_rur']['sell'],
                                      'sell': data['usdt_rur']['buy']}

            USD_RUB_PAIR['yobit'] = {'buy': data['usd_rur']['sell'],
                                     'sell': data['usd_rur']['buy']}

            USDT_USD_PAIR['yobit'] = {'buy': data['usdt_usd']['sell'],
                                      'sell': data['usdt_usd']['buy']}
        except:
            USDT_RUB_PAIR['yobit'] = {'buy': 0, 'sell': 0}
            USD_RUB_PAIR['yobit'] = {'buy': 0, 'sell': 0}
            USDT_USD_PAIR['yobit'] = {'buy': 0, 'sell': 0}

    if resource == 'huobi':
        try:
            request_buy = requests.get('https://otc-api.bitderiv.com/v1/trade/fast/quote?quoteAsset=rub&cryptoAsset=usdt&side=buy&amount=100&type=quantity&areaType=1&p2pPayment=1&acceptOrder=0',
                                headers=HEADERS_HUOBI)
            request_sell = requests.get('https://otc-api.trygofast.com/v1/trade/fast/quote?quoteAsset=rub&cryptoAsset=usdt&side=sell&amount=1000&type=quantity&areaType=1&p2pPayment=1&acceptOrder=0',
                                    headers=HEADERS_HUOBI)
        except requests.exceptions.ConnectionError:
            return None
        data = request_buy.json()
        data_sell = request_sell.json()
        
        try:
            USDT_RUB_PAIR['huobi'] = {'buy': data['data'][0]['quoteDetail'][0]['price'],
                                      'sell': data_sell['data'][0]['quoteDetail'][0]['price']}
        except:
            USDT_RUB_PAIR['huobi'] = {'buy': 0, 'sell': 0}
            
        return True


def main():
    binance = get_data('binance')
    huobi = get_data('huobi')
    AAX = get_data('f2c')
    if binance is None or huobi is None or AAX is None:
        return {'USD_RUB_PAIR': USD_RUB_PAIR, 'USDT_RUB_PAIR': USDT_RUB_PAIR, 'USDT_USD_PAIR': USDT_USD_PAIR,
                'headers': {'name': 'LOST CONNECTION', 'style': 'red'}}


    return {'USD_RUB_PAIR': USD_RUB_PAIR, 'USDT_RUB_PAIR': USDT_RUB_PAIR, 'USDT_USD_PAIR': USDT_USD_PAIR,
            'headers': {'name': 'Exchange rates', 'style': 'white'}}


if __name__ == '__main__':
    result = main()

    pprint(result['USDT_RUB_PAIR'])
