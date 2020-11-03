import re
from sqlalchemy.orm import validates
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

from db import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    password_hash = db.Column(db.String(128), nullable=False)

    events = db.relationship("Event", backref="users", lazy=True)

    @validates("email")
    def validate_email(self, key, email):
        email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        is_valid = re.match(email_regex, email)
        if not is_valid:
            raise AssertionError("Invalid email address")
        return email

    def hash_password(self):
        self.password_hash = generate_password_hash(self.password_hash).decode("utf8")

    def validate_password(self):
        password = self.password_hash
        if len(password) < 6 or len(password) > 18:
            raise ValueError("Password must be between 7 and 18 characters long")

        if not any(char.isdigit() for char in password):
            raise ValueError("Password should have at least one numeral")

        if not any(char.isupper() for char in password):
            raise ValueError("Password should have at least one uppercase letter")

        if not any(char.islower() for char in password):
            raise ValueError("Password should have at least one lowercase letter")

        if not any(char in ["$", "@", "#", "%"] for char in password):
            raise ValueError("Password should have at least one of the symbols $@#%")

        return True

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User: id={}, email={}, date_created={}>".format(
            self.id, self.email, self.date_created
        )
