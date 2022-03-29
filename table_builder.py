import time

from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich import box
from runner import main
import winsound

def generate_table() -> Table:
    """Make a new table."""
    data = main()
    usdt_rub_data = data['USDT_RUB_PAIR']
    
    table = Table(title=data['headers']['name'], box=box.SQUARE, style=data['headers']['style'])
    table.width = 80    
    
    table.add_column("market")
    table.add_column("buy", justify='center')
    table.add_column("sell", justify='center')

    
    buy_to_check = convert_values('buy', usdt_rub_data)
    #best_buy = min(buy_to_check, key=lambda x: x[1])[0]
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
    

with Live(generate_table(), refresh_per_second=1) as live:
    while True:
        time.sleep(15)
        live.update(generate_table())