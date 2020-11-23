from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError

from db import db
from models.user_model import UserModel
from schema.user_schema import UserSchema


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
