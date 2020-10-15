from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("first_name", type=str)
parser.add_argument("last_name", type=str, required=True)


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


users = {1: {"first_name": "Max"}}


class Users(Resource):
    def get(self):
        return users


class User(Resource):
    def get(self, user_id):
        if user_id not in users:
            abort(404, message="User {} does not exist".format(user_id))
        return {user_id: users[user_id]}

    def put(self, user_id):
        user_data = parser.parse_args(strict=True)
        users[user_id] = user_data
        return {user_id: users[user_id]}


api.add_resource(HelloWorld, "/")
api.add_resource(Users, "/users")
api.add_resource(User, "/users/<int:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
