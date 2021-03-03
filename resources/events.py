from flask import request, current_app as app
from flask_restful import Resource, abort
from marshmallow import ValidationError

from models.event import Event
from models.event_user import EventUser
from models.item import Item
from schema.event_schema import EventSchema
from schema.item_schema import ItemSchema
from .auth.decorators import user_required
from db import db


class Events(Resource):
    method_decorators = [user_required]

    def get(self, user):
        response = EventSchema(many=True).dump(user.events)
        return response

    def post(self, user):
        try:
            payload = request.get_json()
            payload_items = payload.pop("items", [])
            event_data = EventSchema().load(payload)
            item_data = ItemSchema(many=True).load(payload_items)
        except ValidationError as e:
            app.logger.error(e)
            abort(
                400,
                message="Error validating event data",
                status=400,
                errors=e.messages,
            )

        event = Event(**event_data)
        user_event = EventUser(user=user, event=event, user_type=EventUser.HOST)
        for item in item_data:
            Item(**item)

        user_event.user_event_items.append(item_data)
        db.session.commit()

        response = EventSchema(many=True).dump(user.events)

        return response
