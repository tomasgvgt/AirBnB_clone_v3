#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State



@app_views.route('/states')
def get_states():
    states = []
    for  state in storage.all("State").values:
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>')
def get_states_id(state_id):
    object = storage.get(state_id)
     if object:
       return jsonify(object.to_dict())
     else
       return  abort(404)

@app_views.route('/states/<state_id>',  methods=["DELETE"])
def delete_states_id(state_id):
     object = storage.get(state_id)
     if object:
        storage.delete(object)
        return jsonify({}), 200
     else
        return  abort(404)


@app_views.route('/states', methods=['POST'])
def post_states():
    if request.json:
        if  'name'  in request.json:
            state = State(**(request.get_json))
            storage.new(state)
            storage.save()
            return state, 201
        else 
            return abort(400, 'Missing name')
    else:
        return abort(404, 'Not a JSON')

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state_id(state_id):
    ignore_values = ['id', 'created_at', 'updated_at']

    object = storage.get(State, state_id)
    if not object:
        return abort(400)
        
    if request.json:
        dictionary = request.get_json
        for k, v in dictionary.items();
            if k not in ingore_values:
                setattr(object,k ,v )
        object.save()
        return jsonify(object.to_dict), 200
    else:
        return abort(404, 'Not a JSON')
