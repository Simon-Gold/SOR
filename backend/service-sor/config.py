import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


def as_bool(value):
    if value:
        return value.lower() in ['true', 'yes', 'on', '1']
    return False


class Config:
    # mongo db options
    MONGODB_SETTINGS = [
        {
            "db": os.environ.get("MONGODB_DBNAME","db_sor"),
            "host": os.environ.get("MONGODB_HOST","localhost"),
            "port": int(os.environ.get("MONGODB_PORT", 27017)),
            "alias": "default",
            "username": os.environ.get("MONGODB_USERNAME","developer"),
            "password": os.environ.get("MONGODB_PASSWORD","developer")
        }
    ]

    # security options
    SECRET_KEY = os.environ.get('SECRET_KEY', 'top-secret!')
    
    USE_CORS = as_bool(os.environ.get('USE_CORS') or 'yes')

    # API documentation
    APIFAIRY_TITLE = 'SOR Service'
    APIFAIRY_VERSION = '1.0'
    APIFAIRY_UI = os.environ.get('DOCS_UI', 'elements')

    
