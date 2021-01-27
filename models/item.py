from db import db


class Item(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    title = db.Column(db.String(120), nullable=False)

    event = db.relationship("Event", back_populates="items")

    def __repr__(self):
        return "<Item: id={}, title={}, user_id={}, event_id={}>".format(
            self.id, self.title, self.user_id, self.event_id
        )
