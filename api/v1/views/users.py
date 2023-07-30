#!/usr/bin/python3
"""This module contains the User view"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False)
def get_users():
    """Retrieves all User objects"""
    users = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves a User object by its id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """Deletes a User object by its id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object"""
    r = request.get_json()
    if not r:
        abort(400, "Not a JSON")
    if not r.get('email'):
        abort(400, "Missing email")
    if not r.get('password'):
        abort(400, "Missing password")
    obj = User(**r)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    r = request.get_json()
    if not r:
        abort(400, 'Not a JSON')
    for key, value in r.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())
