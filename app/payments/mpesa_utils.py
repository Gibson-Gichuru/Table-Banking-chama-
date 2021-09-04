from flask import current_app
import requests

import base64

import hashlib

import os

from datetime import datetime


class Mpesa:

    def __init__(self):

        self.auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        self.c2b_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"


    def format_phone_number(self, number):

        formart_number = list(number)

        if formart_number[0] == 0:

            formart_number[0] = "254"

            return "".join(formart_number)

        return "".join(formart_number)


    def lipa_na_mpesa_password(self):

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        business_code = os.environ.get('BUSINESS_CODE')

        pass_key = os.environ.get('PASS_KEY')

        row_transaction_pass = business_code + pass_key + timestamp

        return base64.b64encode(row_transaction_pass.encode('utf-8')).decode('utf-8'), timestamp



    def access_token(self):


        row_token = f"{os.environ.get('CONSUMER_KEY')}:{os.environ.get('CONSUMER_SECRET')}".encode('utf-8')

        #token = hashlib.sha3_256(row_token).hexdigest()

        token = base64.b64encode(row_token).decode("utf-8")

        headers = {

            "HOST":"sandbox.safaricom.co.ke",
            "Authorization": f"Basic {token}", 
            "Content-Type":"Application/json",
            
            }

        response = requests.get(self.auth_url, headers=headers)

        return response.json()['access_token']

    def initiate_stk_push(self, phoneNumber, amount):

        headers = {
            "Content-Type":"application/json",
            "Authorization": f"Bearer {self.access_token()}" 
            }

        payload = {
            "BusinessShortCode": os.environ.get('BUSINESS_CODE'),
            "Password": self.lipa_na_mpesa_password()[0],
            "Timestamp": self.lipa_na_mpesa_password()[1],
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": self.format_phone_number(phoneNumber),
            "PartyB": os.environ.get('BUSINESS_CODE'),
            "PhoneNumber": self.format_phone_number(phoneNumber),
            "CallBackURL": os.environ.get('CONFIRMATION_URL'),
            "AccountReference": "CompanyXLTD",
            "TransactionDesc": "Payment of X"
        }

        response = requests.post(self.c2b_url,  json = payload,headers = headers)

        return response


