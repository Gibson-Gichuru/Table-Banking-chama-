from . import payment

from flask import current_app, url_for, jsonify, Response, request

from app.auth.views import authentication

from app.schema import PaymentSchema

import requests

from app.payments.mpesa_utils import Mpesa

schema = PaymentSchema()


@payment.route("/confirmation", methods = ['POST', 'GET'])
def confirmation():
    return Response('ok', status=200)

@payment.route('/validation', methods=['POST', 'GET'])
def validation():

    return Response('ok', status=200)


@payment.route('/make_payments')
@authentication.login_required()
def make_payments():

    pass

