from marshmallow import Schema, fields


class EventSchema(Schema):
    title = fields.Str(required=True)
    address = fields.Str()
    timestamp = fields.DateTime(data_key="timestamp")
    google_maps_place_id = fields.Str(data_key="placeId")
