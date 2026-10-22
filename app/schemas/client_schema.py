from marshmallow import Schema, fields, validate


class ClientSchema(Schema):
    id = fields.Integer(dump_only=True)
    nom = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )
    prenom = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )
    email = fields.Email(required=True)
    telephone = fields.String(
        allow_none=True,
        validate=validate.Length(max=30),
    )
    created_at = fields.DateTime(dump_only=True)


client_schema = ClientSchema()
