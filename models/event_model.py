from db import db
from datetime import datetime


class EventModel(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    place_id = db.Column(db.String())
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    modified_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return "<Event: id={}, title={}, user_id={}>".format(
            self.id, self.title, self.user_id
        )
