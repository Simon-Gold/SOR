from marshmallow import (validate, validates, validates_schema,
                         ValidationError, fields)
# from bson import ObjectId # TODO revisit
# internals
from api import marsh as ma
from api.auth.handlers import token_auth
from api.models import User

# ma.Schema.TYPE_MAPPING[ObjectId] = fields.String # TODO revisit


class UserSchema(ma.Schema):
    class Meta:
        ordered = True

    id = ma.String(unique=True, dump_only=True)
    full_name = ma.String(validate=validate.Length(
        min=3, max=64))  # TODO will remove
    first_name = ma.String(validate=validate.Length(min=3, max=64))
    last_name = ma.String(validate=validate.Length(min=3, max=64))
    username = ma.String(required=True,
                         validate=validate.Length(min=3, max=64))
    email = ma.String(required=True, validate=[validate.Length(max=120),
                                               validate.Email()])
    password = ma.String(required=True, load_only=True,
                         validate=validate.Length(min=3))
    is_superuser = ma.Boolean()
    is_active = ma.Boolean()
    created_date = ma.DateTime(dump_only=True)
    updated_date = ma.DateTime(dump_only=True)

    @validates('username')
    def validate_username(self, value):
        if not value[0].isalpha():
            raise ValidationError('Username must start with a letter')
        user = token_auth.current_user()
        old_username = user.username if user else None
        if value != old_username and User.objects(username=value):
            raise ValidationError('Use a different username.')

    @validates('email')
    def validate_email(self, value):
        user = token_auth.current_user()
        old_email = user.email if user else None
        if value != old_email and User.objects(username=value):
            raise ValidationError('Use a different email.')


class UpdateUserSchema(UserSchema):
    old_password = ma.String(load_only=True, validate=validate.Length(min=3))

    @validates('old_password')
    def validate_old_password(self, value):
        if not token_auth.current_user().verify_password(value):
            raise ValidationError('Password is incorrect')


class PasswordResetRequestSchema(ma.Schema):
    class Meta:
        ordered = True

    email = ma.String(required=True, validate=[validate.Length(max=120),
                                               validate.Email()])


class PasswordResetSchema(ma.Schema):
    class Meta:
        ordered = True

    token = ma.String(required=True)
    new_password = ma.String(required=True, validate=validate.Length(min=3))
