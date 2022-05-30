import os
from flask import request, Response
from functools import wraps
import jwt


os.environ["JWT_SECRET"] = "0cec2ac0c09602448541f423f31e5d4fc2c6e040"


def authorize(roles=[]):
    def _authorize(f):
        @wraps(f)
        def __authorize(*args, **kwargs):
            try:
                token1 = request.headers['Authorization'].split(" ")[1]
                # print(token)
                token2 = jwt.encode(
                    {"role": "admin"}, "0cec2ac0c09602448541f423f31e5d4fc2c6e040")
                print(token1 == token2)
                print(token1, type(token1))
                print(token2, type(token2))
                data = jwt.decode(
                    token2, "0cec2ac0c09602448541f423f31e5d4fc2c6e040", algorithms=['HS256'])
                if data["role"].lower() in roles:
                    return f(*args, **kwargs)
                else:
                    return Response("Role unauthorized", status=401, mimetype='application/json')

            except jwt.exceptions.ExpiredSignatureError:
                return Response("Token has expired", status=401, mimetype='application/json')
            except jwt.exceptions.InvalidSignatureError:
                return Response("Signature verification failed", status=401, mimetype='application/json')
            except Exception as e:
                raise e
                return Response("Unauthorized", status=401, mimetype='application/json')
        return __authorize
    return _authorize
