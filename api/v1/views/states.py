#!/usr/bin/python3
"""Restful api actions for State"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def get_states():
    """Get states"""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_states_id(state_id):
    """Get state by id"""
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_states_id(state_id):
    """Delete state"""
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """Post state"""
    if request.get_json():
        if 'name' in request.get_json():
            state = State(**(request.get_json()))
            storage.new(state)
            storage.save()
            return make_response(jsonify(state.to_dict()), 201)
        else:
            return abort(400, 'Missing name')
    else:
        return abort(404, 'Not a JSON')


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_id(state_id):
    """Put state"""
    ignore_values = ['id', 'created_at', 'updated_at']
    obj = storage.get(State, state_id)
    if not obj:
        return abort(400)
    if request.get_json():
        dictionary = request.get_json()
        for k, v in dictionary.items():
            if k not in ignore_values:
                setattr(obj, k, v)
        obj.save()
        return make_response(jsonify(obj.to_dict()), 200)
    else:
        return abort(404, 'Not a JSON')
