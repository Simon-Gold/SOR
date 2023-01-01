import os
import json
import requests
from requests.auth import HTTPBasicAuth

from flask import abort, jsonify


class AuthService(object):

    def __init__(self):
        self.AUTH_SERVICE_HOST = os.environ.get(
            "AUTH_SERVICE_HOST", "localhost")
        self.AUTH_SERVICE_PORT = os.environ.get("AUTH_SERVICE_PORT", "5000")
        self.API_PREFIX = os.environ.get("API_PREFIX", "api/v1")
        self.AUTH_ENDPOINT = os.environ.get("AUTH_ENDPOINT", "tokens/verify/")
        self.AUTH_SERVICE_PROTOCOL = os.environ.get(
            "AUTH_SERVICE_PROTOCOL", "http")

    def is_authorized(self, token):
        headers = {"Authorization": f"Bearer {token}"}
        url = "{}://{}:{}/{}/{}".format(
            self.AUTH_SERVICE_PROTOCOL,
            self.AUTH_SERVICE_HOST,
            self.AUTH_SERVICE_PORT,
            self.API_PREFIX,
            self.AUTH_ENDPOINT
        )
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
        return False

    def get_access_token(self, username, password):
        url = "{}://{}:{}/{}/{}".format(
            self.AUTH_SERVICE_PROTOCOL,
            self.AUTH_SERVICE_HOST,
            self.AUTH_SERVICE_PORT,
            self.API_PREFIX,
            self.AUTH_ENDPOINT
        )
        res = requests.post(
            url, auth=HTTPBasicAuth(username=username, password=password)
        )
        if res.status_code == 200:
            return jsonify(access_token=res.get("access_token"))
        return abort(401)

    def get_user(self, token):
        pass
