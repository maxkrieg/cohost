from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError

from db import db
from models.user_model import UserModel
from schema.user_schema import UserSchema
from sqlalchemy.exc import SQLAlchemyError


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

        existing_user = (
            db.session.query(UserModel)
            .filter(UserModel.email == user_data["email"])
            .first()
        )
        if existing_user is not None:
            abort(
                400, message="User account with this email already exists", status=400
            )

        new_user = UserModel(**user_data)
        new_user.hash_password()

        db.session.add(new_user)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            abort(500, message="Error creating new user", status=500)

        response = UserSchema().dump(new_user)
        return response
