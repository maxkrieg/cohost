from flask_restful import Resource

from models.event import Event
from db import db


class EventsApi(Resource):
    def get(self, user_id):
        events = db.session.query(Event).filter(Event.user_id == user_id).all()
        response = [
            {"title": event.title, "address": event.address, "time": event.timestamp}
            for event in events
        ]
        return response
