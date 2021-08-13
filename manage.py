#Python Standard package importation


import os, sys, requests

#Flask retaled package importation
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand

from flask import url_for

#application level parckage importation

from app import create_app, db
from app.models import User, Role, BotActivity, BotCommand

##application initalization 

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():

    return dict(User = User, Role = Role, db = db, BotActivity = BotActivity, BotCommand = BotCommand)


@manager.command
def test():

    pass

@manager.command
def deploy():

    pass
@manager.command
def register_bot():

    url = f"https://api.telegram.org/bot{app.config['TELEBOT_TOKEN']}/setWebhook?url={url_for('bot.bot_callback', _external =True)}"

    response = requests.get(url)

    print(response.json()['description'])



## Application commands Registration

manager.add_command("shell", Shell(make_context = make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":

    manager.run()
