from app import db, create_app
from models.user import User
from models.event import Event
from models.event_user import EventUser
from models.item import Item

app = create_app()

with app.app_context():
    print(User)
    print(Event)
    print(EventUser)
    print(Item)
    db.drop_all(app=app)
    # db.create_all(app=app)
