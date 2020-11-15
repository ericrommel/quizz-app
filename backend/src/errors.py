import src

from flask import render_template, jsonify


def bad_request(e):
    src.LOGGER.error(e)
    return render_template("errors/400.html"), 400


def unauthorized(e):
    src.LOGGER.error(e)
    return render_template("errors/400.html"), 401


def forbidden(e):
    src.LOGGER.error(e)
    return render_template("errors/403.html"), 403


def page_not_found(e):
    src.LOGGER.error(e)
    return render_template("errors/404.html"), 404


def method_not_allowed(e):
    src.LOGGER.error(e)
    return render_template("errors/405.html"), 405


def internal_server_error(e):
    src.LOGGER.error(e)
    return render_template("errors/500.html"), 500
