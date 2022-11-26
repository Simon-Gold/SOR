from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from apifairy import APIFairy
# internals
from config import Config


cors = CORS()
mail = Mail()
marsh = Marshmallow()
apifairy = APIFairy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # extensions
    

    from api import models
    models.db.init_app(app)

    # api documentation
    apifairy.init_app(app)

    # serialization/deserialization Marshmellow
    marsh.init_app(app)
    # Mail
    mail.init_app(app)
    # CORS
    if app.config['USE_CORS']:  # pragma: no branch
        cors.init_app(app)

    # blueprints
    API_URL_PREFIX = "/api/v1"
    from api.errors import errors
    app.register_blueprint(errors)
    from api.tokens import tokens
    app.register_blueprint(tokens, url_prefix=API_URL_PREFIX)
    from api.users import users
    app.register_blueprint(users, url_prefix=API_URL_PREFIX)
    from api.offender.views import offenders
    app.register_blueprint(offenders, url_prefix=API_URL_PREFIX)

    # define the shell context
    # @app.shell_context_processor
    # def shell_context():  # pragma: no cover
    #     ctx = {'db': db}
    #     for attr in dir(models):
    #         model = getattr(models, attr)
    #         if hasattr(model, '__bases__') and \
    #                 db.Model in getattr(model, '__bases__'):
    #             ctx[attr] = model
    #     return ctx

    @app.route('/')
    def index():  # pragma: no cover
        return redirect(url_for('apifairy.docs'))

    @app.after_request
    def after_request(response):
        # Werkzeu sometimes does not flush the request body so we do it here
        request.get_data()
        return response

    return app
