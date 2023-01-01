from flask_cors import CORS
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from apifairy import APIFairy
from flask_mongoengine import MongoEngine
# internals

db = MongoEngine()
cors = CORS()
mail = Mail()
marsh = Marshmallow()
apifairy = APIFairy()


