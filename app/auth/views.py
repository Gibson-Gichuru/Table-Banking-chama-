
from .errors import forbidden_errror , unauthorised
from flask import current_app, jsonify, g, request
from app.models import User
from app.schema import UserSchema

from flask_httpauth import HTTPBasicAuth
from .import auth as auth_bp

from app import db

import pdb

auth = HTTPBasicAuth()
user_schema = UserSchema()

@auth.verify_password
def verify_password(email_or_token, password):

    if email_or_token == "":

        return False

    if password == "":

        g.current_user = User.query.filter_by(email = email_or_token).first()
        g.token_used = True

        return g.current_user is not None

    user = User.query.filter_by(email = email_or_token).first()

    if not user:

        return False

    g.current_user = user 
    g.toke_used = False

    return user.verify_password(email_or_token)


@auth_bp.route('/register', methods = ["POST"])
def register():

    request_body = request.get_json()

    pdb.set_trace()

    if not request_body:

        return forbidden_errror("No User information was provided for registation")

    errors = user_schema.validate(request_body)

    if errors:

        return forbidden_errror(errors)

    existing_user =User.query.filter_by(email = request_body['Email']).first()
    existing_username =User.query.filter_by(username = request_body['UserName']).first()
    existing_phone =User.query.filter_by(phone_numer = request_body['PhoneNumer']).first()

    if existing_user:

        return forbidden_errror("Email aready registered")

    if existing_username:

        return forbidden_errror("Username aready in use")

    if existing_phone:

        return forbidden_errror("PhoneNumber aready in user")

    user = User(

        email = request_body['Email'],
        username = request_body['UserName'],
        phone = request_body['Phone'],
    )

    user.password = request_body['Password']

    db.session.add(user)

    response = {"message":"Confirm Your account to the link sent to you"}

    return 
    
@auth_bp.route("/token", methods = ["POST"])
@auth.login_required
def token():
    
    if not g.current_user or g.token_used:

        return unauthorised("Invalid Credentials")


    return jsonify({"token":g.current_user.generate_auth_token(expiration = 3600),"expiration":3599})


