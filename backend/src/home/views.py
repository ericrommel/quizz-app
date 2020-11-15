from flask import render_template

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
