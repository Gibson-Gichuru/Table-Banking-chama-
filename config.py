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



    ## Common application configuration

    pass


class Development(Config):

    #Development Specific configurations


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