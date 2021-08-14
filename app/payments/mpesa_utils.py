from flask import current_app
import requests

import base64

import hashlib


class Mpesa:

    def __init__(self):

        self.auth_url = "https://api.proxyapi.co.ke/sandbox/mpesa/v1/auth"
        self.c2b_url = ""


    def access_token(self):

        row_token = f"{current_app.config['MPESA_KEY']}:{current_app.config['MPESA_SECRET']}".encode('utf-8')

        token = hashlib.sha3_256(row_token).hexdigest()

        headers = {

            "HOST":"api.proxyapi.co.ke",
            "X-Authorization": f"Basic {token}", 
            "Content-Type":"Application/json",
            
            }

        response = requests.get(self.auth_url, headers=headers)

        return response.json()['Data']['AccessToken']

    def initiate_stk_push(self, phoneNumber):

        pass

