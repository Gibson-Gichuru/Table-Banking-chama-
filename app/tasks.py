import requests

from .payments.mpesa_utils import Mpesa


def initiate_stk(phonenumber, amount):

    mpesa = Mpesa()

    response = mpesa.initiate_stk_push(phoneNumber=phonenumber, amount=amount)    

    return response

