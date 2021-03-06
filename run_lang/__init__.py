from flask import Flask, request, jsonify, Blueprint
from .execute import execute
from .describe import get_ubuntu, get_description, get_packages


bp = Blueprint("rce", __name__)


@bp.route('/api/run', methods=['POST'])
def playground():
    json_data = request.get_json()
    if not json_data:
        return {"message": "Data must be JSON"}, 400
    try:
        code = json_data["code"]
        tests = json_data["tests"]
        func_name = json_data["func_name"]
    except KeyError:
        return {"message": "Key \"code\" or \"tests\" are not present"}, 400

    result = execute(code, func_name, tests)
    return jsonify(result), 200


@bp.route('/api/describe', methods=['GET'])
def describe():
    return jsonify({
        "ubuntu": get_ubuntu(),
        "description": get_description(),
        "packages": get_packages(),
    })


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    return app
