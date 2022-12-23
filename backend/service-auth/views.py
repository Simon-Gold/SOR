from flask import Blueprint, request, abort, current_app, url_for, jsonify
from werkzeug.http import dump_cookie
from apifairy import authenticate, body, response, other_responses
from werkzeug.exceptions import NotFound

#  internals
from handlers import basic_auth
from models import User, Token
from schemas import TokenSchema, UserSchema, UpdateUserSchema
from handlers import token_auth


bp_auth = Blueprint('auth', __name__)
token_schema = TokenSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)
update_user_schema = UpdateUserSchema(partial=True)


def token_response(token):
    headers = {}
    if current_app.config['REFRESH_TOKEN_IN_COOKIE']:
        samesite = 'strict'
        if current_app.config['USE_CORS']:  # pragma: no branch
            samesite = 'none' if not current_app.debug else 'lax'
        headers['Set-Cookie'] = dump_cookie(
            'refresh_token', token.refresh_token,
            path=url_for('auth.create_token'), secure=not current_app.debug,
            httponly=True, samesite=samesite)
    return {
        'access_token': token.access_token,
        'refresh_token': token.refresh_token
        if current_app.config['REFRESH_TOKEN_IN_BODY'] else None,
    }, 200, headers

@bp_auth.route("/", methods=["GET","HEAD"])
def health():
    return jsonify(message="It works!")

@bp_auth.route("/tokens/verify/", methods=["GET"])
def verify_token():
    """
    Verify received token from headers
    """
    try:
        tkn_val = request.headers.get("Authorization", None)
        if not tkn_val:
            abort(401)
        tkn = tkn_val.split(" ")[-1]
        token = Token.objects.get(access_token=tkn)
        return jsonify(response=True, token=token.access_token)
    except Token.DoesNotExist:
        abort(401)

@bp_auth.route('/tokens/', methods=['POST'])
@authenticate(basic_auth)
# @response(token_schema)
# @other_responses({401: 'Invalid username or password'})
def create_token():
    """Create new access and refresh tokens

    The refresh token is returned in the body of the request or as a hardened
    cookie, depending on configuration. A cookie should be used when the
    client is running in an insecure environment such as a web browser, and
    cannot adequately protect the refresh token against unauthorized access.
    """
    user = basic_auth.current_user()
    token = user.generate_auth_token()
    token.clean()  # keep token table clean of old tokens
    return token_response(token)


@bp_auth.route('/users/', methods=['POST'])
@body(user_schema)
@response(user_schema, 201)
@other_responses({400: "Bad Request!"})
def create_user(args):
    """Create a new user"""
    user_data = request.get_json()
    password = user_data.pop("password")
    user = User(**user_data)
    user.set_password(password)
    user.save()
    return user


@bp_auth.route('/users/', methods=['GET'])
@authenticate(token_auth)
# @response(users_schema)
def get_users():
    """Get all users"""
    PAGE = 1
    PAGE_LIMIT = 10
    page = request.args.get("page") or PAGE
    limit = request.args.get("limit") or PAGE_LIMIT
    try:
        po = User.objects.paginate(page=int(page), per_page=int(limit))
        response = jsonify({
            "next": f"{request.base_url}?page={po.next_num}&limit={po.per_page}",
            "prev": f"{request.base_url}?page={po.prev_num}&limit={po.per_page}" if po.has_prev else None,
            "current_page": po.page,
            "limit": po.per_page,
            "total_items": po.total,
            "total_pages": po.pages,
            "items": users_schema.dump(po.items),
        })
        return response
    except NotFound:
        return abort(404)


@bp_auth.route('/users/me', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
def me():
    """Retrieve the authenticated user"""
    return token_auth.current_user()


@bp_auth.route('/users/<string:id>', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
@other_responses({404: 'User not found'})
def get_user(id):
    """Retrieve a user by id"""
    return User.objects(pk=id).first() or abort(404)


@bp_auth.route("/users/<string:id>", methods=["DELETE"])
@authenticate(token_auth)
@other_responses({404: "User Not Found"})
def delete_user(id):
    """Delete an user by id"""
    try:
        user = User.objects.get(pk=id)
        user.delete()
        msg = {
            "message": "User is deleted successfully",
            "id": id
        }
        response = jsonify(msg)
        return response
    except User.DoesNotExist:
        return abort(404)


@bp_auth.route('/users/<string:id>', methods=['PUT', 'PATCH'])
@authenticate(token_auth)
@body(update_user_schema)
@response(user_schema)
def update_user(data, id):
    """Edit other user information"""
    try:
        user = User.objects.get(id=id)
        password = data.pop("password", None)
        old_password = data.pop("old_password", None)
        if (password and (not old_password or not user.verify_password(old_password))):
            abort(400)
        if data:
            user.update(**data)
        if password:
            user.set_password(password)
    except Exception as e:
        raise e
    else:
        user.save()
        user.reload()
        return user


@bp_auth.route('/users/me', methods=['PUT', 'PATCH'])
@authenticate(token_auth)
@body(update_user_schema)
@response(user_schema)
def update_me(data):
    """Edit user information"""
    try:
        user = token_auth.current_user()
        password = data.pop("password", None)
        old_password = data.pop("old_password", None)
        if (password and (not old_password or not user.verify_password(old_password))):
            abort(400)
        if data:
            user.update(**data)
        if password:
            user.set_password(password)
    except Exception as e:
        raise e
    else:
        user.save()
        user.reload()
        return user
