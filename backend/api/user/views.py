from flask import Blueprint, jsonify, request, abort
from apifairy import authenticate, body, response, other_responses
from apifairy.exceptions import ValidationError
from werkzeug.exceptions import NotFound

# internals
from api.models import User
from api.user.schemas import UserSchema, UpdateUserSchema
from api.auth.handlers import token_auth


# globals
bp_user = Blueprint('users', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
update_user_schema = UpdateUserSchema(partial=True)


@bp_user.route('/users/', methods=['POST'])
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


@bp_user.route('/users/', methods=['GET'])
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


@bp_user.route('/users/me', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
def me():
    """Retrieve the authenticated user"""
    return token_auth.current_user()


@bp_user.route('/users/<string:id>', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
@other_responses({404: 'User not found'})
def get(id):
    """Retrieve a user by id"""
    return User.objects(pk=id).first() or abort(404)


@bp_user.route("/users/<string:id>", methods=["DELETE"])
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


@bp_user.route('/users/<string:id>', methods=['PUT', 'PATCH'])
@authenticate(token_auth)
@body(update_user_schema)
@response(user_schema)
def update_user(data, id):
    """Edit other user information"""
    user = User.objects.get(id=id)
    password = data.pop("password")
    old_password = data.pop("old_password")
    if (password and (not old_password or not user.verify_password(old_password))):
        abort(400)
    user.update(**data)
    if password:
        user.set_password(password)
    user.save()
    user.reload()
    return user


@bp_user.route('/users/me', methods=['PUT'])
@authenticate(token_auth)
@body(update_user_schema)
@response(user_schema)
def update_me(data):
    """Edit user information"""
    user = token_auth.current_user()
    if 'password' in data and ('old_password' not in data or
                               not user.verify_password(data['old_password'])):
        abort(400)
    user.update(**data)
    user.save()
    user.reload()
    return user
