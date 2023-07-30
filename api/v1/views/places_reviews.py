#!/usr/bin/python3
"""This module contains the Review view"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """Retrieves all Review objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [obj.to_dict() for obj in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """Retrieves a Review object by its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """Deletes a Review object by its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    r = request.get_json()
    if not r:
        abort(400, "Not a JSON")
    if 'user_id' not in r:
        abort(400, 'Missing user_id')
    user = storage.get(User, r.get('user_id'))
    if not user:
        abort(404)
    if 'text' not in r:
        abort(400, 'Missing text')
    r.update({'place_id': place_id})
    obj = Review(**r)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    r = request.get_json()
    if not r:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for key, value in r.items():
        if key not in ignore_keys:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())
