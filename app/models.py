from datetime import datetime

from app import db

class Permissions:

    pass

class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)

    def __str__(self):

        return f"<Role:{self.name}>"

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(120), unique = True)
    password_hash  = db.Column(db.String(240), nullable = False)
    register_date = db.Column(db.DateTime, default = datetime.utcnow)


    def __str__(self) -> str:
        return f"<User:{self.username}>"


