from app import db, create_app
from models.user import User
from models.event import Event
from models.user_events import UserEvent

app = create_app()

with app.app_context():
    print(User)
    print(Event)
    print(UserEvent)
    db.drop_all(app=app)
    db.create_all(app=app)
