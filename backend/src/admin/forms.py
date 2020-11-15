from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from src import LOGGER


class QuestionsForm(FlaskForm):
    """
    Form for an admin to add or edit a question
    """

    LOGGER.info("Generate the question form")
    problem = StringField("Problem", validators=[DataRequired()])
    wrong_solution = StringField("Wrong Solution", validators=[DataRequired()])
    correct_solution = StringField("Correct Solution", validators=[DataRequired()])
    levels = ["Beginner", "Easy", "Normal", "Hard", "Very Hard", "Fiendish"]
    level = QuerySelectField(query_factory=levels, get_label="level")  # ToDo: Create a table for Levels
    submit = SubmitField("Submit")
