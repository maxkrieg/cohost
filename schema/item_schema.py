from marshmallow import Schema, fields


class ItemSchema(Schema):
    title = fields.Str(required=True)
    quantity = fields.Integer(default=1)