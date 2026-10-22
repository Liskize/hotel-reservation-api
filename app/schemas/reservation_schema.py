from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from app.models.reservation import STATUTS_RESERVATION


class ReservationSchema(Schema):
    id = fields.Integer(dump_only=True)
    hotel_id = fields.Integer(required=True, validate=validate.Range(min=1))
    client_id = fields.Integer(required=True, validate=validate.Range(min=1))
    date_debut = fields.Date(required=True)
    date_fin = fields.Date(required=True)
    statut = fields.String(
        load_default="EN_ATTENTE",
        validate=validate.OneOf(STATUTS_RESERVATION),
    )
    montant_total = fields.Decimal(
        places=2,
        allow_none=True,
        as_string=True,
        validate=validate.Range(min=0),
    )
    created_at = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_dates(self, data, **_kwargs):
        date_debut = data.get("date_debut")
        date_fin = data.get("date_fin")
        if date_debut and date_fin and date_fin <= date_debut:
            raise ValidationError(
                {"date_fin": ["La date de fin doit etre posterieure a la date de debut."]}
            )


reservation_schema = ReservationSchema()
