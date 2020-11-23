from src.models import User, Question


def test_user_model(app):
    """
    Test number of records in User table
    """

    assert User.query.count() == 2


def test_did_number_model(app):
    """
    Test number of records in Question table
    """

    assert Question.query.count() == 5
