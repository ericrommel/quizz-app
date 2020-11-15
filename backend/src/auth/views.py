from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .. import db
from .forms import LoginForm, SignUpForm
from ..models import User


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handle requests to the /signup route
    Add a user to the database through the sign up form
    """

    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            fullname=form.fullname.data,
            password=form.password.data,
        )

        # add user to the database
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered! You may now login.")

        # redirect to the login page
        return redirect(url_for("auth.login"))

    # load registration template
    return render_template("auth/register.html", form=form, title="Sign Up")


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle requests to the /login route
    Log an employees in through the sign in form
    """

    form = LoginForm()
    if form.validate_on_submit():

        # Check if the employees exists in the DB and if the password entered matches the password in the DB
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            # Log user in
            login_user(user)

            # Redirect to the correct dashboard (admin or normal user) page after login
            if user.is_admin:
                return redirect(url_for("home.admin_dashboard"))  # ToDo: Create an admin dashboard
            else:
                return redirect(url_for("home.homepage"))  # ToDo: Create a user dashboard
        # When login details are incorrect
        else:
            flash("Invalid email or password.")

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
