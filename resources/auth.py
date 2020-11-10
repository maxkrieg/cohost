import datetime
from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import Unauthorized
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError

from db import db
from models.user_model import UserModel
from schema.user_schema import UserSchema
from resources.errors import InternalServerError


class SignupApi(Resource):
    def post(self):
        try:
            user_data = UserSchema().load(request.get_json())
        except ValidationError as e:
            abort(
                400,
                message="Error validating signup data",
                status=400,
                errors=e.messages,
            )

        new_user = UserModel(**user_data)
        new_user.hash_password()
        db.session.add(new_user)
        db.session.commit()
        response = UserSchema().dump(new_user)
        return response


class LoginApi(Resource):
    def post(self):
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

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {"token": access_token}, 200
