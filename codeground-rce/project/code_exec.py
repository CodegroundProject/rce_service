from marshmallow import Schema, fields


class SchemaCodeExec(Schema):
    lang = fields.Str(required=True)
    code = fields.Str(required=True)
    # challenge_id = fields.Str(required=True)
