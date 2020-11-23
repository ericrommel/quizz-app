import json
import os
import string
from pathlib import Path
from random import choice

import pytest
from flask import url_for, template_rendered

from src import create_app, db
from src.models import User, Question


def get_url(app, url, next_url=None, id=None):
    with app.test_request_context():
        return url_for(url, next=next_url, id=id)


class AuthActions(object):
    def __init__(self, app, client):
        self._app = app
        self._client = client

    def signup(self, a_dict):
        """
        Sign up request
        """

        return self._client.post(
            get_url(app=self._app, url="auth.signup"),
            data=json.dumps(a_dict),
            content_type="application/json",
            follow_redirects=True,
        )

    def login(self, a_dict):
        """
        Logo in request
        """

        return self._client.post(
            get_url(app=self._app, url="auth.login"),
            data=json.dumps(a_dict),
            content_type="application/json",
            follow_redirects=True,
        )

    def logout(self):
        """
        Log out request
        """

        return self._client.get(get_url(app=self._app, url="auth.logout"), follow_redirects=True)

    def generic_put(self, url, a_dict):
        """
        Generic PUT request
        """

        return self._client.put(url, data=json.dumps(a_dict), content_type="application/json", follow_redirects=True)

    def generic_post(self, url, a_dict):
        """
        Generic POST request
        """

        return self._client.post(url, data=json.dumps(a_dict), content_type="application/json", follow_redirects=True)


@pytest.fixture
def auth(app, client):
    return AuthActions(app, client)


@pytest.fixture()
def app():
    """
    Create app with a database test
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # Create 'db' folder if it is not done yet
    try:
        os.makedirs(Path(current_dir, "db"))
    except OSError:
        pass

    db_dir = Path(current_dir, "db")

    app = create_app("testing")
    app.config.from_object("config.TestingConfig")
    app.config.from_mapping(
        SECRET_KEY="TeMpOrArYkEyHaSbEeNuSeD",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,  # avoid FSADeprecationWarning
        PRESERVE_CONTEXT_ON_EXCEPTION=False,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(db_dir, 'quiz-test-db.db')}",
    )

    with app.app_context():
        # Will be called before every test
        db.create_all()

        # Create test admin user
        admin = User(
            email="admin@admin.com", username="admin", fullname="Name of Admin", password="123456", is_admin=True
        )

        # Create test non-admin user
        user1 = User(
            email="non-admin@admin.com",
            username="non-admin",
            fullname="Full Name User",
            password="123456",
            is_admin=False,
        )

        # Save users to database
        db.session.add(admin)
        db.session.add(user1)
        db.session.commit()

        # Add and save 5 questions to database
        with open("sample_5_questions.json") as fjson:
            json_data = json.load(fjson)
            levels = {"Beginner": 1, "Easy": 1.5, "Normal": 2, "Hard": 2.5, "Very Hard": 3, "Fiendish": 5}
            for f in json_data:
                q = Question(
                    subject=f.get("Subject"),
                    description=f.get("QuestionText"),
                    correct_answer=f.get("Answer"),
                    false_answer_1=f.get("False1"),
                    false_answer_2=f.get("False2"),
                    false_answer_3=f.get("False3"),
                    level=levels.get(f.get("Level")),
                )
                db.session.add(q)
                db.session.commit()

        yield app

        # Will be called after every test
        User.query.delete()
        Question.query.delete()
        db.session.commit()
        db.drop_all()


@pytest.fixture()
def client(app):
    """
    Make requests to the application without running the server
    """

    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


def json_of_response(response):
    """
    Decode json from response
    """

    return json.loads(response.data.decode("utf8"))


def get_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    a_string = "".join(choice(letters) for i in range(length))
    return a_string


def get_random_int(length: int) -> int:
    if length > 10:
        length = 10

    numbers = "0123456789"
    a_string = "".join(choice(numbers) for i in range(length))
    return int(a_string)


def populate_user(n):
    for i in range(n):
        username = get_random_string(10)
        email = f"{username}@gmail.com"
        user = User(
            username=username,
            password="123456",
            is_admin=False,
            fullname=f"First Name {username} Last Name",
            email=email,
        )

        # save user to database
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
