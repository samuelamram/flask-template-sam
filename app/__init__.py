# coding: utf-8

# Python standard libraries import
import logging
import warnings
from os import getenv, environ

# External packages import
from flask import Flask

# Local import needing app to be created
from .tools import string2bool
from .main import main


def create_app(config_final=None):
    # Create app
    app = Flask(__name__, instance_relative_config=True)

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
    py_warning_handler = logging.StreamHandler()
    py_warning_handler.setFormatter(formatter)
    py_warning_logger.addHandler(py_warning_handler)
    warnings.simplefilter('default')
    logging.captureWarnings(True)

    # Set logging level
    app.logger.setLevel(logging.DEBUG)

    # Replace Flask logger handler by our own
    for flask_handler in app.logger.handlers:
        print(f'Removing handler {flask_handler}')
        app.logger.removeHandler(flask_handler)
        # if flask_handler.level == logging.ERROR:
        #     flask_handler.setLevel(logging.INFO)
        # flask_handler.setFormatter(formatter)

    print(f'Adding handler {new_handler}')
    app.logger.addHandler(new_handler)

    app.logger.info('msg="Starting up app..."')

    # Get configuration from config files or environment variables
    app.logger.info('msg="Loading configuration..."')
    app.config.from_object('config')
    app.config.from_pyfile('config.py', silent=True)

    # Update configuration from environment variables named as config keys
    for key in set(app.config.keys()).intersection(environ.keys()):
        env_key = string2bool(getenv(key), key=key)
        if env_key is not None:
            app.logger.info(f'msg="Overwriting {key} from environment variable"')
            app.config[key] = env_key

    # Update configuration from param
    app.config.update(config_final or {})

    # Lower logger level from DEBUG to INFO after config is loaded, if Debug mode is False
    if not app.config['DEBUG']:
        new_handler.level = logging.INFO

    # Convert string to int
    try:
        app.config['REQUEST_TIMEOUT'] = int(app.config['REQUEST_TIMEOUT'])
    except ValueError as err:
        app.logger.critical(f'msg="Error: ValueError setting REQUEST_TIMEOUT" err="{err}"')
        exit(1)
    except KeyError as err:
        app.logger.critical(f'msg="Error: KeyError setting REQUEST_TIMEOUT" err="{err}"')
        exit(1)
    app.logger.info(f"msg=\"app.config['REQUEST_TIMEOUT'] set to {app.config['REQUEST_TIMEOUT']}\"")

    # Display config variables
    # app.logger.info(app.config)

    # Check all required config variables
    for key in ['SERVER_NAME', 'PREFERRED_URL_SCHEME', 'REQUEST_TIMEOUT']:
        if app.config.get(key) is None:
            app.logger.critical(f'msg="Error: Required config variable not set" err="app.config[\'{key}\'] is None"')
            exit(1)

    app.register_blueprint(main)

    app.logger.info('DEBUG MODE is {0}'.format(app.debug))

    return app
