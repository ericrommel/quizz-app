from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from src import LOGGER


class QuestionForm(FlaskForm):
    """
    Form for an admin to add or edit a question
    """

    LOGGER.info("Generate the question form from admin")
    description = StringField("Problem", validators=[DataRequired()])
    correct_answer = StringField("Correct Answer", validators=[DataRequired()])
    subject = StringField("Subject related", validators=[DataRequired()])
    false_answer_1 = StringField("Wrong Answer 1", validators=[DataRequired()])
    false_answer_2 = StringField("Wrong Answer 2", validators=[DataRequired()])
    false_answer_3 = StringField("Wrong Answer 3", validators=[DataRequired()])
    levels = [(1, "Beginner"), (1.5, "Easy"), (2, "Normal"), (2.5, "Hard"), (3, "Very Hard"), (5, "Fiendish")]
    level = SelectField(u"Level", choices=levels)  # ToDo: Create a table for Levels
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    """
    Form for an admin to edit a user
    """

    LOGGER.info("Generate the user form from admin")
    fullname = StringField("Full name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired()])
    is_admin = SelectField(u"Is admin?", choices=["True", "False"])
    submit = SubmitField("Edit")
