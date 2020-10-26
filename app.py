from flask import Flask
from flask_restful import Api
from resources.users import UsersResource, UserResource
from db import db


def create_app():
    app = Flask(__name__)
    app.config["BUNDLE_ERRORS"] = True
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:postgres@127.0.0.1/cohostdb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True

    api = Api(app)
    api.add_resource(UsersResource, "/users")
    api.add_resource(UserResource, "/users/<int:user_id>")
    db.init_app(app)

    return app
