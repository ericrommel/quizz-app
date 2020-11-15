from config import app_config
from flask import Flask
from flask_bootstrap import Bootstrap
from log import Log
from src.errors import page_not_found, internal_server_error, bad_request, unauthorized, forbidden, method_not_allowed

LOGGER = Log("quizz-app").get_logger(logger_name="app")


def create_app(config_name):
    """
    This is the application factory function. It creates and configures the app
    """

    LOGGER.info("Initialize Flask app")
    app = Flask(__name__, instance_relative_config=True)

    # Error Handling
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, internal_server_error)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py", silent=True)

    Bootstrap(app)
    from .home import home as home_bprint

    app.register_blueprint(home_bprint)

    from .about import about as about_bprint

    app.register_blueprint(about_bprint)

    return app
