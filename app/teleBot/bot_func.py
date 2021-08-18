import requests
from flask import current_app

import re


from app.models import BotCommand


PHONE_NUMBER_PATTERN = r"^(07|254)([0-9|7])(\d){7}"
USER_NAME_PATTERN = r"/[a-zA-z_]+@[a-zA-z0-9/-_]+"

def parse_msg_args(msg, pattern, white_out):

    ticker = re.findall(pattern, msg)

    if not ticker:

        return None

    return ticker[0].strip(f"/{white_out}@")


def parse_message(message):

    chat_id = message["message"]["chat"]["id"]
    msg_text = message["message"]["text"]
    sender_id = message['message']['from']['id']
    sender_name = message['message']['from']['first_name']

    pattern = r"^/[a-zA-Z_.-]+"

    ticker = re.findall(pattern, msg_text)

    if ticker:
    
        command = ticker[0].strip("/")


        bot_command = BotCommand.query.filter_by(name = command.upper()).first()

        if command.upper() == "USE_BOT":

            global USER_NAME_PATTERN

            chama_username = parse_msg_args(msg_text, USER_NAME_PATTERN, command)

            return chat_id, bot_command, sender_id, sender_name, chama_username, None
            

        if command.upper() == "PAYMENT":

            global PHONE_NUMBER_PATTERN

            phone_number = parse_msg_args(msg_text, PHONE_NUMBER_PATTERN, command)

            return chat_id, bot_command, sender_id, sender_name, None, phone_number

        return chat_id, bot_command, sender_id, sender_name, None, None

    else:

        return chat_id, None, sender_id, sender_name, None, None





def send_message(chat_id,message,token):

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {'chat_id':chat_id, 'text':message}

    response = requests.post(url, json = payload)

    return response



