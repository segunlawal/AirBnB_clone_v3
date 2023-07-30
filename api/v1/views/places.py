#!/usr/bin/python3
"""This module contains the Place view"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Place
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """Retrieves all Place objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [obj.to_dict() for obj in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a Place object by its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """Deletes a Place object by its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    r = request.get_json()
    if not r:
        abort(400, "Not a JSON")
    if 'user_id' not in r:
        abort(400, 'Missing user_id')
    user = storage.get(User, r.get('user_id'))
    if not user:
        abort(404)
    if 'name' not in r:
        abort(400, 'Missing name')
    r.update({'city_id': city_id})
    obj = Place(**r)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    r = request.get_json()
    if not r:
        abort(400, 'Not a JSON')
    for key, value in r.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())
