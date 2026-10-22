from marshmallow import Schema, fields, validate


class HotelSchema(Schema):
    id = fields.Integer(dump_only=True)
    nom = fields.String(
        required=True,
        validate=validate.Length(min=1, max=120),
    )
    ville = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )
    adresse = fields.String(
        required=True,
        validate=validate.Length(min=1, max=255),
    )
    nombre_chambres = fields.Integer(
        required=True,
        validate=validate.Range(min=1),
    )
    created_at = fields.DateTime(dump_only=True)


hotel_schema = HotelSchema()
