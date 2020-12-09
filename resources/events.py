from flask import request, current_app as app
from flask_restful import Resource, abort
from marshmallow import ValidationError

from models.event_model import EventModel
from schema.event_schema import EventSchema
from .auth.decorators import user_required
from db import db


class Events(Resource):
    method_decorators = [user_required]

    def get(self, user):
        response = EventSchema(many=True).dump(user.events)
        return response

    def post(self, user):
        try:
            event_data = EventSchema().load(request.get_json())
        except ValidationError as e:
            app.logger.error(e)
            abort(
                400,
                message="Error validating event data",
                status=400,
                errors=e.messages,
            )

        new_event = EventModel(**event_data)
        user.events.append(new_event)
        db.session.commit()

        response = EventSchema(many=True).dump(user.events)

        return response
