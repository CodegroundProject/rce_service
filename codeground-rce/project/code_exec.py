from marshmallow import Schema, fields


class SchemaCodeExec(Schema):
    lang = fields.Str(required=True)
    code = fields.Str(required=True)
