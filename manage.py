#Python Standard package importation


import json
import os, sys, requests

#Flask retaled package importation
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand

from flask import url_for

#application level parckage importation

from app import create_app, db
from app.models import User, Role, BotCommand, Task, Stk

from app.payments.mpesa_utils import Mpesa

from flask_migrate import upgrade

##application initalization 

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():

    return dict(User = User, Role = Role, db = db, BotCommand = BotCommand, Task = Task, Stk = Stk)


@manager.command
def test():

    pass

@manager.command
def deploy():

    # update  database schema to the database

    upgrade()

    ## setup the user roles
    Role.insert_roles()

    ## setup the telegram bot user commands

    BotCommand.insert_commands()
    
@manager.command
def register_bot():

    url = f"https://api.telegram.org/bot{app.config['TELEBOT_TOKEN']}/setWebhook?url={url_for('bot.bot_callback', _external =True)}"

    response = requests.get(url)

    print(response.json()['description'])


@manager.command
def mpesa_callbacks():

    from app.payments.mpesa_utils import Mpesa

    mpesa = Mpesa()

    url  = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"

    headers = {

        "HOST":"sandbox.safaricom.co.ke",
        "Authorization": f"Bearer {mpesa.access_token()}",
        "Content-Type":"application/json"
    }

    body  = {

        "ShortCode":app.config['BUSINESS_CODE'],
        "ResponseType":"Cancelled",
        "ConfirmationURL":app.config['CONFIRMATION_URL'],
        "ValidationURL":app.config['VALIDATION_URL']
    }

    response = requests.post( url=url, headers=headers, json=body)
    return response.json()

## Application commands Registration

manager.add_command("shell", Shell(make_context = make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":

    manager.run()
