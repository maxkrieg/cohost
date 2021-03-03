from db import db
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM

GUEST = "Guest"
HOST = "Host"
user_types = (GUEST, HOST)


class EventUser(db.Model):

    __tablename__ = "event_users"

    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(
        ENUM(*user_types, name="user_types"), nullable=False, default=GUEST
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="events")

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    event = db.relationship("Event", back_populates="users")

    user_types = user_types
    GUEST = GUEST
    HOST = HOST

    # user_event_items = db.relationship("UserEventItem", back_populates="user_event")

    UniqueConstraint(user_id, event_id, name="event_users_user_id_event_id_key")

    def __repr__(self):
        return "<EventUser: id={}, user_id={}, event_id={}>".format(
            self.id, self.user_id, self.event_id
        )
