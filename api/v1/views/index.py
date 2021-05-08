#!/usr/bin/python3
"""Restful api status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def app_views_status():
    """restful api status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def retrieve_stats():
    """Restful api stats"""
    obj_stats = {}
    for k, v in classes.items():
        obj_stats[k] = storage.count(v)
    return jsonify(obj_stats)
