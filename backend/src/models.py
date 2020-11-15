from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager, LOGGER


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