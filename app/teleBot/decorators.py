import functools
import  re

from .bot_func import start, payment, register, loan, use_bot

from app.models import User


def parser(func):

    patterns = {

        "phone_number_pattern": r"/[a-zA-z_]+@(\+?254|0)(7)([0-9]{8})",
        "user_name_pattern": r"/[a-zA-z_]+@[a-zA-z0-9/-_]+",
        "payment_pattern": r"/[a-zA-Z_-]+@[0-9]+",
        "common_pattern": r"/[a-zA-Z_]+"
    }

    @functools.wraps(func)
    def parse(message):

        msg_text = message['message']['text']

        for pattern in patterns:

            match = re.findall(patterns[pattern], msg_text)

        if len(match) == 0:

            return func(message)

        match = match[0].strip("/")        

        try:
            separator = match.index("@")
            command = "".join(match[:separator])
            add_on = "".join(match[separator+1:])
            message['command'] = command
            message['add_on'] = add_on


        except Exception:

            command = match
            message['command'] = command
            message['add_on'] = None

        return func(message)
    return parse


def construct_message(func):
    reply = {

        "PAYMENT":payment,
        "USE_BOT":use_bot,
        "LOAN":loan,
        "REGISTER":register,
        "START":start
    }    
    @functools.wraps(func)
    def build(message):

        command = message['command'] if "command" in message else None

        if command is None:

            return func(message)

        add_on = message['add_on'] if "add_on" in message else None

        if command.upper() in reply:

            results = reply[command.upper()](add_on)

            message['reply_msg'] = results 
        return func(message)

    return build



def check_user(func):

    @functools.wraps(func)
    def checker(*args, **kwargs):

        telegram_username = kwargs['tele_username'] 

        user = User.query.filter_by()
