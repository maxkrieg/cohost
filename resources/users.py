from flask_restful import Resource, abort


from models.user import User
from db import db


def get_user_or_404(user_id):
    try:
        user = db.session.query(User).filter(User.id == user_id).one()
        return user
    except Exception as e:
        print("Error getting user {}: {}".format(user_id, str(e)))
        abort(404, message="User {} does not exist".format(user_id))


class UsersApi(Resource):
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


class UserApi(Resource):
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
