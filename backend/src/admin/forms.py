from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from src import LOGGER


class QuestionForm(FlaskForm):
    """
    Form for an admin to add or edit a question
    """

    LOGGER.info("Generate the question form")
    description = StringField("Problem", validators=[DataRequired()])
    correct_answer = StringField("Correct Answer", validators=[DataRequired()])
    subject = StringField("Subject related", validators=[DataRequired()])
    false_answer_1 = StringField("Wrong Answer 1", validators=[DataRequired()])
    false_answer_2 = StringField("Wrong Answer 2", validators=[DataRequired()])
    false_answer_3 = StringField("Wrong Answer 3", validators=[DataRequired()])
    levels = ["Beginner", "Easy", "Normal", "Hard", "Very Hard", "Fiendish"]
    level = SelectField(u"Level", choices=levels)  # ToDo: Create a table for Levels
    submit = SubmitField("Submit")
