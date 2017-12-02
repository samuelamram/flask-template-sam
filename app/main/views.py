import logging
from flask import Blueprint, jsonify

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/hello')
def hello_world():
    logger = logging.getLogger()
    logger.info('Hello world')

    return jsonify({'Test': 'Hello world'})
