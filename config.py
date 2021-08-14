import  os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    load_dotenv()

    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_COMMITON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    ##Database Configurtions


    ##Email Configurations

    MAIL_SUBJECT_PREFIX = "CHAMA-APP"
    MAIL_SENDER = os.environ.get("MAIL_ADMIN")
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_ADMIN = os.environ.get("MAIL_ADMIN")


    ##Telebot Config settings

    TELEBOT_TOKEN = os.environ.get('TELEBOT_TOKEN')

    ##MPESA Config setting

    MPESA_KEY = os.environ.get('CONSUMER_KEY')
    MPESA_SECRET = os.environ.get('CONSUMER_SECRET')
    BUSINESS_CODE = os.environ.get('BUSINESS_CODE')

    ## Common application configuration



class Development(Config):

    #Development Specific configurations

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USER_TLS = True


    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL'
    ) or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    def init_app(app):

        pass


class Testing(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL'
    ) or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

    def inti_app(app):

        pass


class Production(Config):
    # Production Specific configuration

    pass

config = {
            'development':Development, 
            'production':Production,
            'default':Development
        }