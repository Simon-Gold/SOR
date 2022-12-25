from functools import wraps
from flask import request, abort
#  internals
from services import AuthService


def auth_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token_val = request.headers.get("Authorization", None)
        if not token_val:
            return abort(401)

        token = token_val.split(" ")[1]

        if AuthService().is_authorized(token=token):
            return func(*args, **kwargs)
        return abort(401)

    return decorator
