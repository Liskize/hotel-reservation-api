from datetime import date

from flask import Blueprint, jsonify, request

from app.errors import ApiError
from app.extensions import db
from app.models import Reservation, STATUTS_RESERVATION
from app.routes.common import (
    commit_or_conflict,
    get_or_404,
    json_payload,
    optional_positive_int_arg,
    pagination_args,
    pagination_response,
)
from app.schemas import reservation_schema
from app.services import validate_reservation


reservations_bp = Blueprint(
    "reservations",
    __name__,
    url_prefix="/api/v1/reservations",
)


@reservations_bp.get("")
def list_reservations():
    page, per_page = pagination_args()
    statement = db.select(Reservation)

    hotel_id = optional_positive_int_arg("hotel_id")
    client_id = optional_positive_int_arg("client_id")
    statut = request.args.get("statut", type=str)
    date_debut = _date_arg("date_debut")
    date_fin = _date_arg("date_fin")

    if hotel_id is not None:
        statement = statement.where(Reservation.hotel_id == hotel_id)
    if client_id is not None:
        statement = statement.where(Reservation.client_id == client_id)
    if statut:
        statut = statut.strip().upper()
        if statut not in STATUTS_RESERVATION:
            raise ApiError("Le parametre statut est invalide", 400)
        statement = statement.where(Reservation.statut == statut)
    if date_debut is not None:
        statement = statement.where(Reservation.date_debut >= date_debut)
    if date_fin is not None:
        statement = statement.where(Reservation.date_fin <= date_fin)

    pagination = db.paginate(
        statement.order_by(Reservation.id),
        page=page,
        per_page=per_page,
        error_out=False,
    )
    return jsonify(pagination_response(pagination, reservation_schema)), 200


@reservations_bp.get("/<int:reservation_id>")
def get_reservation(reservation_id):
    reservation = get_or_404(Reservation, reservation_id, "Reservation")
    return jsonify(reservation_schema.dump(reservation)), 200


@reservations_bp.post("")
def create_reservation():
    data = json_payload(reservation_schema)
    validate_reservation(data)
    reservation = Reservation(**data)
    db.session.add(reservation)
    commit_or_conflict("Cette reservation existe deja")
    return jsonify(reservation_schema.dump(reservation)), 201


@reservations_bp.put("/<int:reservation_id>")
def update_reservation(reservation_id):
    reservation = get_or_404(Reservation, reservation_id, "Reservation")
    data = json_payload(reservation_schema, partial=True)
    validate_reservation(data, reservation)
    for field, value in data.items():
        setattr(reservation, field, value)
    commit_or_conflict("Cette reservation existe deja")
    return jsonify(reservation_schema.dump(reservation)), 200


@reservations_bp.delete("/<int:reservation_id>")
def delete_reservation(reservation_id):
    reservation = get_or_404(Reservation, reservation_id, "Reservation")
    db.session.delete(reservation)
    commit_or_conflict("Impossible de supprimer cette reservation")
    return "", 204


def _date_arg(name):
    raw_value = request.args.get(name)
    if raw_value is None or raw_value == "":
        return None
    try:
        return date.fromisoformat(raw_value)
    except ValueError as error:
        raise ApiError(f"Le parametre {name} doit respecter AAAA-MM-JJ", 400) from error
