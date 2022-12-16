import unittest
import os
# internals
from api.app import create_app, db
from config import Config
from api.models import User

class TestConfig(Config):
    SERVER_NAME = '127.0.0.1:5000'
    TESTING = True
    DISABLE_AUTH = True
    MONGODB_SETTINGS = [
        {
            "db":"test_db_sor",
            "host":"localhost",
            "port": 27017,
            "alias": "default",
            "username":"developer",
            "password":"developer",
            # "connect":False, # NOTE not necessary will be removed
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
        self.app = create_app(self.config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        # drop previous existing data
        db.connection["default"].drop_database("test_db_sor")
        self.create_user()
        self.client = self.app.test_client()

    def tearDown(self):
        db.connection["default"].drop_database("test_db_sor")
        db.disconnect()
        self.app_context.pop()
