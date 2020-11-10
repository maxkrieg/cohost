from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from models.user_model import UserModel
from schema.user_schema import UserSchema
from db import db


def get_user_or_404(user_id):
    try:
        user = db.session.query(UserModel).filter(UserModel.id == user_id).one()
        return user
    except NoResultFound as e:
        print("Error getting user {}: {}".format(user_id, str(e)))
        abort(404, message="User {} does not exist".format(user_id))


# TODO: Wrap these endpoints with an admin decorator
class UsersApi(Resource):
    def get(self):
        users = db.session.query(UserModel).all()
        response = UserSchema(many=True).dump(users)
        return response


class UserApi(Resource):
    def get(self, user_id):
        user = get_user_or_404(user_id)
        response = UserSchema().dump(user)
        return response

    def delete(self, user_id):
        user = get_user_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return "", 204
