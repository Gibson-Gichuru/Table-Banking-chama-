from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError

from app.models import User


class RegistrationForm(FlaskForm):

    email = StringField("email", validators=[DataRequired(), Length(1, 64), Email()])

    username = StringField(
        "username",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have onyl \
							letters, numbers, dots or underscore",
            ),
        ],
    )

    password = PasswordField(
        "password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="password must match"),
        ],
    )

    password2 = PasswordField("confirm password", validators=[DataRequired()])

    phonenumber = StringField("PhoneNumber", validators = [

        DataRequired(),
        Regexp(
            "^(\+?254|0)(7)([0-9]{8})$",
            0,
            "Invalid Phonenumber format"
        )
    ])

    submit = SubmitField("Register")

    # custom validators

    def validate_email(self, field):

        if User.query.filter_by(email=field.data).first():

            raise ValidationError("Email aready registered")

    def validate_username(self, field):

        if User.query.filter_by(username=field.data).first():

            raise ValidationError("Username aready in use")



class FogotPasswordForm(FlaskForm):

    email = StringField("email", validators=[DataRequired(), Length(1, 64), Email()])

    submit = SubmitField("Register")

class PasswordRestForm(FlaskForm):

    password = PasswordField(
        "password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="password must match"),
        ],
    )

    password2 = PasswordField("confirm password", validators=[DataRequired()])


    submit = SubmitField("Reset")



