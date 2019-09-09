# coding: utf-8

# Python standard libraries import
import logging
import warnings

# External packages import
from flask import Flask

# Local import needing app to be created
from .tools import get_config_from_env
from .main.views import main


def create_app(config_final=None):

    # Create app
    app = Flask(__name__, instance_relative_config=True)

    # Logging
    warnings.simplefilter('default')
    logging.captureWarnings(True)

    # Initialize logging in key=value format
    formatter = logging.Formatter('created="{asctime}" logger={name} lvl={levelname} {message} '
                                  'in="{filename}:{funcName}:{lineno}"',
                                  style='{')

    # Initialize handler
    new_handler = logging.StreamHandler()
    new_handler.setFormatter(formatter)
    new_handler.setLevel(logging.DEBUG)

    # Capture warnings and redirect them to logs
    py_warning_logger = logging.getLogger('py.warnings')
    py_warning_logger.addHandler(new_handler)

    # Set logging level
    app.logger.setLevel(logging.DEBUG)

    # Replace Flask logger handler by our own
    for flask_handler in app.logger.handlers:
        app.logger.removeHandler(flask_handler)
    app.logger.addHandler(new_handler)

    app.logger.info('msg="Starting up app..."')

    # Get configuration from config files or environment variables
    app.logger.info('msg="Loading configuration..."')
    app.config.from_object('config_defaults')
    app.config.from_pyfile('config.py', silent=True)

    # Update configuration from environment variables named as config keys
    config_from_env = get_config_from_env(set(app.config.keys()))
    app.logger.info(f'msg="Config from env: {config_from_env}"')
    app.config.update(config_from_env or {})

    # Update configuration from param
    app.config.update(config_final or {})

    # Lower logger level from DEBUG to INFO after config is loaded, if Debug mode is False
    if not app.debug:
        new_handler.level = logging.INFO

    # Check all required config variables
    for key in ['REQUEST_TIMEOUT']:
        if app.config.get(key) is None:
            app.logger.critical(f'msg="Error: Required config variable not set" err="app.config[\'{key}\'] is None"')
            exit(1)


    @app.route("/test")
    def test_route():
        return "Test, World!"

    app.register_blueprint(main)
    app.logger.info('DEBUG MODE is {0}'.format(app.debug))

    return app
