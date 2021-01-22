from flask import request, current_app as app
from flask_restful import Resource, abort
from marshmallow import ValidationError

from db import db
from models.user import User
from schema.user_schema import UserSchema
from sqlalchemy.exc import SQLAlchemyError


class Signup(Resource):
    def post(self):
        try:
            user_data = UserSchema().load(request.get_json())
        except ValidationError as e:
            app.logger.error(e)
            abort(
                400,
                message="Error validating signup data",
                status=400,
                errors=e.messages,
            )

        existing_user = (
            db.session.query(User).filter(User.email == user_data["email"]).first()
        )
        if existing_user is not None:
            error_message = "User account with this email already exists"
            app.logger.error(error_message)
            abort(400, message=error_message, status=400)

        new_user = User(**user_data)
        new_user.hash_password()

        db.session.add(new_user)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            app.logger.error(e)
            abort(500, message="Error creating new user", status=500)

        response = UserSchema().dump(new_user)
        return response
