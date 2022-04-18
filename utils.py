import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sensetive_data import MY_EMAIL, MY_PASSWORD, TARGET_EMAIL

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

def send_message(binance, kucoin, kucoin_sell, email):
    msg = MIMEMultipart()
    difference_buy = round(float(binance*0.999-kucoin*0.999), 2)
    difference_sell = round(float(kucoin_sell*0.999-binance*0.999), 2)
    try:
        difference_percents_buy = round((float(binance*0.999 / kucoin*0.999) - 1) * 100, 3)
    except ZeroDivisionError:
        raise ZeroDivisionError
    try:
        difference_percents_sell = round((float(kucoin_sell*0.999 / binance*0.999) - 1) * 100, 3)
    except ZeroDivisionError:
        raise ZeroDivisionError
    message = f'K_b: {kucoin}, K_s: {kucoin_sell}, B: {binance} \n P_b: {difference_buy} ({difference_percents_buy}%) P_s: {difference_sell} ({difference_percents_sell}% \n Актуальная информация.'

    password = MY_PASSWORD
    msg['From'] = MY_EMAIL
    msg['To'] = email
    msg['Subject'] = '!!! KUCOIN !!!'

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(msg['From'], password)  
    server.send_message(msg)
    server.quit()
    