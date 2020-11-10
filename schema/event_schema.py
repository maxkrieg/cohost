from marshmallow import Schema, fields


class EventSchema(Schema):
    title = fields.Str(required=True)
    address = fields.Str()
    timestamp = fields.Date(data_key="timeStamp")
    google_maps_place_id = fields.Str(data_key="placeId")
