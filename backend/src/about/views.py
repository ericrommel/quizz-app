from flask import render_template

from . import about


@about.route("/about")
def about_page():
    """
    Render the homepage templates on the '/about' route
    """

    return render_template("about/about.html", title="About")
