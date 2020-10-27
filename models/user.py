from datetime import datetime
from db import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())

    events = db.relationship("Event", backref="users", lazy=True)

    def __repr__(self):
        return "<User: id={}, email={}, date_created={}>".format(
            self.id, self.email, self.date_created
        )
