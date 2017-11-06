from flask import jsonify
from app import app


@app.route('/')
def hello_world():
    app.logger.info('Hello world')

    return jsonify('Hello world')
