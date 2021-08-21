from flask import current_app
import requests

import base64

import hashlib

import os


class Mpesa:

    def __init__(self):

        self.auth_url = "https://api.proxyapi.co.ke/sandbox/mpesa/v1/auth"
        self.c2b_url = "https://api.proxyapi.co.ke/sandbox/mpesa/v1/c2b/customerpaybill"


    def format_phone_number(self, number):

        formart_number = list(number)

        if formart_number[0] == 0:

            formart_number[0] = "254"

            return "".join(formart_number)

        return "".join(formart_number)


    def access_token(self):

        row_token = f"{os.environ.get('CONSUMER_KEY')}:{os.environ.get('CONSUMER_SECRET')}".encode('utf-8')

        token = hashlib.sha3_256(row_token).hexdigest()

        headers = {

            "HOST":"api.proxyapi.co.ke",
            "X-Authorization": f"Basic {token}", 
            "Content-Type":"Application/json",
            
            }

        response = requests.get(self.auth_url, headers=headers)

        return response.json()['Data']['AccessToken']

    def initiate_stk_push(self, phoneNumber, amount):

        headers = {

            "HOST":"api.proxyapi.co.ke",
            "X-Authorization": f"Bearer {self.access_token()}" 
            }

        body = {

            "SenderMSISDN": self.format_phone_number(phoneNumber),
            "ReceiverShortcode": os.environ.get('BUSINESS_CODE'),
            "Amount":int(amount),
            "AccountReference": "Testing"

        }

        response = requests.post(self.c2b_url, headers = headers, json = body)

        return response


