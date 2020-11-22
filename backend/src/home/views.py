from flask import abort, render_template, url_for
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from . import home
from .. import LOGGER


@home.route("/")
@home.route("/index")
def homepage():
    """
    Render the homepage templates on the '/' or '/index' route
    """

    LOGGER.info("Home page has been called")

    return render_template("home/index.html", title="Home")


@home.route("/admin/dashboard")
@login_required
def admin_dashboard():
    """
    Render the admin dashboard template on the /admin/dashboard route
    """

    if not current_user.is_admin:
        abort(403)

    return render_template("home/admin_dashboard.html", title="Dashboard")


@home.route("/dashboard")
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """

    return redirect(url_for("user.dashboard", user_id=current_user.id))
