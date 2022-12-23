from datetime import datetime, timedelta
import secrets
from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import MongoEngine
from flask import current_app

# internals
from main import db


class User(db.Document):
    """Test model for AllFieldsModel and pagination."""

    username = db.StringField(max_length=60, unique=True)
    full_name = db.StringField(max_length=60)# TODO will remove
    first_name = db.StringField(max_length=60)
    last_name = db.StringField(max_length=60)
    email = db.EmailField(unique=True)
    is_superuser = db.BooleanField(default=False)
    is_active = db.BooleanField(default=True)

    created_date = db.DateTimeField(default=datetime.now)
    updated_date = db.DateTimeField(default=datetime.now)

    password = db.StringField(
        required=True,
        min_length=5,
    )
    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def verify_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def generate_auth_token(self):
        token = Token(user=self)
        token.generate()
        token.save()
        return token
    
    @staticmethod
    def verify_access_token(access_token, refresh_token=None):
        token = Token.objects(access_token=access_token).first()
        if token:
            return token.user

    @staticmethod
    def verify_refresh_token(refresh_token, access_token):
        token = Token.objects(refresh_token=refresh_token, access_token=access_token).first()
        if token:
            if token.refresh_expiration > datetime.utcnow():
                return token

            # someone tried to refresh with an expired token
            # revoke all tokens from this user as a precaution
            token.user.revoke_all()

    def revoke_all(self):
        Token.objects(user=self).delete()

    def generate_reset_token(self):
        return jwt.encode(
            {
                'exp': time() + current_app.config['RESET_TOKEN_MINUTES'] * 60,
                'reset_email': self.email,
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_token(reset_token):
        try:
            data = jwt.decode(reset_token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except jwt.PyJWTError:
            return
        return User.objects.get(email=data['reset_email'])



class Token(db.Document):
    """Test embedded for AllFieldsModel."""

    access_token = db.StringField(unique=True)
    refresh_token = db.StringField(unique=True)
    access_expiration = db.DateTimeField()
    refresh_expiration = db.DateTimeField()
    user = db.ReferenceField(document_type=User)


    def generate(self):
        self.access_token = secrets.token_urlsafe()
        self.access_expiration = datetime.utcnow() + \
            timedelta(minutes=current_app.config['ACCESS_TOKEN_MINUTES'])
        self.refresh_token = secrets.token_urlsafe()
        self.refresh_expiration = datetime.utcnow() + \
            timedelta(days=current_app.config['REFRESH_TOKEN_DAYS'])

    def expire(self, delay=None):
        if delay is None:  # pragma: no branch
            # 5 second delay to allow simultaneous requests
            delay = 5 if not current_app.testing else 0
        self.access_expiration = datetime.utcnow() + timedelta(seconds=delay)
        self.refresh_expiration = datetime.utcnow() + timedelta(seconds=delay)

    @staticmethod
    def clean():
        """Remove any tokens that have been expired for more than a day."""
        yesterday = datetime.utcnow() - timedelta(days=1)
        tokens = Token.objects(refresh_expiration__lt=yesterday)
        tokens.delete()
        
