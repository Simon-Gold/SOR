from datetime import datetime, timedelta
from unittest import mock
from flask import url_for
from tests.base_test_case import BaseTestCase, TestConfigWithAuth


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
        url = url_for('users.me')
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
        url = url_for("users.get_users")
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
        url = url_for("users.get_users")
        res = self.client.get(url, headers={
            'Authorization': f'Bearer {self.access_token + "x"}'})
        assert res.status_code == 401

    def test_get_users__with_refresh_token(self):
        url = url_for("users.get_users")
        res = self.client.get(url, headers={
            'Authorization': f'Bearer {self.refresh_token}'})
        assert res.status_code == 401


"""

    def test_get_token_in_cookie_only(self):
        self.app.config['REFRESH_TOKEN_IN_COOKIE'] = True
        self.app.config['REFRESH_TOKEN_IN_BODY'] = False
        res = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert res.status_code == 200
        assert res.json['refresh_token'] is None
        assert res.headers['Set-Cookie'].startswith('refresh_token=')

    def test_get_token_in_body_only(self):
        self.app.config['REFRESH_TOKEN_IN_COOKIE'] = False
        self.app.config['REFRESH_TOKEN_IN_BODY'] = True
        res = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert res.status_code == 200
        assert res.json['refresh_token'] is not None
        assert 'Set-Cookie' not in res.headers

    def test_token_expired(self):
        res = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert res.status_code == 200
        access_token = res.json['access_token']

        with mock.patch('api.models.datetime') as dt:
            dt.utcnow.return_value = datetime.utcnow() + timedelta(days=1)
            res = self.client.get('/api/users', headers={
                'Authorization': f'Bearer {access_token}'})
            assert res.status_code == 401

    def test_refresh_token(self):
        res = self.client.post('/api/tokens', auth=('test@example.com', 'foo'))
        assert res.status_code == 200
        access_token1 = res.json['access_token']
        refresh_token1 = res.json['refresh_token']

        res = self.client.put(
            '/api/tokens', json={'access_token': access_token1},
            headers={'Cookie': 'refresh_token=' + refresh_token1})
        assert res.status_code == 200
        assert res.json['access_token'] != access_token1
        assert res.json['refresh_token'] != refresh_token1
        access_token2 = res.json['access_token']

        res = self.client.get('/api/users', headers={
            'Authorization': f'Bearer {access_token2}'})
        assert res.status_code == 200
        assert res.json['data'][0]['username'] == 'test'

        res = self.client.get('/api/users', headers={
            'Authorization': f'Bearer {access_token1}'})
        assert res.status_code == 401

    def test_refresh_token_failure(self):
        res = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert res.status_code == 200
        access_token = res.json['access_token']
        refresh_token = res.json['refresh_token']

        self.client.cookie_jar.clear()
        res = self.client.put('/api/tokens', json={
            'access_token': access_token})
        assert res.status_code == 401
        res = self.client.put('/api/tokens', json={
            'access_token': access_token,
            'refresh_token': refresh_token + 'x',
        })
        res = self.client.put('/api/tokens', json={
            'access_token': access_token + 'x',
            'refresh_token': refresh_token,
        })
        assert res.status_code == 401

    def test_refresh_revoke_all(self):
        res = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert res.status_code == 200
        access_token1 = res.json['access_token']
        refresh_token1 = res.json['refresh_token']

        res = self.client.get('/api/users', headers={
            'Authorization': f'Bearer {access_token1}'})
        assert res.status_code == 200

        res = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert res.status_code == 200
        access_token2 = res.json['access_token']
        refresh_token2 = res.json['refresh_token']

        res = self.client.put('/api/tokens', json={
            'access_token': access_token2})
        assert res.status_code == 200
        access_token3 = res.json['access_token']
        refresh_token3 = res.json['refresh_token']

        res = self.client.put('/api/tokens', json={
            'access_token': access_token2,
            'refresh_token': refresh_token2})
        assert res.status_code == 401  # duplicate refresh

        res = self.client.get('/api/users', headers={
            'Authorization': f'Bearer {access_token1}'})
        assert res.status_code == 401
        res = self.client.get('/api/users', headers={
            'Authorization': f'Bearer {access_token2}'})
        assert res.status_code == 401
        res = self.client.get('/api/users', headers={
            'Authorization': f'Bearer {access_token3}'})
        assert res.status_code == 401

        res = self.client.put('/api/tokens', json={
            'access_token': access_token1,
            'refresh_token': refresh_token1})
        assert res.status_code == 401
        res = self.client.put('/api/tokens', json={
            'access_token': access_token2,
            'refresh_token': refresh_token2})
        assert res.status_code == 401
        res = self.client.put('/api/tokens', json={
            'access_token': access_token3,
            'refresh_token': refresh_token3})
        assert res.status_code == 401

    def test_revoke(self):
        res = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert res.status_code == 200
        access_token = res.json['access_token']

        res = self.client.get('/api/users', headers={
            'Authorization': f'Bearer {access_token}'})
        assert res.status_code == 200

        res = self.client.delete('/api/tokens', headers={
            'Authorization': f'Bearer {access_token}'})
        assert res.status_code == 204

        res = self.client.get('/api/users', headers={
            'Authorization': f'Bearer {access_token}'})
        assert res.status_code == 401

    def test_no_login(self):
        res = self.client.post('/api/tokens')
        assert res.status_code == 401

    def test_bad_login(self):
        res = self.client.post('/api/tokens', auth=('test', 'bar'))
        assert res.status_code == 401

    def test_reset_password(self):
        with mock.patch('api.tokens.send_email') as send_email:
            res = self.client.post('/api/tokens/reset', json={
                'email': 'bad@example.com',
            })
            assert res.status_code == 204
            res = self.client.post('/api/tokens/reset', json={
                'email': 'test@example.com',
            })
            assert res.status_code == 204
        send_email.assert_called_once()
        assert send_email.call_args[0] == (
            'test@example.com', 'Reset Your Password', 'reset')
        reset_token = send_email.call_args[1]['token']
        reset_url = send_email.call_args[1]['url']
        assert reset_url == 'http://localhost:3000/reset?token=' + reset_token

        res = self.client.put('/api/tokens/reset', json={
            'token': reset_token + 'x',
            'new_password': 'bar'
        })
        assert res.status_code == 400

        res = self.client.put('/api/tokens/reset', json={
            'token': reset_token,
            'new_password': 'bar'
        })
        assert res.status_code == 204

        res = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert res.status_code == 401

        res = self.client.post('/api/tokens', auth=('test', 'bar'))
        assert res.status_code == 200

"""
