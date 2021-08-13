from . import payment

from app.auth.views import authentication

from app.schema import PaymentSchema

schema = PaymentSchema()


@payment.route("/confirmation", methods = ['POST'])
def mpesa_callback_confirmation():

    pass

@payment.route('/validation', methods=['POST'])
def mpesa_callback_validation():

    pass


@payment.route('/make_payments')
@authentication.login_required()
def make_payments():

    pass
