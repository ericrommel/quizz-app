from flask import redirect

from tests.conftest import get_url


def test_users_details_without_login_view(app, client):
    """
    Test list users details without login (a redirection should be done)
    """

    target_url = get_url(app=app, url="user.user_details")
    redirect_url = redirect(get_url(app=app, url="auth.login", next_url=target_url))
    response = client.get(target_url)
    assert response.status_code == 302
    assert response, redirect_url


def test_users_details_with_login_view(app, auth, client):
    """
    Test list users details with login (non-admin user)
    """

    target_url = get_url(app=app, url="user.user_details")
    auth.login(a_dict=dict(email="non-admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 200


def test_users_details_with_login_admin_view(app, auth, client):
    """
    Test list users_details with login and the user is an admin
    """

    target_url = get_url(app=app, url="user.edit_users", id=1)
    auth.login(a_dict=dict(email="admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 200


def test_user_detail_does_not_exist_view(app, auth, client):
    """
    Test list user detail whose doesn't exist
    """

    target_url = get_url(app=app, url="user.edit_users", id=10000000)
    auth.login(a_dict=dict(email="admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 404
