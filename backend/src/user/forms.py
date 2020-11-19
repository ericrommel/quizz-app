from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, InputRequired, Email

from src import LOGGER
from src.models import Question


class UserForm(FlaskForm):
    """
    Form for a user to edit its information
    """

    LOGGER.info("Generate the user form")
    fullname = StringField("Full Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-Mail", validators=[Email()])
    submit = SubmitField("Edit")


class SetForAQuizForm(FlaskForm):
    """
    Form for a user to create a new quiz
    """

    LOGGER.info("Generate the quiz form for the user")
    number_of_questions = SelectField(
        "Select the number of questions to solve", choices=["5", "10", "15", "20"], validators=[InputRequired()]
    )
    subject = SelectField("Select a subject", choices=[], validators=[InputRequired()])

    submit = SubmitField("Generate the quiz")


class SolveQuizForm(FlaskForm):
    """
    Form that show a question form to solve by the user
    """

    LOGGER.info("Generate the question form for the quiz")
    question = RadioField(choices=[], validators=[InputRequired()])
    submit = SubmitField("Next")
