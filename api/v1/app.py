#!/usr/bin/python3
"""
Blueprint for app
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def appcontext_error(error):
    """Teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Page not found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    if environ.get("HBNB_API_HOST"):
        host_ = environ.get("HBNB_API_HOST")
    else:
        host_ = "0.0.0.0"
    if environ.get("HBNB_API_PORT"):
        port_ = environ.get("HBNB_API_PORT")
    else:
        port_ = 5000
    app.run(host=host_, port=port_, threaded=True)
