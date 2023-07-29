#!/usr/bin/python3
"""This module contains a route status"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns JSON status of API"""
    return jsonify({"status": "OK"})
