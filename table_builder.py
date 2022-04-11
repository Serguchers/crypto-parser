import time
import winsound
from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich import box
from runner import main
from utils import check_pair, convert_values, compare_values, send_message


REFRESH_COUNT = 15
NEED_NEW_DATA = False
data = main()
kucoin_previous_price = float(data['USDT_RUB_PAIR']['kucoin']['buy'])

def generate_table() -> Table:
    """Make a new table."""
    global NEED_NEW_DATA
    global REFRESH_COUNT
    global data
    global kucoin_previous_price
    
    REFRESH_COUNT -= 1
    if REFRESH_COUNT == 0:
        NEED_NEW_DATA = True
        REFRESH_COUNT = 15
    if NEED_NEW_DATA:
        data = main()
        NEED_NEW_DATA = False
        

    usdt_rub_data = data['USDT_RUB_PAIR']
    
    table = Table(title=data['headers']['name'], box=box.SQUARE, style=data['headers']['style'])
    table.width = 80    
    
    table.add_column("market")
    table.add_column("buy", justify='center')
    table.add_column("sell", justify='center')

    
    buy_to_check = convert_values('buy', usdt_rub_data)
    if compare_values(buy_to_check[2][1], kucoin_previous_price):
        send_message(buy_to_check[0][1], buy_to_check[2][1])
    kucoin_previous_price = buy_to_check[2][1]
    
    huobi_binance = list(filter(lambda x: x[0] == 'huobi' or x[0] == 'binance', buy_to_check))
    BUY_CALL = False
    if check_pair('buy', huobi_binance):
        BUY_CALL = True

    
    sell_to_check = convert_values('sell', usdt_rub_data)
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

    table.add_row('---', '---', '---')
    table.add_row('time to update', f'{time.ctime()}', f'{REFRESH_COUNT}', style='blue')
    table_centered = Align.center(table)
    return table_centered


with Live(generate_table()) as live:
    while True:
        live.update(generate_table())
        time.sleep(1)