#!/usr/bin/python3
"""Restful api actions for City"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """Get Cities"""
    state_ = storage.get(State, state_id)
    if state_ is None:
        abort(404)
    cities = []
    for city_ in state_.cities:
        cities.append(city_.to_dict())
    return jsonify(cities)


@app_views.route('/api/v1/cities/<city_id>', strict_slashes=False)
def get_cities_id(city_id):
    """Get city by id"""
    obj = storage.get(City, city_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_cities_id(city_id):
    """Delete state"""
    obj = storage.get(City, City_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_cities(state_id):
    """Post city"""
    if request.get_json():
        state_ = storage.get(State, state_id)
        if state_ is None:
            abort(404)
        if 'name' in request.get_json():
            city_ = City(**(request.get_json()))
            storage.new(city_)
            storage.save()
            return make_response(jsonify(city_.to_dict()), 201)
        else:
            return abort(400, 'Missing name')
    else:
        return abort(404, 'Not a JSON')


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city_id(city_id):
    """Put city"""
    ignore_values = ['id', 'created_at', 'updated_at']
    obj = storage.get(City, city_id)
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
