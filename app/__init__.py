from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail

from config import config

##dependencies module initialization

db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()

def create_app(config_name):

    #Application setup and enviroment setup
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


    #module integration with the application
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)

    #Application Blueprint Registration

    ###########AUTHENTICATION BLUEPRINT REGISTRATION##############
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = "/auth")

    ###########MAIN BLUEPRINT REGISTRATION#######################
    from  .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    ###########PAYMENT BLUEPRINT REGiSTRATION####################
    from .payments import payment as payment_blueprint
    app.register_blueprint(payment_blueprint)

    #############TELEGRAM BOT BLUEPRINT REGISTRATION#############
    from .teleBot import  bot
    app.register_blueprint(bot, url_prefix= "/bot")



    return app



