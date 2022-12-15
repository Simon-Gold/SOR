from datetime import datetime, timedelta
from unittest import mock
import secrets
import pytest
from flask import url_for
# internals
from tests.base_test_case import BaseTestCase, TestConfigWithAuth
from api.models import User


class UsersTests(BaseTestCase):
    """
    pytest -v tests/test_user/test_views.py::UsersTests -s --disable-warnings
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
        result = super().setUp()
        self.create_token()
        return result

    def test_me(self):
        url = url_for('users.me')
        res = self.client.get(url, headers=self.headers)
        assert res.status_code == 200
        assert res.json["is_active"] == True
        assert res.json["username"] == self.user.username
        assert res.json["email"] == self.user.email

    def test_get_user__password_is_not_in_repsonse(self):
        correct_user_id = str(self.user.id)
        url = url_for('users.get_user', id=correct_user_id)
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
        url = url_for('users.get_user', id=correct_user_id)
        res = self.client.get(url, headers=self.headers)
        assert res.status_code == 200
        assert res.json["username"] == self.user.username
        assert res.json["email"] == self.user.email
        #  generate random 24 character hex string
        wrong_user_id = secrets.token_hex(12)
        url = url_for('users.get_user', id=wrong_user_id)
        res = self.client.get(url, headers=self.headers)
        assert res.status_code == 404

    def test_get_users__pagination_fail_with_extreme_params(self):
        """
        Test pagination with extreme page number and page size (limit).
        There are only 2 records and 
            if we pass page number more than 2 it will raise 404
        """
        query_params = {"page": 1000}
        url = url_for('users.get_users')
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
        url = url_for('users.get_users')
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
        url = url_for('users.get_users')
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
        url = url_for('users.create_user')
        payload = {
            "username": "myuser",
            "password": "qwert",
            "email": "myuser@example.com",
        }
        res = self.client.post(url, json=payload, headers=self.headers)
        assert res.status_code == 201

    def test_delete_user(self):
        url = url_for('users.create_user', id=self.user.id)
        payload = {
            "username": "tmp",
            "password": "qwert",
            "email": "tmp@example.com",
        }
        res = self.client.post(url, json=payload, headers=self.headers)
        assert res.status_code == 201
        # fetch user
        tmp_user = User.objects.get(username=payload["username"])
        url = url_for('users.delete_user', id=tmp_user.id)
        res = self.client.delete(url, headers=self.headers)
        assert res.status_code == 200
        assert res.json["id"] == str(tmp_user.id)

    def test_update_user__bad_request_duplicate_username(self):
        """ pytest -v tests/test_user/test_views.py::UsersTests::test_update_user__bad_request_duplicate_username -s --disable-warnings """
        url = url_for('users.update_user', id=self.user.id)
        # admin username is already taken
        payload = {"username": self.admin.username}
        res = self.client.patch(url, json=payload, headers=self.headers)
        assert res.status_code == 400

    def test_update_me(self):
        url = url_for('users.update_me')
        payload = {"is_superuser": True}
        res = self.client.patch(url, json=payload, headers=self.headers)
        assert res.status_code == 200

        payload = {"first_name": "tester", "last_name": "user"}
        res = self.client.put(url, json=payload, headers=self.headers)
        assert res.status_code == 200
        assert res.json["first_name"] == payload["first_name"]
        assert res.json["last_name"] == payload["last_name"]

    def test_update_user(self):
        url = url_for('users.update_user', id=self.user.id)
        payload = {"is_superuser": True}
        res = self.client.patch(url, json=payload, headers=self.headers)
        assert res.status_code == 200

        payload = {"first_name": "tester", "last_name": "user"}
        res = self.client.put(url, json=payload, headers=self.headers)
        assert res.status_code == 200
        assert res.json["first_name"] == payload["first_name"]
        assert res.json["last_name"] == payload["last_name"]

    def test_update_user__password_change(self):
        url = url_for('users.update_user', id=self.user.id)
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
