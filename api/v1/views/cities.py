#!/usr/bin/python3
"""This module contains the City view"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [obj.to_dict() for obj in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieves a City object by its id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """Deletes a City object by its id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City object"""
    r = request.get_json()
    if not r:
        abort(400, "Not a JSON")
    if not r.get('name'):
        abort(400, "Missing name")
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    r.update({'state_id': state_id})
    city = City(**r)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    r = request.get_json()
    if not r:
        abort(400, 'Not a JSON')
    for key, value in r.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())
