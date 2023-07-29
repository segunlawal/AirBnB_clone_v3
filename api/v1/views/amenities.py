#!/usr/bin/python3
"""This module contains the Amenity view"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenites', strict_slashes=False)
def get_amenities():
    """Retrieves all Amenity objects"""
    amenities = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Retrieves an Amenity object by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """Deletes an Amenity object by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an Amenity object"""
    r = request.get_json()
    if not r:
        abort(400, "Not a JSON")
    if not r.get('name'):
        abort(400, "Missing name")
    obj = Amenity(**r)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    obj = storage.get(State, state_id)
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
