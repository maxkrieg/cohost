from flask_restful import Resource, abort, reqparse

from models.user import User
from db import db

parser = reqparse.RequestParser()
parser.add_argument(
    "firstName",
    type=str,
    required=True,
    location="json",
    help="Person's first name, cannot be blank",
)
parser.add_argument(
    "lastName",
    type=str,
    required=True,
    location="json",
    help="Person's last name, cannot be blank",
)
parser.add_argument("email", type=str, required=True, location="json")


def get_user_or_404(user_id):
    try:
        user = db.session.query(User).filter(User.id == user_id).one()
        return user
    except Exception as e:
        print("Error getting user {}: {}".format(user_id, str(e)))
        abort(404, message="User {} does not exist".format(user_id))


class UsersResource(Resource):
    def get(self):
        users = db.session.query(User).all()
        response = [
            {
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
            }
            for user in users
        ]
        return response

    def post(self):
        user_data = parser.parse_args(strict=True)
        new_user = User(
            email=user_data.email,
            first_name=user_data.firstName,
            last_name=user_data.lastName,
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.id


class UserResource(Resource):
    def get(self, user_id):
        user = get_user_or_404(user_id)
        return {
            "email": user.email,
            "firstName": user.first_name,
            "lastName": user.last_name,
        }

    def delete(self, user_id):
        user = get_user_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return "", 204
