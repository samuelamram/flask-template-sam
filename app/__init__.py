from os import getenv
from time import sleep
import logging

from flask import Flask


app = Flask(__name__, instance_relative_config=True)

from . import views

# Get configuration from config files or environment variables
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

# Update configuration from environment variables
for key in app.config.keys():
    app.config[key] = getenv(key) or app.config[key]

for handler in app.logger.handlers:
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))

app.logger.info('Demarrage...')


