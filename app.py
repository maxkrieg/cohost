from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
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
    api = Api(app, errors=errors)
    api.add_resource(UsersApi, "/admin/users")
    api.add_resource(UserApi, "/admin/users/<string:user_handle>")
    api.add_resource(EventsApi, "/events")
    api.add_resource(SignupApi, "/auth/signup")
    api.add_resource(LoginApi, "/auth/login")
    db.init_app(app)

    return app
