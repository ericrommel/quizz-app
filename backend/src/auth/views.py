import json

from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError

from . import auth
from .. import db, LOGGER
from .forms import LoginForm, SignUpForm
from ..models import User


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handle requests to the /signup route
    Add a user to the database through the sign up form
    """

    req = request.get_json() if request.get_json() else request.form
    form = SignUpForm(obj=req)

    if request.method == "POST":
        user = User(
            email=req.get("email"),
            username=req.get("username"),
            fullname=req.get("fullname"),
            password=req.get("password"),
            is_admin=req.get("is_admin", False),
        )

        # add user to the database
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(403, f'Username "{user.username}" or email "{user.email}" already exist in the database.')
        except Exception as error:
            LOGGER.error(f"Exception: {error}")
            abort(500, error)

        flash("You have successfully registered! You may now login.")

        # redirect to the login page
        return redirect(url_for("auth.login"), 201)
    elif request.method == "GET":
        # load registration template
        return render_template("auth/register.html", form=form, title="Sign Up")
    else:
        abort(405)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle requests to the /login route
    Log an users in through the sign in form
    """

    LOGGER.info("Try to sign in the system")
    req = request.get_json() if request.get_json() else request.form

    form = LoginForm()

    if request.method == "POST":

        # Check if the users exists in the DB and if the password entered matches the password in the DB
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            LOGGER.info("Login successful")
            # Log user in
            login_user(user)

            # Redirect to the correct dashboard (admin or normal user) page after login
            if user.is_admin:
                return redirect(url_for("home.admin_dashboard"))  # ToDo: Create an admin dashboard
            else:
                return redirect(url_for("home.dashboard"))
        # When login details are incorrect
        else:
            flash("Invalid email or password.")
            return render_template("auth/login.html", form=form, title="Login"), 401

    # load login template
    return render_template("auth/login.html", form=form, title="Login")


@auth.route("/logout")
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log a user out through the logout link
    """

    logout_user()
    flash("You have successfully been logged out.")

    # Redirect to the login page
    return redirect(url_for("auth.login"))
