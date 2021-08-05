from flask import current_app, jsonify

from .import auth

@auth.route("/register")
def register():

    return "Welcome to Chama Api EndPoint"


@auth.route("/login")
def login():

    return "You are now logged in"