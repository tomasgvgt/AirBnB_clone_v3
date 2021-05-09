#!/usr/bin/python3
"""Restful api actions for State"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    """Get users"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user_id(user_id):
    """Get user by id"""
    obj = storage.get(User, user_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_user_id(user_id):
    """Delete user"""
    obj = storage.get(User, user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """Post user"""
    if request.get_json():
        if 'name' in request.get_json():
            user = User(**(request.get_json()))
            storage.new(user)
            storage.save()
            return make_response(jsonify(user.to_dict()), 201)
        else:
            return abort(400, 'Missing name')
    else:
        return abort(404, 'Not a JSON')


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_id(user_id):
    """Put user"""
    ignore_values = ['id', 'created_at', 'updated_at']
    obj = storage.get(User, user_id)
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
