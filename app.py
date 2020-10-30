from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api
from resources.users import UsersApi, UserApi
from resources.events import EventsApi
from resources.auth import SignupApi
from db import db


def create_app():
    app = Flask(__name__)

    app.config.update(
        {
            "BUNDLE_ERRORS": True,
            "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@127.0.0.1/cohostdb",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SQLALCHEMY_ECHO": True,
        }
    )

    Bcrypt(app)

    api = Api(app)
    api.add_resource(UsersApi, "/users")
    api.add_resource(UserApi, "/users/<int:user_id>")
    api.add_resource(EventsApi, "/users/<int:user_id>/events")
    api.add_resource(SignupApi, "/auth/signup")
    db.init_app(app)

    return app
