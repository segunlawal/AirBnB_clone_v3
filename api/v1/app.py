#!/usr/bin/python3
"""This module contains a flask application"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(o):
    """Handles storage close"""
    storage.close()


@app.errorhandler(404)
def handle_error(error):
    """Handles 404 errors"""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default="0.0.0.0")
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host, port, threaded=True)
