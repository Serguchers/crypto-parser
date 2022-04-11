import time
import winsound
from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich import box
from test_data import data as test_data

REFRESH_COUNT = 15
NEED_NEW_DATA = False
data = test_data[0]
counter = 0
kucoin_previous_price = float(data['USDT_RUB_PAIR']['kucoin']['buy'])

def generate_table() -> Table:
    """Make a new table."""
    global NEED_NEW_DATA
    global REFRESH_COUNT
    global data
    global counter
    global kucoin_previous_price
    
    REFRESH_COUNT -= 1
    if REFRESH_COUNT == 0:
        NEED_NEW_DATA = True
        REFRESH_COUNT = 15
        counter += 1
    if NEED_NEW_DATA:
        data = test_data[counter]
        NEED_NEW_DATA = False
        

    usdt_rub_data = data['USDT_RUB_PAIR']
    
    table = Table(title=data['headers']['name'], box=box.SQUARE, style=data['headers']['style'])
    table.width = 80    
    
    table.add_column("market")
    table.add_column("buy", justify='center')
    table.add_column("sell", justify='center')

    
    buy_to_check = convert_values('buy', usdt_rub_data)
    print(buy_to_check[3][1], kucoin_previous_price)
    if compare_values(buy_to_check[3][1], kucoin_previous_price):
        send_message(buy_to_check[0][1], buy_to_check[1][1])
    kucoin_previous_price = buy_to_check[3][1]
    huobi_binance = list(filter(lambda x: x[0] == 'huobi' or x[0] == 'binance', buy_to_check))
    BUY_CALL = False
    if check_pair('buy', huobi_binance):
        BUY_CALL = True

    
    sell_to_check = convert_values('sell', usdt_rub_data)
    #best_sell = max(sell_to_check, key=lambda x: x[1])[0]
    huobi_binance = list(filter(lambda x: x[0] == 'huobi' or x[0] == 'binance', sell_to_check))
    SELL_CALL = False
    if check_pair('sell', huobi_binance):
        SELL_CALL = True


    table.add_row('USDT_RUB_PAIR')

    for key in usdt_rub_data:
        website_name = key
        buy = str(usdt_rub_data[key]['buy'])
        sell = str(usdt_rub_data[key]['sell'])
        if BUY_CALL or SELL_CALL:
            if BUY_CALL and SELL_CALL and website_name == 'huobi':
                style = 'purple'
                winsound.Beep(500, 1000)
                table.add_row(website_name, f'[{style}]{buy}', f'[{style}]{sell}')
                continue
            elif SELL_CALL and website_name == 'huobi':
                style = 'purple'
                winsound.Beep(500, 1000)
                table.add_row(website_name, buy, f'[{style}]{sell}')
                continue
            elif BUY_CALL and website_name == 'huobi':
                style = 'purple'
                winsound.Beep(500, 1000)
                table.add_row(website_name, f'[{style}]{buy}', sell)
                continue

        table.add_row(website_name, buy, sell)
        # else:
        #     if website_name == best_sell:
        #         style = 'red'
        #         table.add_row(website_name, buy, f'[{style}]{sell}')
        #         continue
        #     elif website_name == best_buy:
        #         style = 'green'
        #         table.add_row(website_name, f'[{style}]{buy}', sell)
        #         continue

        #     table.add_row(website_name, buy, sell)
    
    table.add_row('---', '---', '---')
    table.add_row('time to update', '-', f'{REFRESH_COUNT}', style='blue')
    table_centered = Align.center(table)
    return table_centered

def check_pair(action, pair):
    binance = pair[0][1]
    huobi = pair[1][1]
    
    if action == 'buy':
        return huobi < binance
    if action == 'sell':
        binance = binance * 1.01
        return huobi > binance
    
def convert_values(action:str, values):
    converted_values = []
    for i in values:
        try:
            price = float(values[i][action])
        except:
            price = 0
        converted_values.append((i, price))
    return converted_values
    
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def check_pair(action, pair):
    binance = pair[0][1]
    huobi = pair[1][1]
    
    if action == 'buy':
        return huobi < binance
    if action == 'sell':
        binance = binance * 1.01
        return huobi > binance
    
def convert_values(action:str, values):
    converted_values = []
    for i in values:
        try:
            price = float(values[i][action])
        except:
            price = 0
        converted_values.append((i, price))
    return converted_values

def compare_values(current, previous):
    if abs(current - previous) >= 0.1:
        return True
    return False

def send_message(binance, kucoin):
    msg = MIMEMultipart()

    message = f'Текущая цена kucoin: {kucoin} \n Текущая цена binance: {binance} \n Разница: {(binance*0.999-kucoin*0.999)}'

    password = 'rnbbfukzculujsef'
    msg['From'] = 'mycryptonotifier@yandex.ru'
    msg['To'] = 'sergucho.gaming@gmail.com'
    msg['Subject'] = 'Notification'

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(msg['From'], password)  
    server.send_message(msg)
    server.quit()
    
with Live(generate_table()) as live:
    while True:
        live.update(generate_table())
        time.sleep(1)