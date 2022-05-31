import os
from flask import render_template, request, Blueprint, redirect, url_for
from urllib.parse import urljoin
# from flask_login import LoginManager, login_required
# from flask_redis import FlaskRedis
# from .auth import auth as auth_bp, User, SECRET_KEY
from .code_exec import SchemaCodeExec
from .playground import SchemaSavePlayground, \
    DEFAULT_LANGUAGE, DEFAULT_LANG_BUFFERS, DEFAULT_EXECUTION_RESULT
from marshmallow import ValidationError

from .config import lang_to_host
from .middlewares.auth import authorize

import json
import redis
import requests
import uuid

THIRTY_DAYS = 60 * 60 * 24 * 30

rce = Blueprint("rce", __name__)

redis_read_client = redis.Redis(host='127.0.0.1', port=6379, db=0)
redis_write_client = redis.Redis(host='127.0.0.1', port=6379, db=0)


def do_code_exec(lang, code, tests):
    # addr = "http://%s-engine/api/run" % lang
    print(lang_to_host(lang))
    addr = "http://%s/api/run" % lang_to_host(lang)
    response = requests.post(addr, json={"code": code, "tests": tests})
    return response.json(), response.status_code


def do_lang_describe(run_lang_ip, lang):
    addr = "http://%s/api/describe/%s" % lang_to_host(lang)
    response = requests.get(addr)
    return response.json(), response.status_code


def gen_playground_id():
    # We'll fill up after 16^10 IDs, so this is more than fine for our scale.
    return uuid.uuid4().hex[0:10]


@rce.route('/')
# @login_required
def playground():
    return render_template(
        "playground.html",
        active_lang=DEFAULT_LANGUAGE, lang_buffers=DEFAULT_LANG_BUFFERS,
        execution_result=DEFAULT_EXECUTION_RESULT,
    )


@rce.route('/<pg_id>')
def saved_playground(pg_id=None):
    data = redis_read_client.get(pg_id)
    if data is None:
        return redirect(url_for('rce.playground'))

    data = json.loads(data)
    return render_template(
        "playground.html",
        active_lang=data["active_lang"],
        lang_buffers=json.dumps(data["lang_buffers"]),
        execution_result=json.dumps(data["execution_result"]),
    )


@rce.route('/api/save_playground', methods=['POST'])
def save_playground():
    json_data = request.get_json()
    if not json_data:
        return {"message": "Data must be JSON"}, 400
    try:
        data = SchemaSavePlayground().load(json_data)
    except ValidationError as err:
        return err.messages, 400

    pg_id = gen_playground_id()
    while redis_read_client.exists(pg_id) > 0:
        pg_id = gen_playground_id()

    redis_write_client.set(pg_id, json.dumps(data), ex=THIRTY_DAYS)
    return {"playgroundId": pg_id}, 200


@rce.route('/api/rce', methods=['POST'])
# @authorize(roles=["user"])
# @login_required
def remote_code_execution():
    json_data = request.get_json()
    if not json_data:
        return {"message": "Data must be JSON"}, 400
    try:
        data = SchemaCodeExec().load(json_data)
    except ValidationError as err:
        return err.messages, 400

    lang = data["lang"]
    code = data["code"]
    challenge_id = data["challenge_id"]
    r = requests.get(urljoin(os.environ.get("CONTENT_MANAGER_URL"), "/api/tests"),
                     json={"challenge_id": challenge_id})
    tests = r.json()
    # tests = [
    #     {
    #         "id": "test_id",
    #         "func_name": "add_",
    #         "inputs": [
    #             {"value": 2},
    #             {"value": 4}
    #         ],
    #         "expected": 6

    #     }
    # ]

    return do_code_exec(lang, code, tests)


@rce.route('/api/describe/<lang>', methods=['GET'])
# @login_required
def describe(lang=None):
    try:
        run_lang_ip = RUN_LANG_TABLE[lang]
    except KeyError:
        return {"message": "Language \"%s\" is not valid" % lang}, 400

    return do_lang_describe(run_lang_ip, lang)
