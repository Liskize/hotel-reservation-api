from sqlalchemy import func

from app.errors import ApiError
from app.extensions import db
from app.models import Client, Hotel, Reservation


def validate_reservation(data, current=None):
    hotel_id = data.get("hotel_id", current.hotel_id if current else None)
    client_id = data.get("client_id", current.client_id if current else None)
    date_debut = data.get("date_debut", current.date_debut if current else None)
    date_fin = data.get("date_fin", current.date_fin if current else None)
    statut = data.get("statut", current.statut if current else "EN_ATTENTE")

    if date_fin <= date_debut:
        raise ApiError(
            "Donnees invalides",
            422,
            {"date_fin": ["La date de fin doit etre posterieure a la date de debut."]},
        )

    hotel = db.session.get(Hotel, hotel_id)
    if hotel is None:
        raise ApiError("Hotel introuvable", 404)

    if db.session.get(Client, client_id) is None:
        raise ApiError("Client introuvable", 404)

    duplicate_query = db.select(Reservation.id).where(
        Reservation.hotel_id == hotel_id,
        Reservation.client_id == client_id,
        Reservation.date_debut == date_debut,
        Reservation.date_fin == date_fin,
    )
    if current is not None:
        duplicate_query = duplicate_query.where(Reservation.id != current.id)
    if db.session.scalar(duplicate_query.limit(1)) is not None:
        raise ApiError("Cette reservation existe deja", 409)

    if statut != "ANNULEE":
        occupied_query = db.select(func.count(Reservation.id)).where(
            Reservation.hotel_id == hotel_id,
            Reservation.statut != "ANNULEE",
            Reservation.date_debut < date_fin,
            Reservation.date_fin > date_debut,
        )
        if current is not None:
            occupied_query = occupied_query.where(Reservation.id != current.id)
        occupied = db.session.scalar(occupied_query) or 0
        if occupied >= hotel.nombre_chambres:
            raise ApiError("Aucune chambre disponible pour cette periode", 409)
