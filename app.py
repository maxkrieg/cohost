from logging.config import dictConfig
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from logger_config import logger_config
from routes import initialize_routes, log_routes
from db import db

dictConfig(logger_config)


def create_app():
    app = Flask(__name__)
    app.config.from_envvar("ENV_FILE_LOCATION")
    Bcrypt(app)
    JWTManager(app)
    initialize_routes(app)
    log_routes(app)
    CORS(app, supports_credentials=True)

    db.init_app(app)

    return app
