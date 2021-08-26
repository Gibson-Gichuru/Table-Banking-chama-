from datetime import datetime
from enum import unique

from sqlalchemy.orm import backref

from app import db

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app


#user session call back function
class Permissions:

    PAYMENT=0X02
    PAYMENT_HISTORY = 0X04
    PUBLIC_LEDGER =0X08
    SUSPEND_ACCOUNT = 0X16
    ADMINISTER = 0X80

class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)

    default = db.Column(db.Boolean, default = False, index = True)

    permisions = db.Column(db.Integer)

    #Tables relationship setup
    users = db.relationship('User',backref = 'role', lazy = 'dynamic')

    @staticmethod
    def insert_roles():


        """
            BITWISE OR COMBINATIONS OF PERMISSIONS TRANSLATE TO A ROLE

            lets take an 8 bit number to represent  all the permisions a user can preform 

            1. 0b00000000 >>>>> Have no permision and can do nothing
            2. 0b00000001>>>>>>Permision to Make payments
            3. 0b000000100>>>>> Permision to request payment history
            4. 0b000001000>>>>>> Permision to view public ledger
            5. 0b00001000>>>>>> Permission to suspend an account
            6. 0b10000000 >>>>> permision to administer

            

            class Permisions :

                Payment = 0X01 >>>> 0b00000001
                View_Public_ledger = 0X04 >>>> 0b00000010
                request_payment_history =0X08 >>>> 0b00000100
                suspend_account = 0X16 >>>0b00001000
                administer = 0X80 >>>> 0b100000000

            from the above permisions we can do a  bitwise or operation to obtain a user with specific permisions i.e

            user = Permisions.Payment | Permission.View_public_ledger | permisssions.request_payment_history >>>> 0b0000111

            other types of users ca easly be added by just performing a bitwise or operation

            admin will be composed of bitwise or operation to all the permissions


        """

        roles = {

            "User": (Permissions.PAYMENT | Permissions.PAYMENT_HISTORY | Permissions.PUBLIC_LEDGER, True),
            "bot": (Permissions.PAYMENT | Permissions.PAYMENT_HISTORY | Permissions.PUBLIC_LEDGER, False),
            "Administrator": (0xff, False)
        }

        for r in  roles:

            role = Role.query.filter_by(name = r).first()

            if role is None:

                role = Role(name = r)
                role.permisions = roles[r][0]
                role.default = roles[r][1]

                db.session.add(role)

        db.session.commit()

    



    def __str__(self):

        return f"<Role:{self.name}>"

class User(db.Model):

    __tablename__ = "users"

    ###Table Columns definations

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(120), unique = True)
    password_hash  = db.Column(db.String(240), nullable = False)
    register_date = db.Column(db.DateTime, default = datetime.utcnow)
    confirmed = db.Column(db.Boolean, default = False)
    phone_number = db.Column(db.String(20))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    #RELATIONSHIP

    bot_command = db.relationship("BotActivity", backref = "user", lazy = "dynamic")

    payment = db.relationship("Payment", backref='payer', lazy = 'dynamic')


    """When an instance of this class is made check if the email passed equal to the stored admin email
    
    
    if the email match the admins then assign the admin role to this instance
    
    """

    def __init__(self, **kwargs):

        super(User, self).__init__(**kwargs)

        if self.role is None:

            if self.email == current_app.config['MAIL_ADMIN']:

                self.role = Role.query.filter_by(permissions=0xff).first()

        if self.role is None:

            self.role = Role.query.filter_by(default =True).first()




    """ 
        ________________________________________________________________________

                        ###PASSWORD SECURITY IMPLEMENTATION###
        ________________________________________________________________________
        1.Make the password attrbute unreadable
        2. The password setter passess the encrypted version of the user passed password to password_hash for storage
        3. Incase a user interacts with any authentication requeried route we need to verify their given password

    """
    @property
    def password(self):

        return AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):

        return check_password_hash(self.password_hash, password)


    def generate_confirmation_token(self, expiration = 3600):

        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        return s.dumps({'Confirm': self.id})

    def generate_reset_token(self,expiration = 3600):

        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        return s.dumps({'reset':self.id})


    @staticmethod
    def reset_password(token, new_pasword):

        s = Serializer(current_app.config['SECRET_KEY'])

        try:

            data = s.loads(token)

        except:

            return False

        user = User.query.get(data['reset'])

        if user is None:

            return False

        user.password = new_pasword

        db.session.add(user)

        db.session.commit()

        return True

    @staticmethod
    def confirm(token):

        s= Serializer(current_app.config['SECRET_KEY'])

        try:

            data = s.loads(token)
        except:

            return False

        user = User.query.get(data['Confirm'])

        if user is None:

            return False

        user.confirmed = True

        db.session.add(user)

        db.session.commit()

        return True



    """USER ROLE VALIDATION 
    
        use bitwise & to compare if the permission_in question & permission_assigned == permission_in question

    """

    def can(self, permisions):

        return self.role is not None and (self.role.permisions & permisions ) == permisions

    def is_administrator(self):

        return self.can(Permissions.ADMINISTER)



    def __str__(self) -> str:
        return f"<User:{self.username}>"



class BotCommand(db.Model):

    __tablename__="bot_commands"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(65), unique = True, index = True)

    #RELATIONSHIPS

    activity = db.relationship("BotActivity", backref = "command", lazy = "dynamic")

    

    @staticmethod
    def insert_commands():

        active_commands = ["LEDGER", "PAYMENT", "LOAN", "HISTORY"]

        for c in active_commands:

            command = BotCommand.query.filter_by(name = active_commands[c]).first()

            if command is not None:

                command = BotCommand(name = active_commands[c])

                db.session.add(command)

        db.session.commit()




    def __str__(self):

        return f"<Command: {self.name}>"


class BotActivity(db.Model):

    __tablename__ = "bot_activity"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    command_id = db.Column(db.Integer, db.ForeignKey('bot_commands.id'))
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    finished = db.Column(db.Boolean, default = False)


    def _str__(self):

        return f"<Command:>"



class Payment(db.Model):

    __tablename_ ="payments"

    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    trans_time = db.Column(db.String(65))
    amount = db.Column(db.Numeric(10, 2))
    trans_id = db.Column(db.Text)
    reference = db.Column(db.Text)
    first_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone_number = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


