import src

from flask import render_template, jsonify


def bad_request(e):
    src.LOGGER.error(e)
    return render_template("errors/400.html", error=e, title="Error 400"), 400


def unauthorized(e):
    src.LOGGER.error(e)
    return render_template("errors/401.html", error=e, title="Error 401"), 401


def forbidden(e):
    src.LOGGER.error(e)
    return render_template("errors/403.html", error=e, title="Error 403"), 403


def page_not_found(e):
    src.LOGGER.error(e)
    return render_template("errors/404.html", error=e, title="Error 404"), 404


def method_not_allowed(e):
    src.LOGGER.error(e)
    return render_template("errors/405.html", error=e, title="Error 405"), 405


def internal_server_error(e):
    src.LOGGER.error(e)
    return render_template("errors/500.html", error=e, title="Error 500"), 500
