# Built-in imports
import os
from pathlib import Path

# Thirty part imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Local imports
from config import app_config
from log import Log
from src.errors import page_not_found, internal_server_error, bad_request, unauthorized, forbidden, method_not_allowed

LOGGER = Log("quizz-app").get_logger(logger_name="app")

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    """
    This is the application factory function. It creates and configures the app
    """

    LOGGER.info("Initialize Flask app")
    app = Flask(__name__, instance_relative_config=True)

    current_dir = os.path.dirname(os.path.abspath(__file__))

    LOGGER.info("Create 'db' folder if it is not done yet")
    try:
        os.makedirs(Path(current_dir, "db"))
    except OSError:
        pass

    db_dir = Path(current_dir, "db")

    # Error Handling
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, internal_server_error)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py", silent=True)
    app.config["SECRET_KEY"] = "TeMpOrArYkEyHaSbEeNuSeD"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # avoid FSADeprecationWarning
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{Path(db_dir, 'quizz-db.db')}"

    LOGGER.info("Initialize the application to use with its setup DB")
    Bootstrap(app)
    db.init_app(app)

    LOGGER.info("Register and attach the `LoginManager`")
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page"
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    from .admin import admin as admin_bprint

    app.register_blueprint(admin_bprint)

    from .about import about as about_bprint

    app.register_blueprint(about_bprint)

    from .auth import auth as auth_bprint

    app.register_blueprint(auth_bprint)

    from .home import home as home_bprint

    app.register_blueprint(home_bprint)

    return app
