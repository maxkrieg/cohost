from flask_restful import Resource

from models.user_model import UserModel
from schema.user_schema import UserSchema
from .services.user_service import get_user_or_404
from db import db


# TODO: Wrap these endpoints with an admin decorator
class UsersApi(Resource):
    def get(self):
        users = db.session.query(UserModel).all()
        response = UserSchema(many=True).dump(users)
        return response


class UserApi(Resource):
    def get(self, user_handle):
        user = get_user_or_404(user_handle)
        response = UserSchema().dump(user)
        return response

    def delete(self, user_handle):
        user = get_user_or_404(user_handle)
        db.session.delete(user)
        db.session.commit()
        return "", 204
