from flask import Flask, request, jsonify, Blueprint
from run_lang.services.execute import execute
from run_lang.services.describe import get_ubuntu, get_description

bp = Blueprint("rce", __name__)

@bp.route('/run', methods=['POST'])
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


@bp.route('/describe', methods=['GET'])
def describe():
    return jsonify({
        "ubuntu": get_ubuntu(),
        "description": get_description(),
    })


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    return app
