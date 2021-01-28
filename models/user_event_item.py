from db import db


class UserEventItem(db.Model):

    __tablename__ = "user_event_items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user_event_id = db.Column(db.Integer, db.ForeignKey("user_events.id"))

    user_event = db.relationship("UserEvent", back_populates="user_event_items")

    def __repr__(self):
        return "<UserEventItem: id={}, title={}, user_event_id={}>".format(
            self.id, self.title, self.user_event_id
        )
