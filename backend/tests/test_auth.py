import json

import pytest
from flask import session


def test_signup_view(auth):
    """
    Test that a sign up can be done
    """

    a_dict = dict(
        email="test@test.com",
        username="test",
        fullname="test test test",
        password="123456",
        is_admin=False,
    )

    response = auth.signup(a_dict)
    assert response.status_code == 201


def test_login_user_admin_view(client, auth, captured_templates):
    """
    Test that a login can be done with right credentials. User goes to admin's dashboard.
    """

    a_dict = dict(email="admin@admin.com", password="123456")
    response = auth.login(a_dict)

    template, context = captured_templates[0]

    assert template.name == "home/admin_dashboard.html"

    assert "title" in context
    assert context["title"] == "Dashboard"


def test_login_user_no_admin_view(client, auth, captured_templates):
    """
    Test that a login can be done with right credentials. User goes to user's dashboard.
    """

    a_dict = dict(email="non-admin@admin.com", password="123456")
    response = auth.login(a_dict)

    template, context = captured_templates[0]

    assert template.name == "home/dashboard.html"

    assert "title" in context
    assert context["title"] == "Dashboard"

    # Accessing context variables after the response
    with client:
        client.get("/")
        assert session["_user_id"] == "2"


@pytest.mark.parametrize(
    ("email", "password", "message"),
    (
        ("non-admin@admin.com", "654321", b"Invalid email or password."),
        ("123456", "non-admin@admin.com", b"Invalid email or password."),
    ),
)
def test_login_fail_view(auth, email, password, message):
    """
    Test that a login cannot be done with wrong credentials
    """

    a_dict = dict(email=email, password=password)
    response = auth.login(a_dict)
    assert response.status_code == 401
    assert message in response.data


def test_logout_view(auth):
    """
    Test that logout cannot be done without a login before
    """

    auth.login(dict(email="non-admin@admin.com", password="123456"))
    response = auth.logout()
    assert response.status_code == 200
