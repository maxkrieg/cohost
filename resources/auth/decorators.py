from flask_restful import abort
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from db import db


def user_required(func):
    @wraps(func)
    @jwt_required
    def wrapper(*args, **kwargs):
        user_handle = get_jwt_identity()

        try:
            user = db.session.query(User).filter(User.handle == user_handle).one()
        except NoResultFound as e:
            print("Error getting user {}: {}".format(user_handle, str(e)))
            abort(403, message="Unauthorized")

        return func(*args, **kwargs, user=user)

    return wrapper


def admin_required(func):
    @wraps(func)
    @jwt_required
    def wrapper(*args, **kwargs):
        user_handle = get_jwt_identity()

        try:
            user = (
                db.session.query(User)
                .filter(User.handle == user_handle)
                .filter(User.is_admin == True)
                .one()
            )
        except NoResultFound as e:
            print("Error getting user {}: {}".format(user_handle, str(e)))
            abort(403, message="Unauthorized for admin")

        return func(*args, **kwargs, user=user)

    return wrapper
