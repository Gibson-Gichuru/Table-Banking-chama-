from datetime import datetime
from enum import unique

from sqlalchemy.orm import backref

from app import db
from app import login_manager

from flask_login import UserMixin, AnonymousUserMixin

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app

import redis

import rq

from sqlalchemy import desc


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


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

class User(db.Model, UserMixin):

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
    tele_username = db.Column(db.String(64), default = None)

    #RELATIONSHIP

    payment = db.relationship("Payment", backref='payer', lazy = 'dynamic')

    task = db.relationship('Task', backref = "user", lazy = 'dynamic')

    stk = db.relationship('Stk', backref = 'initiator', lazy = 'dynamic')


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

    def generate_auth_token(self, expiration = 3600):

        s = Serializer(current_app.config['SECRET_KEY'], expires_in= expiration)

        return s.dumps({'id':self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):

        s= Serializer(current_app.config['SECRET_APP'])

        try:

            data = s.dumps(token)

        except:

            return None

        return User.query.get(data['id'])



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


    def lauch_task(self, name, description, *args, **kwargs):

        if name == "initiate_stk":

            stk = Stk()

            stk.initiator = self

            db.session.add(stk)

            db.session.commit()

        rq_job = current_app.task_queue.enqueue('app.tasks.'+name, result_ttl = 550, *args, **kwargs)

        task = Task(id = rq_job.get_id(), name = name, description = description, user = self)

        db.session.add(task)

        db.session.commit()

        return task

    def get_tasks_in_progress(self):

        return Task.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name):

        return Task.query.filter_by(name=name, user=self, complete=False).order_by(desc(Task.time_stamp)).first()


    def __str__(self) -> str:
        return f"<User:{self.username}>"


class BotCommand(db.Model):

    __tablename__="bot_commands"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(65), unique = True, index = True)

    #RELATIONSHIPS


    @staticmethod
    def insert_commands():

        active_commands = ["LEDGER", "PAYMENT", "LOAN", "HISTORY", "START", "USE_BOT"]

        for c in active_commands:

            command = BotCommand.query.filter_by(name = c).first()

            if command is None:

                command = BotCommand(name = c)

                db.session.add(command)

        db.session.commit()




    def __str__(self):

        return f"<Command: {self.name}>"



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


class Stk(db.Model):

    __tablename__ = "stk"

    id = db.Column(db.Integer, primary_key = True)
    CheckoutRequestID = db.Column(db.String(64), index =True, default = None)
    timestamp =db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    payment_accepted = db.Column(db.Boolean, default = False)


class Task(db.Model):

    __tablename__ = 'tasks'

    id = db.Column(db.String(38), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    complete = db.Column(db.Boolean, default=False)
    time_stamp = db.Column(db.DateTime, default = datetime.utcnow)


    def get_rq_job(self):

        try:

            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)

        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):

            return None

        return rq_job

class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):

        return False

    def is_administrator(self):

        return False


login_manager.anonymous_user = AnonymousUser






