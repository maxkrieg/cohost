from flask_restful import Resource
from .auth.decorators import user_required
from schema.user_schema import UserSchema


class User(Resource):
    method_decorators = [user_required]

    def get(self, user):
        return UserSchema().dump(user)
