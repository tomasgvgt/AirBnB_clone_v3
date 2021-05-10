#!/usr/bin/python3
"""Restful api actions for City"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.city import City


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """Get reviews"""
    place_ = storage.get(Place, place_id)
    if place_ is None:
        abort(404)
    reviews = []
    for review_ in place_.reviews:
        reviews.append(review_.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_reviews_id(review_id):
    """Get review by id"""
    obj = storage.get(Review, review_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_review_id(review_id):
    """Delete review"""
    obj = storage.get(Review, review_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Post review"""
    if request.get_json():
        place_ = storage.get(Place, place_id)
        if place_ is None:
            abort(404)
        request_ = request.get_json()

        # check user
        user_id_check = request_.get('user_id')
        if user_id_check:
            user_ = storage.get(User, user_id_check)
        else:
            abort(404)

        user_ = storage.get(User, user_id_check)
        
        if request_.get('user_id') and request_.get('text'):
            review_ = Review(**(request_))
            review_.state_id = place_.id
            storage.new(review_)
            storage.save()
            return make_response(jsonify(review_.to_dict()), 201)
        else:
            if request_.get('user_id') is None:
                return abort(400, 'Missing user_id')
            if request_.get('text') is None:
                return abort(400, 'Missing text')

    else:
        return abort(404, 'Not a JSON')


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review_id(review_id):
    """Put review"""
    ignore_values = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    obj = storage.get(Review, review_id)
    if not obj:
        return abort(404)
    if request.get_json():
        dictionary = request.get_json()
        for k, v in dictionary.items():
            if k not in ignore_values:
                setattr(obj, k, v)
        obj.save()
        return make_response(jsonify(obj.to_dict()), 200)
    else:
        return abort(400, 'Not a JSON')
