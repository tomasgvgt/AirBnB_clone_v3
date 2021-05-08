#!/usr/bin/python3
"""Restful api actions for Amenity"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """Get Amenities"""
    amenities = []
    for amenity in storage.get(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenities_id(amenity_id):
    """Get city by id"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenities_id(amenity_id):
    """Delete state"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def post_amenities():
    """Post amenity"""
    if request.get_json():
        if request.get_json().get('name'):
            amenity_ = Amenity(**(request.get_json()))
            storage.new(amenity_)
            storage.save()
            return make_response(jsonify(amenity_.to_dict()), 201)
        else:
            return abort(400, 'Missing name')
    else:
        return abort(400, 'Not a JSON')


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity_id(amenity_id):
    """Put Amenity"""
    ignore_values = ['id', 'created_at', 'updated_at']
    obj = storage.get(Amenity, amenity_id)
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
