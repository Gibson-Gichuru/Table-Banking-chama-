import os
import requests
from flask import Response
from . import bot

from .decorators import parser, construct_message

from flask import request

@parser
@construct_message
def updated_repy(message):

    return message

def send_message(message):

    token = os.environ.get('TELEBOT_TOKEN')

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    chat_id = message['message']['chat']['id']

    reply = message['reply_msg'] if "reply_msg" in message else "Oups! didn't get what you requested,\n do press the command menu for assistance"

    payload = {'chat_id':chat_id, 'text':reply}

    return requests.post(url=url, json =payload)

@bot.route("/telebot", methods=['POST'])
def bot_callback():

    user_msg = request.get_json()
    reply_msg= updated_repy(user_msg) 

    send_message(reply_msg)

    return Response('ok', status=200)
