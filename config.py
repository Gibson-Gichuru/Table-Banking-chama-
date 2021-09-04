import  os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    
    SSL_DISABLE = True
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_COMMITON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    ##Database Configurtions


    ##Email Configurations

    MAIL_SUBJECT_PREFIX = "CHAMA-APP"
    MAIL_SENDER = os.environ.get("MAIL_ADMIN")
    
    MAIL_ADMIN = os.environ.get("MAIL_ADMIN")


    ##Telebot Config settings

    TELEBOT_TOKEN = os.environ.get('TELEBOT_TOKEN')
    BOT_EMAIL = os.environ.get('BOT_EMAIL')
    BOT_PASS = os.environ.get('BOT_PASS')

    ##MPESA Config setting

    MPESA_KEY = os.environ.get('CONSUMER_KEY')
    MPESA_SECRET = os.environ.get('CONSUMER_SECRET')
    BUSINESS_CODE = os.environ.get('BUSINESS_CODE')

    ## Common application configuration


    ## Redis Config

    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

    @staticmethod
    def init_app(app):

        pass



class Development(Config):

    load_dotenv()

    #Development Specific configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL'
    ) or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


    @staticmethod
    def init_app(app):

        pass


class Testing(Config):

    TEST_MSISDN = os.environ.get('TEST_MSISDN')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL'
    ) or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

    @staticmethod
    def init_app(app):

        pass


class Production(Config):
    # Production Specific configuration

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    #SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("://", "ql://", 1) or \
    #"sqlite:///" + os.path.join(basedir, 'data.sqlite')


    @classmethod
    def init_app(cls, app):

        """Enable On production Error Logging and send the logfiles to the admin email"""

        Config.init_app(app)

        import logging

        from logging.handlers import SMTPHandler

        secure = None

        credentials = None

        if getattr(cls, "MAIL_USERNAME", None) is not None:

            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)

            if getattr(cls, 'MAIL_USE_TLS', None):

                secure = ()

        mail_handler = SMTPHandler(

            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.MAIL_ADMIN],
            subject=cls.MAIL_SUBJECT_PREFIX + "Application Error",
            credentials=credentials,
            secure=secure
        )

        mail_handler.setLevel(logging.WARNING)

        app.logger.addHandler(mail_handler)



class Heroku(Production):

    @classmethod
    def init_app(cls,app):
        
        Production.init_app(app)

        import logging

        from logging import StreamHandler

        file_handler = StreamHandler()

        file_handler.setLevel(logging.WARNING)

        app.logger.addHandler(file_handler)

        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app)


    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))


config = {
            'development':Development, 
            'production':Production,
            'default':Development,
            'heroku':Heroku,
        }