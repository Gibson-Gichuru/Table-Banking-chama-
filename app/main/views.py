from flask import render_template, flash, redirect
import flask
from flask.helpers import url_for
from . import main

from .form import  RegistrationForm

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
            "email", 
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