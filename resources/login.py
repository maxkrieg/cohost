import datetime
from flask import Blueprint, request, current_app as app, jsonify
from flask_restful import abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_optional,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from werkzeug.exceptions import Unauthorized
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError

from db import db
from models.user_model import UserModel
from schema.user_schema import UserSchema
from resources.errors import InternalServerError

login_api = Blueprint("login_api", __name__)


@login_api.route("/login", methods=["POST"])
@jwt_optional
def login():
    logged_in_user_handle = get_jwt_identity()
    app.logger.info("Got logged in user handle: {}".format(logged_in_user_handle))
    if logged_in_user_handle:
        return jsonify(login=True), 200

    try:
        login_data = UserSchema().load(request.get_json(), partial=True)
    except ValidationError as e:
        abort(
            400,
            message="Missing login fields",
            status=400,
            errors=e.messages,
        )

    try:
        user = (
            db.session.query(UserModel)
            .filter(UserModel.email == login_data["email"])
            .one()
        )
        authorized = user.check_password(login_data["password"])
        if not authorized:
            raise Unauthorized("Invalid password")
    except (NoResultFound, Unauthorized) as e:
        abort(
            401,
            message="Error authorizing user with email '{}': {}".format(
                login_data.email, e
            ),
            status=401,
        )
    except Exception:
        raise InternalServerError

    token_identity = str(user.handle)
    access_token_exp = datetime.timedelta(days=app.config["JWT_ACCESS_TOKEN_EXP_DAYS"])
    refresh_token_exp = datetime.timedelta(
        days=app.config["JWT_REFRESH_TOKEN_EXP_DAYS"]
    )

    # Create the tokens we will be sending back to the user
    access_token = create_access_token(
        identity=token_identity, expires_delta=access_token_exp
    )
    refresh_token = create_refresh_token(
        identity=token_identity, expires_delta=refresh_token_exp
    )

    # Set the JWTs and the CSRF double submit protection cookies
    # in this response
    response = jsonify(login=True)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200


@login_api.route("/logout", methods=["POST"])
def logout():
    resp = jsonify(logout=True)
    unset_jwt_cookies(resp)
    return resp, 200
