#!/usr/bin/python3
"""Restful api actions for Place"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """Get Places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_places_id(place_id):
    """Get place by id"""
    obj = storage.get(Place, place_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_places_id(city_id):
    """Delete place"""
    obj = storage.get(Place, place_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_places(state_id):
    """Post place"""
    if request.get_json():
        city_ = storage.get(City, city_id)
        if city_ is None:
            abort(404)
        if request.get_json().get('name') and request.get_json().get('user_id'):
            place_ = Place(**(request.get_json()))
            place_.city_id = city_.id
            storage.new(place_)
            storage.save()
            return make_response(jsonify(place_.to_dict()), 201)
        else:
            if request.get_json().get('name'):
                return abort(400, 'Missing name')
            if request.get_json().get('user_id'):
                return abort(400, 'Missing user_id')
    else:
        return abort(404, 'Not a JSON')


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place_id(place_id):
    """Put place"""
    ignore_values = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    obj = storage.get(Place, place_id)
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
