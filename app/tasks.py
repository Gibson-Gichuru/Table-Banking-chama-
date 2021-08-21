import requests

from .payments.mpesa_utils import Mpesa

import pdb

def initiate_stk(phonenumber, amount):

    mpesa = Mpesa()

    response = mpesa.initiate_stk_push(phoneNumber=phonenumber, amount=amount)    

    print(response.json())

