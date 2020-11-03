import datetime
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import create_access_token
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
            password_hash=user_data.password,
        )
        new_user.validate_password()
        new_user.hash_password()
        db.session.add(new_user)
        db.session.commit()
        return {
            "id": new_user.id,
            "email": new_user.email,
            "firstName": new_user.first_name,
            "lastName": new_user.last_name,
        }


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
                raise Exception("User unauthorized")
        except Exception as e:
            print("Error authenticating user '{}': {}".format(login_data.email, str(e)))
            abort(401, message="Email or password invalid")

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {"token": access_token}, 200
