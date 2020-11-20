from flask_restful import Resource, abort
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from models.event_model import EventModel
from schema.event_schema import EventSchema
from .services.user_service import get_user_or_404
from db import db


class EventsApi(Resource):
    @jwt_required
    def get(self):
        user_handle = get_jwt_identity()
        user = get_user_or_404(user_handle)
        response = EventSchema(many=True).dump(user.events)
        return response

    @jwt_required
    def post(self):
        user_handle = get_jwt_identity()
        user = get_user_or_404(user_handle)

        try:
            event_data = EventSchema().load(request.get_json())
        except ValidationError as e:
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
