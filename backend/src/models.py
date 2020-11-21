from flask_login import UserMixin
from sqlalchemy import PickleType, DateTime, func
from sqlalchemy.ext.mutable import MutableList
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager, LOGGER


class QuizUser(db.Model):
    """
    Association table between user and quiz (many to many relationship)
    """

    __tablename__ = "quiz_users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"))
    time_for_execution = db.Column(DateTime(timezone=True))
    attempts = db.Column(db.Integer)


class Score(db.Model):
    """
    Create a Score table
    """

    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"))
    results = db.Column(PickleType)


class Quiz(db.Model):
    """
    Create a Quiz table
    """

    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    questions = db.Column(MutableList.as_mutable(PickleType), default=[])
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    first_execution = db.Column(DateTime(timezone=True), server_default=func.now())
    next_execution = db.Column(DateTime(timezone=True), onupdate=func.now())


class Question(db.Model):
    """
    Create a Question table
    """

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), index=True, unique=True)
    correct_answer = db.Column(db.String(500), index=True, unique=False)
    subject = db.Column(db.String(100), index=True, unique=False)
    false_answer_1 = db.Column(
        db.String(500), index=True, unique=False
    )  # ToDo: In order to simplify things here, I have used 'False Answers'. The right way is to use an ANSWER table
    false_answer_2 = db.Column(db.String(500), index=True, unique=False)
    false_answer_3 = db.Column(db.String(500), index=True, unique=False)
    level = db.Column(db.Float, index=True, unique=False)


class User(UserMixin, db.Model):
    """
    Create a User table
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), index=True, unique=False)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(80), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def check_password(self, password):
        """
        Check if hashed password matches with actual password
        """

        LOGGER.info("Check if the password is correct")
        return check_password_hash(self.password_hash, password)

    def __init__(self, fullname, email, username, password, is_admin=False):
        LOGGER.info("Create an user instance")
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return f"<User: {self.username}>"


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
