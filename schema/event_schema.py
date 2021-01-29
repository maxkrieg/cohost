from marshmallow import Schema, fields


class EventItemSchema(Schema):
    title = fields.Str(required=True)
    quantity = fields.Integer(default=1)


class EventSchema(Schema):
    title = fields.Str(required=True)
    address = fields.Str()
    timestamp = fields.DateTime(data_key="timestamp")
    start_date = fields.DateTime(data_key="startDate")
    end_date = fields.DateTime(data_key="endDate")
    place_id = fields.Str(data_key="placeId")
