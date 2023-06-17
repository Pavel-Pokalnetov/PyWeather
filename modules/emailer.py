from datetime import datetime
import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime

def get_current_date_time():
    # Словарь с русскими названиями месяцев
    months = {
        1: 'янв',
        2: 'фев',
        3: 'мар',
        4: 'апр',
        5: 'май',
        6: 'июн',
        7: 'июл',
        8: 'авг',
        9: 'сен',
        10: 'окт',
        11: 'ноя',
        12: 'дек',
    }

    now = datetime.now()

    # Замена сокращенных названий месяцев на русские
    date_time = now.strftime("%H:%M   %d {month} %Y").replace('{month}', months[now.month])

    return date_time

def send_email(html_text, addresses_file):
    currentDateTime = get_current_date_time()
    # Чтение настроек SMTP из файла
    with open('modules\smtp_settings.yml', 'r', encoding='utf-8') as f:
        smtp_settings = yaml.safe_load(f)

    # Чтение адресов из файла
    with open(addresses_file, 'r', encoding='utf-8') as f:
        addresses = f.read().splitlines()

    # Создание объекта SMTP-сервера
    server = smtplib.SMTP(smtp_settings['smtp_server'], smtp_settings['smtp_port'])

    # Авторизация на SMTP-сервере
    server.login(smtp_settings['smtp_username'], smtp_settings['smtp_password'])

    # Отправка письма каждому адресату
    for address in addresses:
        # Формирование сообщения
        message = MIMEMultipart()
        message['From'] = smtp_settings['sender_email']
        message['To'] = address
        message['Subject'] = f'Сводка погоды на {currentDateTime}'

        # Добавление HTML-текста в сообщение
        html_part = MIMEText(html_text, 'html', 'utf-8')
        message.attach(html_part)

        # Отправка сообщения
        server.sendmail(smtp_settings['sender_email'], address, message.as_string())

    # Закрытие соединения с SMTP-сервером
    server.quit()