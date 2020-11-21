from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from ..models import User


class SignUpForm(FlaskForm):
    """
    Form for users to create new account
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField(label="Username", validators=[DataRequired()])
    fullname = StringField(label="Full Name", validators=[DataRequired()])
    password = PasswordField(
        label="Password",
        validators=[
            DataRequired(),
            Length(min=6, max=12, message="Password length must be between %(min)d and %(max)d characters"),
        ],
    )
    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Both password fields must be equal!")],
    )
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email is already in use.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username is already in use.")


class LoginForm(FlaskForm):
    """
    Form for users to login
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
