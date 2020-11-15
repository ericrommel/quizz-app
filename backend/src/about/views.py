from flask import render_template

from . import about
from .. import LOGGER


@about.route("/about")
def about_page():
    """
    Render the homepage templates on the '/about' route
    """

    LOGGER.info("About page has been called")

    return render_template("about/about.html", title="About")
