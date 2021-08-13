from flask import current_app
import requests

import base64


class Mpesa:

    def __init__(self):

        self.auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
        self.c2b_url = ""


    def access_token(self):

        row_token = f"{current_app.config['MPESA_KEY']}:{current_app.config['MPESA_SECRET']}".encode('utf-8')

        token = base64.b64encode(row_token).decode('utf-8')

        headers = {"Authorization": f"Basic {token}", "Content-Type":"Application/json"}

        options = {"grant_type":"client_credentials"}

        response = requests.get(self.auth_url, headers=headers, params= options)

        return response.json()['access_token']

    def initiate_stk_push(self, phoneNumber):

        pass

