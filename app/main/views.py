from flask import render_template, flash, redirect
import flask
from flask.helpers import url_for
from . import main

from .form import  RegistrationForm, FogotPasswordForm, PasswordRestForm

from app.models import User

from app import db

from app.email import send_email



@main.route("/join", methods= ["GET", "POST"])
def join():

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User()

        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data
        user.phone_number = form.phonenumber.data

        db.session.add(user)

        db.session.commit()

        send_email(
            user.email,
            "account Creation", 
            "email/email", 
            token = user.generate_confirmation_token(), 
            user = user
            
            )

        flash(f"Link sent to{user.email}, Confirm your email!", category="message")

        return render_template('register.html', form = form)

    return render_template("register.html", form = form)


@main.route("/confirm/<token>")
def confirm(token):

    if User.confirm(token):

        flash("Account Now Confirmed")

    else:

        flash("Unable To confirm account")

    return render_template("confirm.html")


@main.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():

    form = FogotPasswordForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email = form.email.data).first()

        if user is None:

            flash("Email Not Registered")


        send_email(
            user.email, 
            "Account Password Reset",
            "email/password", 
            user = user, 
            token = user.generate_reset_token()
            )

        flash(f"Reset Password Link Sent to {user.email}")

    return render_template('forgot_password.html', form = form)


@main.route("/confirm/password/reset/<token>", methods = ["POST", "GET"])
def confirm_reset(token):

    form = PasswordRestForm()

    if form.validate_on_submit():

        if User.reset_password(token, form.password.data):

            flash("Password reset Successfull")

            return render_template("password_reset.html", form = form)

        else:

            flash("Password reset Failed")
            return render_template("password_reset.html", form = form)

    return render_template('password_reset.html', form = form)