from db import db


class Item(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="items")

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    event = db.relationship("Event", back_populates="items")

    def __repr__(self):
        return "<UserEventItem: id={}, title={}, user_id={}, event_id={}>".format(
            self.id, self.title, self.user_id, self.event_id
        )
