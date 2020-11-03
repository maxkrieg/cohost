import re
import datetime
from flask import request
from flask_restful import Resource, reqparse, abort
from marshmallow import Schema, fields, validates, ValidationError

# from marshmallow.validate import Length
from flask_jwt_extended import create_access_token
from models.user import User
from resources.errors import UnauthorizedError
from sqlalchemy.orm.exc import NoResultFound
from db import db


class SignupDataSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    first_name = fields.Str(required=True, data_key="firstName")
    last_name = fields.Str(required=True, data_key="lastName")
    password = fields.Str(required=True, load_only=True)

    @validates("email")
    def validate_email(self, email):
        email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        is_valid = re.match(email_regex, email)
        if not is_valid:
            raise ValidationError(field_name="email", message="Bad email format")

    @validates("password")
    def validate_password(self, password):
        error_messages = []
        if len(password) < 6 or len(password) > 18:
            error_messages.append("Password must be between 7 and 18 characters long")

        if not any(char.isdigit() for char in password):
            error_messages.append("Password should have at least one numeral")

        if not any(char.isupper() for char in password):
            error_messages.append("Password should have at least one uppercase letter")

        if not any(char.islower() for char in password):
            error_messages.append("Password should have at least one lowercase letter")

        if not any(char in ["$", "@", "#", "%"] for char in password):
            error_messages.append(
                "Password should have at least one of the symbols $@#%"
            )

        if len(error_messages) > 0:
            raise ValidationError(", ".join(error_messages))


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


login_data_parser = reqparse.RequestParser()
login_data_parser.add_argument("email", type=str, required=True, location="json")
login_data_parser.add_argument("password", type=str, required=True, location="json")


class LoginApi(Resource):
    def post(self):
        login_data = login_data_parser.parse_args(strict=True)

        try:
            user = db.session.query(User).filter(User.email == login_data.email).one()
            authorized = user.check_password(login_data.password)
            if not authorized:
                raise UnauthorizedError("Invalid password")
        except (NoResultFound, UnauthorizedError) as e:
            print(
                "Error authorizing user with email '{}': {}".format(login_data.email, e)
            )
            raise UnauthorizedError

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {"token": access_token}, 200
