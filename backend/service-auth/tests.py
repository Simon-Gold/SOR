from flask import url_for
from unittest import mock
from datetime import datetime, timedelta
import unittest
import pytest
import secrets
import os
#  internals
from main import create_app, db
from config import Config
from models import User


class TestConfig(Config):
    SERVER_NAME = '127.0.0.1:5000'
    TESTING = True
    DISABLE_AUTH = True
    MONGODB_SETTINGS = [
        {
            "db": "test_db_auth",
            "host": "localhost",
            "port": 27017,
            "alias": "default",
            "username": "developer",
            "password": "developer",
            "connect": False,
        }
    ]


class TestConfigWithAuth(TestConfig):
    DISABLE_AUTH = False
    REFRESH_TOKEN_IN_BODY = True


class BaseTestCase(unittest.TestCase):
    """ pytest -s """
    config = TestConfig
    url_prefix = "/api/v1"

    def create_user(self):
        self.user = User(username="test", email="test@example.com")
        self.user.set_password("test")
        self.user.save()
        self.admin = User(username="admin", email="admin@example.com")
        self.admin.set_password("admin")
        self.admin.save()

    def setUp(self):
        db.disconnect("default")
        #  create flask app
        self.app = create_app(self.config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        #  drop previous existing data
        self.create_user()
        self.client = self.app.test_client()

    def tearDown(self):
        db.connection["default"].drop_database("test_db_auth")
        db.disconnect()
        self.app_context.pop()


class AuthTests(BaseTestCase):
    config = TestConfigWithAuth

    def create_token(self):
        url = url_for('auth.create_token')
        res = self.client.post(url, auth=('test', 'test'))
        assert res.status_code == 200
        self.access_token = res.json['access_token']
        self.refresh_token = res.json['refresh_token']

    def setUp(self):
        result = super().setUp()
        self.create_token()
        return result

    def test_no_auth(self):
        url = url_for('auth.me')
        res = self.client.get(url)
        assert res.status_code == 401

    def test_create_token(self):
        url = url_for("auth.create_token")
        res = self.client.post(url, auth=('test', 'test'))
        assert res.status_code == 200
        access_token = res.json['access_token']
        assert access_token != None
        refresh_token = res.json['refresh_token']
        assert refresh_token != None

    def test_get_users__with_token(self):
        url = url_for("auth.get_users")
        headers = {'Authorization': f'Bearer {self.access_token}'}
        res = self.client.get(url, headers=headers)
        assert res.status_code == 200
        res_json = res.json
        """
        NOTE Example response data
        {
            "current_page": 1,
            "items": [
                {
                    "created_date": "2022-11-26T16:25:47.978000",
                    "email": "test@example.com",
                    "first_name": "dev",
                    "full_name": null,
                    "id": "63823e0cdfb94fd0bfaa0910",
                    "is_active": true,
                    "is_superuser": false,
                    "last_name": "developer",
                    "updated_date": "2022-11-26T16:25:47.978000",
                    "username": "test"
                }
            ],
            "limit": 10,
            "next": "http://127.0.0.1:5000/api/v1/users/?page=2&limit=10",
            "prev": null,
            "total_items": 1,
            "total_pages": 1
        }
        """
        assert res_json['items'][0]['username'] == 'test'

    def test_get_users__with_wrong_token(self):
        url = url_for("auth.get_users")
        res = self.client.get(url, headers={
            'Authorization': f'Bearer {self.access_token + "x"}'})
        assert res.status_code == 401

    def test_get_users__with_refresh_token(self):
        url = url_for("auth.get_users")
        res = self.client.get(url, headers={
            'Authorization': f'Bearer {self.refresh_token}'})
        assert res.status_code == 401


class UsersTests(BaseTestCase):
    """
    pytest -v tests.py::UsersTests -s --disable-warnings
    """
    config = TestConfigWithAuth

    def create_token(self):
        url = url_for('auth.create_token')
        res = self.client.post(url, auth=('test', 'test'))
        assert res.status_code == 200
        self.access_token = res.json['access_token']
        self.refresh_token = res.json['refresh_token']
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def setUp(self):
        try:
            result = super().setUp()
            self.create_token()
            return result
        except:
            db.connection["default"].drop_database("test_db_auth")

    def test_me(self):
        url = url_for('auth.me')
        res = self.client.get(url, headers=self.headers)
        assert res.status_code == 200
        assert res.json["is_active"] == True
        assert res.json["username"] == self.user.username
        assert res.json["email"] == self.user.email

    def test_get_user__password_is_not_in_repsonse(self):
        correct_user_id = str(self.user.id)
        url = url_for('auth.get_user', id=correct_user_id)
        res = self.client.get(url, headers=self.headers)
        assert res.status_code == 200
        assert res.json["username"] == self.user.username
        assert res.json["email"] == self.user.email
        #  1. way of checking password is not in the response
        assert res.json.get("password") == None
        #  2. way of checking password is not in the response
        with pytest.raises(KeyError):
            assert res.json["password"] != None

    def test_get_user(self):
        correct_user_id = str(self.user.id)
        url = url_for('auth.get_user', id=correct_user_id)
        res = self.client.get(url, headers=self.headers)
        assert res.status_code == 200
        assert res.json["username"] == self.user.username
        assert res.json["email"] == self.user.email
        #  generate random 24 character hex string
        wrong_user_id = secrets.token_hex(12)
        url = url_for('auth.get_user', id=wrong_user_id)
        res = self.client.get(url, headers=self.headers)
        assert res.status_code == 404

    def test_get_users__pagination_fail_with_extreme_params(self):
        """
        Test pagination with extreme page number and page size (limit).
        There are only 2 records and 
            if we pass page number more than 2 it will raise 404
        """
        query_params = {"page": 1000}
        url = url_for('auth.get_users')
        res = self.client.get(url, headers=self.headers,
                              query_string=query_params)
        assert res.status_code == 404
        #  if we give only limit parameter the response is 200
        query_params = {"limit": 1000}
        res = self.client.get(url, headers=self.headers,
                              query_string=query_params)
        assert res.status_code == 200
        #  if we give extreme limit with page number, both of these cause out of scope for objects
        query_params = {"limit": 1000, "page": 2}
        res = self.client.get(url, headers=self.headers,
                              query_string=query_params)
        assert res.status_code == 404

    def test_get_users__pagination(self):
        query_params = {
            "page": 1,
            "limit": 1
        }
        url = url_for('auth.get_users')
        res = self.client.get(url, headers=self.headers,
                              query_string=query_params)
        assert res.status_code == 200
        next_page_param = f"page={2}"
        next_url = res.request.url.replace("page=1", next_page_param)
        assert res.json["next"] == next_url
        assert res.json["prev"] == None
        assert res.json["limit"] == query_params["limit"]
        assert res.json["current_page"] == query_params["page"]
        user_objects_count = User.objects.count()
        assert res.json["total_items"] == user_objects_count
        assert res.json["total_pages"] == user_objects_count

    def test_get_users(self):
        url = url_for('auth.get_users')
        res = self.client.get(url, headers=self.headers)
        assert res.status_code == 200
        assert res.json["current_page"] == 1
        assert res.json["limit"] == 10
        assert res.json["next"] != None
        assert res.json["prev"] == None
        assert res.json["total_pages"] == 1
        user_objects_count = User.objects.count()
        assert res.json["total_items"] == user_objects_count
        assert len(res.json["items"]) == user_objects_count

    def test_create_user(self):
        url = url_for('auth.create_user')
        payload = {
            "username": "myuser",
            "password": "qwert",
            "email": "myuser@example.com",
        }
        res = self.client.post(url, json=payload, headers=self.headers)
        assert res.status_code == 201

    def test_delete_user(self):
        url = url_for('auth.create_user', id=self.user.id)
        payload = {
            "username": "tmp",
            "password": "qwert",
            "email": "tmp@example.com",
        }
        res = self.client.post(url, json=payload, headers=self.headers)
        assert res.status_code == 201
        # fetch user
        tmp_user = User.objects.get(username=payload["username"])
        url = url_for('auth.delete_user', id=tmp_user.id)
        res = self.client.delete(url, headers=self.headers)
        assert res.status_code == 200
        assert res.json["id"] == str(tmp_user.id)

    def test_update_user__bad_request_duplicate_username(self):
        """ pytest -v tests/test_user/test_views.py::UsersTests::test_update_user__bad_request_duplicate_username -s --disable-warnings """
        url = url_for('auth.update_user', id=self.user.id)
        # admin username is already taken
        payload = {"username": self.admin.username}
        res = self.client.patch(url, json=payload, headers=self.headers)
        assert res.status_code == 400

    def test_update_me(self):
        url = url_for('auth.update_me')
        payload = {"is_superuser": True}
        res = self.client.patch(url, json=payload, headers=self.headers)
        assert res.status_code == 200

        payload = {"first_name": "tester", "last_name": "user"}
        res = self.client.put(url, json=payload, headers=self.headers)
        assert res.status_code == 200
        assert res.json["first_name"] == payload["first_name"]
        assert res.json["last_name"] == payload["last_name"]

    def test_update_user(self):
        url = url_for('auth.update_user', id=self.user.id)
        payload = {"is_superuser": True}
        res = self.client.patch(url, json=payload, headers=self.headers)
        assert res.status_code == 200

        payload = {"first_name": "tester", "last_name": "user"}
        res = self.client.put(url, json=payload, headers=self.headers)
        assert res.status_code == 200
        assert res.json["first_name"] == payload["first_name"]
        assert res.json["last_name"] == payload["last_name"]

    def test_update_user__password_change(self):
        url = url_for('auth.update_user', id=self.user.id)
        payload = {"password": "qwert"}
        # old_password is needed
        res = self.client.put(url, json=payload, headers=self.headers)
        assert res.status_code == 400

        payload = {
            "password": "qwert",
            "old_password": "test"
        }
        res = self.client.put(url, json=payload, headers=self.headers)
        assert res.status_code == 200
