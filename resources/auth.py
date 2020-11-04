import datetime
from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import Unauthorized
from models.user import User
from schema.auth import SignupDataSchema, LoginDataSchema
from sqlalchemy.orm.exc import NoResultFound
from db import db
from marshmallow import ValidationError


class SignupApi(Resource):
    def post(self):
        try:
            user_data = SignupDataSchema().load(request.get_json())
        except ValidationError as e:
            abort(
                400,
                message="Error validating signup data",
                status=400,
                errors=e.messages,
            )

        new_user = User(**user_data)
        new_user.hash_password()
        db.session.add(new_user)
        db.session.commit()
        response = SignupDataSchema().dump(new_user)
        return response


class LoginApi(Resource):
    def post(self):
        try:
            login_data = LoginDataSchema().load(request.get_json())
        except ValidationError as e:
            abort(
                400,
                message="Missing login fields",
                status=400,
                errors=e.messages,
            )

        try:
            user = (
                db.session.query(User).filter(User.email == login_data["email"]).one()
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

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {"token": access_token}, 200
