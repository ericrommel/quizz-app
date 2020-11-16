from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from src import LOGGER


class UserForm(FlaskForm):
    """
    Form for a user to edit its information
    """

    LOGGER.info("Generate the user form")
    fullname = StringField("Full Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-Mail", validators=[DataRequired()])
    submit = SubmitField("Edit")
