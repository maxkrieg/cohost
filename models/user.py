from datetime import datetime
from db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    password_hash = db.Column(db.String(128), nullable=False)

    events = db.relationship("Event", backref="users", lazy=True)

    def hash_password(self):
        self.password_hash = generate_password_hash(self.password_hash).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User: id={}, email={}, date_created={}>".format(
            self.id, self.email, self.date_created
        )
