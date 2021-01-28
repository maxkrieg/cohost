from db import db
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM

GUEST = "Guest"
HOST = "Host"
user_types = (GUEST, HOST)


class UserEvent(db.Model):

    __tablename__ = "user_events"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    user_type = db.Column(
        ENUM(*user_types, name="user_types"), nullable=False, default=GUEST
    )

    user_types = user_types
    GUEST = GUEST
    HOST = HOST

    user = db.relationship("User", back_populates="events")
    event = db.relationship("Event", back_populates="users")

    user_event_items = db.relationship("UserEventItem", back_populates="user_event")

    UniqueConstraint(user_id, event_id, name="user_events_user_id_event_id_key")

    def __repr__(self):
        return "<UserEvent: id={}, user_id={}, event_id={}>".format(
            self.id, self.user_id, self.event_id
        )
