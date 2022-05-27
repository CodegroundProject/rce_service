import connexion
from flask import jsonify


def get():
    return jsonify({}), 200


def search():
    return get()


def post():
    if connexion.request.is_json:
        data = connexion.request.get_json()
        return jsonify(data)
    return jsonify({})
