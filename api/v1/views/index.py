#!/usr/bin/python3
"""This module contains a route status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns JSON status of API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def retrieve_count():
    """Retrieves the number of each objects by type"""
    objs = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return jsonify(objs)
