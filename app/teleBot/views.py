
from flask import request, current_app, Response

from . import bot

from .bot_func import send_message, parse_message

from app.models import User

from app import db


@bot.route("/telebot", methods=['POST'])
def bot_callback():

    msg = request.get_json()

    chat_id, command, msg_sender_id, msg_sender, chama_username, phone_number = parse_message(msg)

    if command is not None:

        if command.name == "START":

            user = User.query.filter_by(tele_username=msg_sender_id).first()

            if user is None:

                send_message(
                    chat_id, 
                    f"Hello {msg_sender} !  \nNew Here? please text /use_bot followed by your chama registered username to get started with this bot.\
                        \n\nPLEASE NOT ITS YOUR CHAMA USERNAME AND NOT TELEGRAM USERNAME",
                     current_app.config['TELEBOT_TOKEN'])

            else:

                send_message(
                    chat_id, f"Hello {msg_sender}! Long time no see, Grad you are back", current_app.config['TELEBOT_TOKEN'])

            return Response('ok', status=200)

        elif command.name == "USE_BOT":

            username = parse_message(message = msg)[-1]

            if username is None:

                send_message(

                    chat_id=chat_id,
                    message= "Looks like you forgot to issue your username!",
                    token= current_app.config['TELEBOT_TOKEN']
                )

                return Response('ok', status = 200)

            user = User.query.filter_by(username = username).first()

            if user is None:

                send_message(

                    chat_id=chat_id,
                    message= "Looks like you are yet To register with our Chama",
                    token= current_app.config['TELEBOT_TOKEN']
                )

                return Response('ok', status = 200)

            user.tele_username = msg_sender_id

            db.session.add(user)

            db.session.commit()

            send_message(

                    chat_id=chat_id,
                    message= "Account Now Connected to this Bot",
                    token= current_app.config['TELEBOT_TOKEN']
                )


            return Response('ok', status = 200)

        elif command.name == "REGISTER":

            pass

        elif command.name == "PAYMENTS":

            pass

        else:

            pass

    else:

        send_message(chat_id, "invalid_command",
                    current_app.config['TELEBOT_TOKEN'])

        return Response('ok', status=200)

    return Response('ok', status=200)
