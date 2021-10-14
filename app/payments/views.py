from sqlalchemy.orm import joinedload
from . import payment

from flask import current_app, url_for, jsonify, Response, request

from app.auth.views import authentication

from app.schema import PaymentSchema

import requests

from app.payments.mpesa_utils import Mpesa

from app.models import User, Payment, Stk

from app import db

import json

import pdb

schema = PaymentSchema()


@payment.route("/confirmation", methods = ['POST', 'GET'])
def confirmation():

    payment_data =request.get_json()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    if payment_data:

        user = User.query.filter_by(phone_number = payment_data['SenderMSISDN']).first()

        if user is not None:

            new_pay = Payment(

                amount = payment_data['TrasAmount'],
                trans_id = payment_data['TransID'],
                reference = payment_data['AccountReference'],
                first_name = payment_data['FirstName'],
                middle_name = payment_data['MiddleName'],
                last_name = payment_data['LastName'],
                phone_number = payment_data['MSISDN'],
                trans_time = payment_data['TransTime']

            )

            new_pay.payer = user

            task = user.get_task_in_progress(name = "initiate_stk")

            if task is not None:

                task.complete = True
                db.session.add(task)

            db.session.add(new_pay)

            db.session.commit()

            return jsonify(context), 200

        else:

            return Response('cancel', status = 404)

    return Response('ok', status=200)

@payment.route('/validation', methods=['POST', 'GET'])
def validation():
    

    pay_validation = request.get_json()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    if pay_validation:

        user = User.query.filter_by(phone_number = pay_validation['MSISDN']).first()

        if user is None:

            #send_message()

            context_reject = {
                "ResultCode": 0,
                "ResultDesc": "Cancelled"
            }

            return jsonify(context_reject), 200

    return jsonify(context), 200


@payment.route('/stk', methods =["POST"])
def stk():

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    context_reject = {
        "ResultCode": 0,
        "ResultDesc": "Cancelled"
    }


    """Improvements to this implementation
    
    use a second thread to query the payment status Daraja api using the payment id to confirm that the payment have been done
    and update the database"""
    stk_data = request.get_json()

    

    if stk_data and stk_data['Body']['stkCallback']['ResultCode'] != 0:

        return Response(context_reject, status = 404)
 

    stk = Stk.query.filter_by(CheckoutRequestID = stk_data['Body']['stkCallback']['CheckoutRequestID']).first()

    stk.payment_accepted = True

    db.session.add(stk)
    db.session.commit()

    return jsonify(context), 200


@payment.route('/make_payments', methods = ['POST'])
@authentication.login_required()
def make_payments():

    ###make an stk push the users phone

    request_data = request.get_json()

    if request_data():

        mpesa = Mpesa()

        stk = mpesa.initiate_stk_push(request_data['PhoneNumber'], request_data['Amount'])

        if stk.status == 200:

            return Response({'message':"confirm the payment your phone"}, status=200)

        else:

            return Response(stk.json())

    return Response({"Message":"payment endpoint"})


