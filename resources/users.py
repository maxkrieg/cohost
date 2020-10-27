from flask_restful import Resource, abort, reqparse

from models.user import User
from db import db

parser = reqparse.RequestParser()
parser.add_argument(
    "first_name",
    type=str,
    required=True,
    location="json",
    help="Person's first name, cannot be blank",
)
parser.add_argument(
    "last_name",
    type=str,
    required=True,
    location="json",
    help="Person's last name, cannot be blank",
)


users = {1: {"first_name": "Max", "last_name": "Krieg"}}


def abort_if_user_not_exists(user_id):
    if user_id not in users:
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
        user_ids = sorted(list(users.keys()))
        new_user_id = user_ids[-1] + 1
        users[new_user_id] = user_data
        return new_user_id


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_exists(user_id)
        return {user_id: users[user_id]}

    def put(self, user_id):
        abort_if_user_not_exists(user_id)
        user_data = parser.parse_args(strict=True)
        users[user_id] = user_data
        return users[user_id]

    def delete(self, user_id):
        abort_if_user_not_exists(user_id)
        del users[user_id]
        return "", 204
