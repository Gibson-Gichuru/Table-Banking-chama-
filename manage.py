#Python Standard package importation
import os, sys

#Flask retaled package importation
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand

#application level parckage importation

from app import create_app, db
from app.models import User, Role

##application initalization 

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():

    return dict(user = User, role = Role, )

    pass


@manager.command
def test():

    pass

@manager.command
def deploy():

    pass


## Application commands Registration

manager.add_command("shell", Shell(make_context = make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":

    manager.run()
