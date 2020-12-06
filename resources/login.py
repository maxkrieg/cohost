import datetime
from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import create_access_token, jwt_optional, get_jwt_identity
from werkzeug.exceptions import Unauthorized
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError

from db import db
from models.user_model import UserModel
from schema.user_schema import UserSchema
from resources.errors import InternalServerError


class LoginApi(Resource):
    @jwt_optional
    def post(self):
        logged_in_user_handle = get_jwt_identity()
        if logged_in_user_handle:
            return {"handle": logged_in_user_handle}, 200

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

        expires = datetime.timedelta(days=365)
        access_token = create_access_token(
            identity=str(user.handle), expires_delta=expires
        )
        return {"token": access_token, "handle": str(user.handle)}, 200
