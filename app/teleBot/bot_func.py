import functools

from app.models import User

def check_user(func):
    @functools.wraps(func)
    def checker(*args, **kwargs):

        telegram_username = kwargs['telegram_username'] 

        telegram_userid = kwargs['telegram_userId']

        user = User.query.filter_by(tele_username = telegram_userid).first()

        if user is None:

            kwargs['message'] = f"Hello {kwargs['telegram_username']}, new here! Please Register With our App to use This Bot"

            return func(*args, **kwargs)

        return func(*args,**kwargs)

    return checker


@check_user
def start(*args, **kwargs):

    message = kwargs['message'] if 'message' in kwargs else f"Hello {kwargs['telegram_username']},\n grad you are always in touch"

    return message
@check_user
def payment(*args, **kwargs):

    amount = kwargs['add_on'] if 'add_on' in kwargs else None 
    message = kwargs['message'] if 'message' in kwargs else f"Hello {kwargs['telegram_username']},\ngrad you are always in touch.\
        \n\nPayment request sent to your phone\ndo confirm it to complete the payment"

    if amount is None:

        message = f"Hello {kwargs['telegram_username']},\ngrad you are always in touch.\
        \n\nNo amount was issued for transaction. please confirm your payment command and make sure it is as follows.\n/payment@amount"
        
    

    return message

@check_user
def register(*args, **kwargs):

    message = kwargs['message'] if 'message' in kwargs else f"Hello {kwargs['telegram_username']},\nan account have aready been linked to this bot"

    return  message
@check_user
def loan(*args, **kwargs):

    message = kwargs['message'] if 'message' in kwargs else f"Hello {kwargs['telegram_username']},\nlogin to the chama website to appy for a loan"

    return message
@check_user
def use_bot(*args, **kwargs):

    message = "Account linked to this bot"

    return message







