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

def send_message(binance, kucoin):
    msg = MIMEMultipart()
    difference = round(float(binance*0.999-kucoin*0.999), 2)
    difference_percents = round((float(binance*0.999 / kucoin*0.999) - 1) * 100, 3)
    message = f'Текущая цена kucoin: {kucoin} \n Текущая цена binance: {binance} \n Разница: {difference} ({difference_percents}%)'

    password = MY_PASSWORD
    msg['From'] = MY_EMAIL
    msg['To'] = TARGET_EMAIL
    msg['Subject'] = '!!! KUCOIN !!!'

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(msg['From'], password)  
    server.send_message(msg)
    server.quit()
    