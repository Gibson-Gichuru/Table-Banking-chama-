from datetime import datetime

from app import db

from werkzeug.security import generate_password_hash, check_password_hash

class Permissions:

    pass

class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)

    #Tables relationship setup
    users = db.relationship('User',backref = 'role', lazy = 'dynamic')

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
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))


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




    def __str__(self) -> str:
        return f"<User:{self.username}>"


