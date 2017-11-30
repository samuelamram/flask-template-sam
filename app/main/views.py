import logging
from flask import jsonify
from . import main


@main.route('/')
@main.route('/hello')
def hello_world():
    logger = logging.getLogger()
    logger.info('Hello world')

    return jsonify('Hello world')
