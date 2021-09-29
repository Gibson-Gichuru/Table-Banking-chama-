import functools

from app.models import User, Stk
from app import db

import pdb

def check_user(func):
    @functools.wraps(func)
    def checker(*args, **kwargs):

        telegram_username = kwargs['telegram_username'] 

        telegram_userid = kwargs['telegram_userId']

        user = User.query.filter_by(tele_username = telegram_userid).first()

        if user is None:

            kwargs['message'] = f"Hello {kwargs['telegram_username']}, new here! Please Register With our App to use This Bot via the link bellow\n\
                https://chama-app.herokuapp.com"

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

    try :

        
        int(amount)

        user = User.query.filter_by(tele_username = kwargs['telegram_userId']).first()

        user.lauch_task('initiate_stk', 'payment', user.phone_number, amount)

        stk = Stk()

        stk.initiator = user


        task = user.get_task_in_progress('initiate_stk')

        job = task.get_rq_job()

        # A very bad idea to wait for the job
        # instead i will fetch the job results using a different thread 
        while True:

            if job.is_finished:

                break 


        result = job.return_value

        if result.status_code == 500:

            message = f"Hello {kwargs['telegram_username']},\nan error occured while processing your payment request\n Please do try again later"

            return message

        if "ResponseCode" in result.json() and result.json()['ResponseCode'] == "0":

            stk.CheckoutRequestID = result.json()['CheckoutRequestID']

            db.session.add(stk)
            db.session.commit()

            return message

        return message

    except ValueError as e:

        message = f"Hello {kwargs['telegram_username']},\ngrad you are always in touch.\
        \n\nMake sure the value entered for amount is a whole number"
        
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

    chama_username = kwargs['add_on'] if 'add_on' in kwargs else None

    if chama_username is None:

        message = f"Hello {kwargs['telegram_username']},\nPlease do provide your chama registered username to activate This bot"

    user = User.query.filter_by(tele_username = kwargs['telegram_username']).first()

    if user is None:

        return f"Hello {kwargs['telegram_username']},\nNo user is registered under that name on chama, Please do verify the username to procceed"

    if user.tele_username is None:

        user.tele_username = kwargs['telegram_userId']

        db.session.add(user)

        db.session.commit()

        return f"Hello {kwargs['telegram_username']},\nthis bot is Now linked to your chama Account"


    message = f"Hello {kwargs['telegram_username']},\nYou are aready linked to a chama account login in to chama website and update if need"

    return message







