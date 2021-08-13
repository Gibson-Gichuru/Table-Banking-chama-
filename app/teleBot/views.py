
from flask import request, current_app, Response

from . import bot

from .bot_func import send_message, parse_message

@bot.route("/telebot", methods = ['POST'])
def bot_callback():

    msg = request.get_json()

    chat_id , command = parse_message(msg)

    if command is None:

        if command =="START":

            send_message(chat_id, "Hello Mate! Welcome to your Chama Bot assistant", current_app.config['TELEBOT_TOKEN'])

            return Response('ok', status = 200)

        send_message(chat_id, "invalid_command", current_app.config['TELEBOT_TOKEN'])


    return Response('ok', status=200)


