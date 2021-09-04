from flask import Flask
from flask.globals import current_app

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail

from flask_login import LoginManager



from config import config

from redis import Redis, connection

import rq

##dependencies module initialization

db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'


def create_app(config_name):

    #Application setup and enviroment setup
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:

        from flask_sslify import SSLify

        sslify = SSLify(app)

    app.redis = Redis.from_url(app.config['REDIS_URL'])

    app.task_queue = rq.Queue('chama-tasks', connection = app.redis)


    #module integration with the application
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

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



