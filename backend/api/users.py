from flask import Blueprint, jsonify, request, abort
from apifairy import authenticate, body, response, other_responses
from apifairy.exceptions import ValidationError

# internals
from api.models import User
from api.schemas import UserSchema, UpdateUserSchema, EmptySchema
from api.auth import token_auth


# globals
users = Blueprint('users', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
update_user_schema = UpdateUserSchema(partial=True)



@users.route('/users/', methods=['POST'])
@body(user_schema)
# @response(user_schema, 201)
# @other_responses({400: "Bad Request!"})
def create_user(args):
    user_data = request.get_json()
    password = user_data.pop("password")
    user = User(**user_data)
    user.set_password(password)
    user.save()
    return jsonify(user)
    

@users.route('/users/', methods=['GET'])
@authenticate(token_auth)
@response(users_schema)
def get_users():
    users = User.objects
    return users


@users.route('/users/me', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
def me():
    """Retrieve the authenticated user"""
    return token_auth.current_user()


@users.route('/users/<string:id>', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
@other_responses({404: 'User not found'})
def get(id):
    """Retrieve a user by id"""
    return User.objects(pk=id).first() or abort(404)


# @users.route('/me', methods=['PUT'])
# @authenticate(token_auth)
# @body(update_user_schema)
# @response(user_schema)
# def put(data):
#     """Edit user information"""
#     user = token_auth.current_user()
#     if 'password' in data and ('old_password' not in data or
#                                not user.verify_password(data['old_password'])):
#         abort(400)
#     # TODO
#     user.update(data)
#     return user
