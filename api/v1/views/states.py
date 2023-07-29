#!/usr/bin/python3
"""This module contains the State view"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def get_states():
    """Retrieves all State objects"""
    states = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves a State object by its id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """Deletes a State object by its id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object"""
    r = request.get_json()
    if not r:
        abort(400, "Not a JSON")
    if not r.get('name'):
        abort(400, "Missing name")
    obj = State(**r)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
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
