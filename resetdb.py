from app import db, create_app
from models.user import User
from models.event import Event
from models.user_event import UserEvent
from models.user_event_item import UserEventItem

app = create_app()

with app.app_context():
    print(User)
    print(Event)
    print(UserEvent)
    print(UserEventItem)
    db.drop_all(app=app)
    db.create_all(app=app)
