from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restful import Api
from resources.errors import errors
from resources.users import UsersApi, UserApi
from resources.events import EventsApi
from resources.signup import SignupApi
from resources.login import LoginApi
from db import db


def create_app():
    app = Flask(__name__)

    app.config.from_envvar("ENV_FILE_LOCATION")
    Bcrypt(app)
    JWTManager(app)
    CORS(app)
    api = Api(app, errors=errors)
    api.add_resource(UsersApi, "/api/admin/users")
    api.add_resource(UserApi, "/api/admin/users/<string:user_handle>")
    api.add_resource(EventsApi, "/api/events")
    api.add_resource(SignupApi, "/api/signup")
    api.add_resource(LoginApi, "/api/login")
    db.init_app(app)

    return app
