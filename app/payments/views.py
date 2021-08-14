from . import payment

from flask import current_app, url_for, jsonify, Response, request

from app.auth.views import authentication

from app.schema import PaymentSchema

import requests

from app.payments.mpesa_utils import Mpesa

from app.models import User, Payment

from app import db

import json

schema = PaymentSchema()


@payment.route("/confirmation", methods = ['POST', 'GET'])
def confirmation():

    payment_data =request.get_json()

    if payment_data:

        user = User.query.filter_by(phone_number = payment_data['SenderMSISDN']).first()

        if user is not None:

            new_pay = Payment(

                amount = payment_data['TransactionAmount'],
                trans_id = payment_data['TransactionID'],
                reference = payment_data['AccountReference'],
                first_name = payment_data['SenderFirstName'],
                middle_name = payment_data['SenderMiddleName'],
                last_name = payment_data['SenderLastName'],
                phone_number = payment_data['SenderMSISDN'],
                trans_time = payment_data['TransactionTime']

            )

            new_pay.payer = user

            db.session.add(new_pay)

            db.session.commit()

            return Response('ok', status = 200)

        else:

            return Response('cancel', status = 404)

    return Response('ok', status=200)

@payment.route('/validation', methods=['POST', 'GET'])
def validation():
    

    pay_validation = request.get_json()

    if pay_validation:

        user = User.query.filter_by(phone_number = pay_validation['SenderMSISDN']).first()

        if user is None:

            #send_message()

            return Response('cancel', status = 200)

    return Response('ok', status=200)


@payment.route('/make_payments')
@authentication.login_required()
def make_payments():

    ###make an stk push the users phone

    pass

