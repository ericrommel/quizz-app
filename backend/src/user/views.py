from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import user
from .forms import UserForm
from .. import db, LOGGER
from ..models import User


@user.route("/users", methods=["GET", "POST"])
@login_required
def user_details():
    """
    Show the user detail
    """

    LOGGER.info("Show user details")
    user_obj = User.query.get_or_404(current_user.id)

    return render_template("user/users.html", user=user_obj, title="User Details")


@user.route("/users/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_user(id):
    """
    Edit a user
    """

    LOGGER.info("Edit user details")

    edit_a_user = True
    user_obj = User.query.get_or_404(id)
    form = UserForm(obj=user_obj)

    # ToDo: Implement change Password
    if form.validate_on_submit():
        user_obj.fullname = form.fullname.data
        user_obj.username = form.username.data
        user_obj.email = form.email.data

        try:
            # edit user in the database
            db.session.commit()
            flash("You have successfully edited the user.")
        except Exception as error:
            LOGGER.error(f"Exception: {error}")
            flash("Error: There was an error and this user cannot be edited. Check each item and try again")

        # redirect to the user page
        return redirect(url_for("user.user_details"))

    form.fullname.data = user_obj.fullname
    form.username.data = user_obj.username
    form.email.data = user_obj.email

    return render_template(
        "user/user.html",
        action="Edit",
        form=form,
        user=user_obj,
        title="Edit User",
    )
