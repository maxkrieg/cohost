from flask_restful import abort
from sqlalchemy.orm.exc import NoResultFound

from models.user_model import UserModel
from db import db


def get_user_or_404(user_handle):
    try:
        user = db.session.query(UserModel).filter(UserModel.handle == user_handle).one()
        return user
    except NoResultFound as e:
        print("Error getting user {}: {}".format(user_handle, str(e)))
        abort(404, message="User {} does not exist".format(user_handle))
