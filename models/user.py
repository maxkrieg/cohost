from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    modified_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now()
    )
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)

    events = db.relationship("UserEvent", back_populates="user")
    items = db.relationship("User", back_populates="user")

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User: id={}, email={}, handle={}>".format(
            self.id, self.email, self.handle
        )
