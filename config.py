import  os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    load_dotenv()

    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")

    ##Database Configurtions


    ##Email Configurations



    ## Common application configuration

    pass


class Development(Config):

    #Development Specific configurations

    def init_app(app):

        pass


class Production(Config):
    # Production Specific configuration

    pass

config = {
            'development':Development, 
            'production':Production,
            'default':Development
        }