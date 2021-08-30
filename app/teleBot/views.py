
from flask import config, request, current_app, Response
from flask.helpers import url_for


from . import bot

from .bot_func import send_message, parse_message

from app.models import User

from app import db

import requests

from .bot_func import get_bot_Access_token




@bot.route("/telebot", methods=['POST'])
def bot_callback():

    msg = request.get_json()

    chat_id, command, msg_sender_id, msg_sender, chama_username, amount = parse_message(
        msg)


    if command is not None:

        if command.name == "START":

            user = User.query.filter_by(tele_username=str(msg_sender_id)).first()

            if user is None:

                send_message(
                    chat_id,
                    f"Hello {msg_sender} !  \nNew Here? please text /use_bot@<username> to get started with this bot.\
                        \n\nPLEASE NOTE IT'S YOUR CHAMA USERNAME AND NOT TELEGRAM USERNAME",
                    current_app.config['TELEBOT_TOKEN'])

            else:

                send_message(
                    chat_id, f"Hello {msg_sender}! Long time no see, Grad you are back", current_app.config['TELEBOT_TOKEN'])

            return Response('ok', status=200)

        elif command.name == "USE_BOT":

            if chama_username is None:

                send_message(

                    chat_id=chat_id,
                    message="Looks like you forgot to issue your username!",
                    token=current_app.config['TELEBOT_TOKEN']
                )

                return Response('ok', status=200)

            user = User.query.filter_by(username=chama_username).first()

            if user is None:

                send_message(

                    chat_id=chat_id,
                    message="Looks like you are yet To register with our Chama",
                    token=current_app.config['TELEBOT_TOKEN']
                )

                return Response('ok', status=200)

            if user.tele_username is not None:

                send_message(
                    chat_id=chat_id,
                    message="Bot Aready connected To an account",
                    token = current_app.config['TELEBOT_TOKEN']
                )

                return Response('ok', status = 200)

            user.tele_username = msg_sender_id

            db.session.add(user)

            db.session.commit()

            send_message(

                chat_id=chat_id,
                message="Account Now Connected to this Bot",
                token=current_app.config['TELEBOT_TOKEN']
            )

            return Response('ok', status=200)

        elif command.name == "REGISTER":

            pass

        elif command.name == "PAYMENT":

            if amount is None:

                send_message(
                    chat_id=chat_id, 
                    message="PLEASE Do Issue an Amount To Transact",
                    token=current_app.config['TELEBOT_TOKEN'])

                return Response('ok', status = 200)

            user = User.query.filter_by(tele_username = str(msg_sender_id)).first()

            if user is None:

                send_message(
                    chat_id,
                    f"Hello {msg_sender} !  \nNew Here? please text /use_bot@<username> to get started with this bot.\
                        \n\nPLEASE NOTE IT'S YOUR CHAMA USERNAME AND NOT TELEGRAM USERNAME",
                    current_app.config['TELEBOT_TOKEN'])


                return Response('ok', status = 200)

            user.lauch_task("initiate_stk","payment" ,user.phone_number, amount)

            send_message(

                chat_id=chat_id,
                message="A payment request have been sent to you. \nPlease confirm it to complete\
                    transaction",

                token = current_app.config['TELEBOT_TOKEN']
            )

            return Response('ok', status = 200)

        else:

            pass

    else:

        send_message(chat_id, "invalid_command",
                     current_app.config['TELEBOT_TOKEN'])

        return Response('ok', status=200)

    return Response('ok', status=200)
