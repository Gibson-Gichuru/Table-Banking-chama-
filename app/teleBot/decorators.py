import functools
import  re
from .bot_func import use_bot, start, register, loan, payment
import pdb
def parser(func):

    common_pattern = r"/[a-zA-Z_]+"

    patterns = {
        "phone_number_pattern": r"@(\+?254|0)(7)([0-9]{8})",
        "user_name_pattern": r"@[a-zA-z0-9/-_]+",
        "payment_pattern": r"@[0-9]+",
    }

    @functools.wraps(func)
    def parse(message):

        msg_text = message['message']['text']

        match = re.findall(common_pattern, msg_text)
        
        for pattern in patterns:

            add_on = re.findall(patterns[pattern], msg_text)

        if len(match) == 0:

            return func(message)

        if len(add_on) == 0:

            add_on = None

        match = match[0].strip("/")

    
        add_on = add_on[0].strip("@")  if add_on is not None else None

        message['command'] = match
        message['add_on'] = add_on     

        return func(message)
    return parse


def construct_message(func):
    reply = {
        "PAYMENT":payment,
        "LOAN":loan,
        "USE_BOT":use_bot,
        "REGISTER":register,
        "START":start
    }

    @functools.wraps(func)
    def build(message):

        command = message['command'] if "command" in message else None
        telegram_username = message['message']['from']['username'] if "username" in message['message']['from'] else "New User"
        telegram_userId = message['message']['from']['id']

        if command is None:

            return func(message)

        add_on = message['add_on'] if "add_on" in message else None

        if command.upper() in reply:

            results = reply[command.upper()](
                add_on = add_on,
                telegram_username = telegram_username,
                telegram_userId =telegram_userId
                 
                )
            message['reply_msg'] = results 
        return func(message)

    return build

