from flask import render_template

from . import home


@home.route("/")
@home.route("/index")
def homepage():
    """
    Render the homepage templates on the '/' or '/index' route
    """

    return render_template("home/index.html", title="Home")
