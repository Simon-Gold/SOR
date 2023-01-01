import pytest
# internals
from services import AuthService


class MockAuthService():

    @staticmethod
    def is_authorized():
        return True

    @staticmethod
    def get_access_token():
        return {
            "access_token": "abcd",
            "refresh_token": "defg",
        }

@pytest.fixture(scope="class")
def mock_is_authorized(monkeypatch):
    def is_authorized(*args, **kwargs):
        return MockAuthService()
    #  we replaced actual AuthService.is_authorized behaviour with our custom is_authorized
    monkeypatch.setattr(AuthService, "is_authorized", is_authorized)


@pytest.fixture(scope="function")
def mock_get_access_token(monkeypatch):
    """
    mp: monkeypatch abbreviation
    """
    def get_access_token(*args, **kwargs):
        return MockAuthService()

    monkeypatch.setattr(AuthService, "get_access_token", get_access_token)