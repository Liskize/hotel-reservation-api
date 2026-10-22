from flask import Blueprint, jsonify, request

from app.errors import ApiError
from app.extensions import db
from app.models import Hotel, Reservation
from app.routes.common import (
    commit_or_conflict,
    get_or_404,
    json_payload,
    pagination_args,
    pagination_response,
)
from app.schemas import hotel_schema


hotels_bp = Blueprint("hotels", __name__, url_prefix="/api/v1/hotels")


@hotels_bp.get("")
def list_hotels():
    page, per_page = pagination_args()
    statement = db.select(Hotel)

    nom = request.args.get("nom", type=str)
    ville = request.args.get("ville", type=str)
    if nom:
        statement = statement.where(Hotel.nom.ilike(f"%{nom.strip()}%"))
    if ville:
        statement = statement.where(Hotel.ville.ilike(f"%{ville.strip()}%"))

    pagination = db.paginate(
        statement.order_by(Hotel.id),
        page=page,
        per_page=per_page,
        error_out=False,
    )
    return jsonify(pagination_response(pagination, hotel_schema)), 200


@hotels_bp.get("/<int:hotel_id>")
def get_hotel(hotel_id):
    hotel = get_or_404(Hotel, hotel_id, "Hotel")
    return jsonify(hotel_schema.dump(hotel)), 200


@hotels_bp.post("")
def create_hotel():
    data = json_payload(hotel_schema)
    hotel = Hotel(**data)
    db.session.add(hotel)
    commit_or_conflict("Impossible de creer cet hotel")
    return jsonify(hotel_schema.dump(hotel)), 201


@hotels_bp.put("/<int:hotel_id>")
def update_hotel(hotel_id):
    hotel = get_or_404(Hotel, hotel_id, "Hotel")
    data = json_payload(hotel_schema, partial=True)
    for field, value in data.items():
        setattr(hotel, field, value)
    commit_or_conflict("Impossible de modifier cet hotel")
    return jsonify(hotel_schema.dump(hotel)), 200


@hotels_bp.delete("/<int:hotel_id>")
def delete_hotel(hotel_id):
    hotel = get_or_404(Hotel, hotel_id, "Hotel")
    reservation_id = db.session.scalar(
        db.select(Reservation.id).where(Reservation.hotel_id == hotel.id).limit(1)
    )
    if reservation_id is not None:
        raise ApiError("Cet hotel possede encore des reservations", 409)
    db.session.delete(hotel)
    commit_or_conflict("Impossible de supprimer cet hotel")
    return "", 204
