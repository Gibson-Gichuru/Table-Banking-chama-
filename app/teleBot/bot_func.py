import requests
from flask import current_app

import re


from app.models import BotCommand


def parse_message(message):

    chat_id = message["message"]["chat"]["id"]
    msg_text = message["message"]["text"]

    pattern = r"/[a-zA-Z]{2,12}"

    ticker = re.findall(pattern, msg_text)

    if ticker:

        command = ticker[0].strip("/")

        bot_command = BotCommand.query.filter_by(name = command.upper()).first()

        return chat_id, bot_command

    return chat_id, None


def send_message(chat_id,message,token):

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {'chat_id':chat_id, 'text':message}

    response = requests.post(url, json = payload)

    return response



