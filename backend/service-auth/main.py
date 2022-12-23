from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from apifairy import APIFairy
from flask_mongoengine import MongoEngine
# internals
from config import Config

db = MongoEngine()
cors = CORS()
mail = Mail()
marsh = Marshmallow()
apifairy = APIFairy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # extensions
    db.init_app(app)

    # api documentation
    apifairy.init_app(app)

    # serialization/deserialization Marshmellow
    marsh.init_app(app)
    from bson import ObjectId
    marsh.Schema.TYPE_MAPPING[ObjectId] = marsh.String

    # Mail
    mail.init_app(app)
    # CORS
    if app.config['USE_CORS']:  # pragma: no branch
        cors.init_app(app, origins="*")

    # blueprints
    API_URL_PREFIX = "/api/v1"
    from errors import errors
    app.register_blueprint(errors)
    from views import bp_auth
    app.register_blueprint(bp_auth, url_prefix=API_URL_PREFIX)

    @app.route('/')
    def index():  # pragma: no cover
        return redirect(url_for('apifairy.docs'))

    @app.after_request
    def after_request(response):
        # Werkzeu sometimes does not flush the request body so we do it here
        request.get_data()
        return response

    return app


#  CREATE APP
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
