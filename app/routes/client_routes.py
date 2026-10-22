from flask import Blueprint, jsonify, request

from app.errors import ApiError
from app.extensions import db
from app.models import Client, Reservation
from app.routes.common import (
    commit_or_conflict,
    get_or_404,
    json_payload,
    pagination_args,
    pagination_response,
)
from app.schemas import client_schema


clients_bp = Blueprint("clients", __name__, url_prefix="/api/v1/clients")


@clients_bp.get("")
def list_clients():
    page, per_page = pagination_args()
    statement = db.select(Client)

    nom = request.args.get("nom", type=str)
    email = request.args.get("email", type=str)
    if nom:
        statement = statement.where(Client.nom.ilike(f"%{nom.strip()}%"))
    if email:
        statement = statement.where(Client.email.ilike(f"%{email.strip()}%"))

    pagination = db.paginate(
        statement.order_by(Client.id),
        page=page,
        per_page=per_page,
        error_out=False,
    )
    return jsonify(pagination_response(pagination, client_schema)), 200


@clients_bp.get("/<int:client_id>")
def get_client(client_id):
    client = get_or_404(Client, client_id, "Client")
    return jsonify(client_schema.dump(client)), 200


@clients_bp.post("")
def create_client():
    data = json_payload(client_schema)
    data["email"] = data["email"].strip().lower()
    existing_id = db.session.scalar(
        db.select(Client.id).where(Client.email == data["email"]).limit(1)
    )
    if existing_id is not None:
        raise ApiError("Cette adresse email est deja utilisee", 409)

    client = Client(**data)
    db.session.add(client)
    commit_or_conflict("Cette adresse email est deja utilisee")
    return jsonify(client_schema.dump(client)), 201


@clients_bp.put("/<int:client_id>")
def update_client(client_id):
    client = get_or_404(Client, client_id, "Client")
    data = json_payload(client_schema, partial=True)
    if "email" in data:
        data["email"] = data["email"].strip().lower()
        existing_id = db.session.scalar(
            db.select(Client.id)
            .where(Client.email == data["email"], Client.id != client.id)
            .limit(1)
        )
        if existing_id is not None:
            raise ApiError("Cette adresse email est deja utilisee", 409)

    for field, value in data.items():
        setattr(client, field, value)
    commit_or_conflict("Cette adresse email est deja utilisee")
    return jsonify(client_schema.dump(client)), 200


@clients_bp.delete("/<int:client_id>")
def delete_client(client_id):
    client = get_or_404(Client, client_id, "Client")
    reservation_id = db.session.scalar(
        db.select(Reservation.id).where(Reservation.client_id == client.id).limit(1)
    )
    if reservation_id is not None:
        raise ApiError("Ce client possede encore des reservations", 409)
    db.session.delete(client)
    commit_or_conflict("Impossible de supprimer ce client")
    return "", 204
