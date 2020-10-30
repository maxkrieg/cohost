from flask_restful import Resource, reqparse
from models.user import User
from db import db

signup_data_parser = reqparse.RequestParser()
signup_data_parser.add_argument(
    "firstName",
    type=str,
    required=True,
    location="json",
    help="Person's first name, cannot be blank",
)
signup_data_parser.add_argument(
    "lastName",
    type=str,
    required=True,
    location="json",
    help="Person's last name, cannot be blank",
)
signup_data_parser.add_argument("email", type=str, required=True, location="json")
signup_data_parser.add_argument("password", type=str, required=True, location="json")


class SignupApi(Resource):
    def post(self):
        user_data = signup_data_parser.parse_args(strict=True)
        new_user = User(
            email=user_data.email,
            first_name=user_data.firstName,
            last_name=user_data.lastName,
            password=user_data.password,
        )
        new_user.hash_password()
        db.session.add(new_user)
        db.session.commit()
