from flask_restful import Resource, abort
from flask import request
from marshmallow import ValidationError

from models.event_model import EventModel
from schema.event_schema import EventSchema
from db import db


class EventsApi(Resource):
    def get(self, user_id):
        events = (
            db.session.query(EventModel).filter(EventModel.user_id == user_id).all()
        )
        response = EventSchema(many=True).dump(events)
        return response

    def post(self, user_id):
        try:
            event_data = EventSchema().load(request.get_json())
        except ValidationError as e:
            abort(
                400,
                message="Error validating event data",
                status=400,
                errors=e.messages,
            )
        new_event = EventModel(**event_data, user_id=user_id)
        db.session.add(new_event)
        db.session.commit()
        response = EventSchema().dump(new_event)
        return response
