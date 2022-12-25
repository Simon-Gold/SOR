from flask import url_for
import pytest
import secrets
import uuid
import random
from unittest import mock
from datetime import datetime, timedelta
import unittest
import os
#  internals
from main import create_app, db
from config import Config
from models import Offender
from services import AuthService


class TestConfig(Config):
    SERVER_NAME = '127.0.0.1:5001'
    TESTING = True
    DISABLE_AUTH = True
    MONGODB_SETTINGS = [
        {
            "db": "test_db_sor",
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


    def setUp(self):
        db.disconnect("default")
        self.app = create_app(self.config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        #  drop previous existing data
        db.connection["default"].drop_database("test_db_sor")
        self.client = self.app.test_client()

    def tearDown(self):
        db.connection["default"].drop_database("test_db_sor")
        db.disconnect()
        self.app_context.pop()


class OffendersTests(BaseTestCase):
    """
    pytest -v tests/test_offender/test_views.py::OffendersTests -s --disable-warnings
    """
    config = TestConfigWithAuth

    def create_offenders(self):
        payload = {
            "addresses": [
                {
                    "line": ""
                }
            ],
            "names": [
                {
                    "first_name": "",
                    "last_name": "",
                    "middle": ""
                }
            ],
            "dob": {
                "year": 1980,
                "month": 1,
                "day": 1
            },
            "demographic": {
                "height": "4' 3\"",
                "race": "WHITE",
                "sex": "MALE",
                "weight": "145 Lbs."
            },
            "cases": [
                {
                    "case_number": "",
                    "charges": [
                        {
                            "description": "Abuse of Minor e",
                            "offense_date": "2012-3-15"
                        }
                    ]
                }
            ]
        }
        first_names = ["john", "joe"]
        last_names = ["captain", "capital"]
        address_lines = ["line1", "line2"]
        races = ["white", "american"]
        dobs = [{"year": 1991, "month": 8, "day": None},
                {"year": 1991, "month": 9, "day": 31}]
        for fn, ln, addr, dob in zip(first_names, last_names, address_lines, dobs):
            address_line = addr
            first_name = fn
            last_name = ln
            case_number = uuid.uuid4().hex
            race = random.choice(races)
            year = dob["year"]
            month = dob["month"]
            day = dob["day"]

            payload["addresses"][0]["line"] = address_line
            payload["names"][0]["first_name"] = first_name
            payload["names"][0]["last_name"] = last_name
            payload["dob"]["year"] = year
            payload["dob"]["month"] = month
            payload["dob"]["day"] = day
            payload["demographic"]["race"] = race
            payload["cases"][0]["case_number"] = case_number

            try:
                offender = Offender(**payload)
                offender.save()
            except:
                print("ERROR: ")
                print(payload)
                print()

    # def get_token(self, mock_get_access_token):
    #     import ipdb; ipdb.set_trace()
    #     username = os.environ.get("TEST_AUTH_USERNAME", "test")
    #     password = os.environ.get("TEST_AUTH_PASSWORD", "test")
    #     res = mock_get_access_token(username, password)
    #     self.access_token = res['access_token']
    #     self.refresh_token = res['refresh_token']
    #     self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def setUp(self):
        result = super().setUp()
        # self.get_token()
        self.create_offenders()
        return result

    # @pytest.mark.usefixtures("mock_is_authorized")
    def test_get_offender(self):
        offender = Offender.objects.first()
        correct_offender_id = str(offender.id)
        url = url_for('offenders.get_offender', id=correct_offender_id)
        # mocker.patch("services.AuthService.is_authorized", return_value=True)
        res = self.client.get(url)
        assert res.status_code == 200
        assert res.json["names"][0]["first_name"] == offender.names[0].first_name
        assert res.json["names"][0]["last_name"] == offender.names[0].last_name
        assert res.json["dob"]["year"] == offender.dob.year
        assert res.json["dob"]["month"] == offender.dob.month
        assert res.json["dob"]["day"] == offender.dob.day
        assert res.json["demographic"]["race"] == offender.demographic.race
        assert res.json["addresses"][0]["line"] == offender.addresses[0].line
        assert res.json["cases"][0]["case_number"] == offender.cases[0].case_number
        #  generate random 24 character hex string
        wrong_offender_id = secrets.token_hex(12)
        url = url_for('offenders.get_offender', id=wrong_offender_id)
        res = self.client.get(url, headers=self.headers)
        assert res.status_code == 404

    def test_get_offenders__pagination_fail_with_extreme_params(self):
        """
        Test pagination with extreme page number and page size (limit).
        There are only 2 records and 
            if we pass page number more than 2 it will raise 404
        """
        query_params = {"page": 1000}
        url = url_for('offenders.get_offenders')
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

    def test_search_offenders(self):
        query_params = {
            "last": "cap",
            "first": "",
            "dob": ""
        }
        url = url_for('offenders.search_offenders')
        res = self.client.get(url, headers=self.headers,
                              query_string=query_params)

        assert res.status_code == 200
        assert len(res.json) == Offender.objects.count()

        query_params = {
            "last": "cap",
            "first": "joe",
            "dob": ""
        }
        url = url_for('offenders.search_offenders')
        res = self.client.get(url, headers=self.headers,
                              query_string=query_params)

        assert res.status_code == 200
        assert len(res.json) == 1

        offender = Offender.objects.first()
        query_params = {
            "last": "cap",
            # "first": "joe",
            #  NOTE # Format month/day/year Example: 08/21/1990
            "dob": f"{offender.dob.month}/{offender.dob.day}/{offender.dob.year}"
        }
        url = url_for('offenders.search_offenders')
        res = self.client.get(url, headers=self.headers,
                              query_string=query_params)

        assert res.status_code == 200
        assert len(res.json) == 1

    def test_get_offenders__pagination(self):
        query_params = {
            "page": 1,
            "limit": 1
        }
        url = url_for('offenders.get_offenders')
        res = self.client.get(url, headers=self.headers,
                              query_string=query_params)
        assert res.status_code == 200
        next_page_param = f"page={2}"
        next_url = res.request.url.replace("page=1", next_page_param)
        assert res.json["next"] == next_url
        assert res.json["prev"] == None
        assert res.json["limit"] == query_params["limit"]
        assert res.json["current_page"] == query_params["page"]
        offender_objects_count = Offender.objects.count()
        assert res.json["total_items"] == offender_objects_count
        assert res.json["total_pages"] == offender_objects_count

    def test_get_offenders(self):
        url = url_for('offenders.get_offenders')
        res = self.client.get(url, headers=self.headers)
        assert res.status_code == 200
        assert res.json["current_page"] == 1
        assert res.json["limit"] == 10
        assert res.json["next"] != None
        assert res.json["prev"] == None
        assert res.json["total_pages"] == 1
        offender_objects_count = Offender.objects.count()
        assert res.json["total_items"] == offender_objects_count
        assert len(res.json["items"]) == offender_objects_count

    def test_create_offender(self):
        url = url_for('offenders.create_offender')
        payload = {
            "addresses": [{"line": "john street"}],
            "names": [{"first_name": "ally", "last_name": "captain", "middle": "jr"}],
            "dob": {"year": 1987, "month": 1, "day": 22},
            "demographic": {
                "height": "4' 3\"",
                "race": "AMERICAN OR ALASKAN NATIVE",
                "sex": "MALE",
                "weight": "135 Lbs."
            }
        }
        res = self.client.post(url, json=payload, headers=self.headers)
        assert res.status_code == 201
