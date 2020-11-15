import os

from config import app_config
from flask import Flask, render_template
from flask_bootstrap import Bootstrap


def create_app(config_name):
    """
    This is the application factory function. It creates and configures the app
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    app.config.from_pyfile("config.py", silent=True)

    Bootstrap(app)
    from .home import home as home_bprint

    app.register_blueprint(home_bprint)

    from .about import about as about_bprint

    app.register_blueprint(about_bprint)

    return app
