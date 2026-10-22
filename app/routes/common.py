from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app.errors import ApiError
from app.extensions import db


def json_payload(schema, *, partial=False):
    if not request.is_json:
        raise ApiError("Le corps de la requete doit etre en JSON", 400)

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise ApiError("Le corps JSON doit etre un objet", 400)
    if partial and not payload:
        raise ApiError("Aucune donnee a modifier", 400)

    try:
        return schema.load(payload, partial=partial)
    except ValidationError as error:
        raise ApiError("Donnees invalides", 422, error.messages) from error


def pagination_args(default_per_page=10, max_per_page=100):
    page = _positive_int_arg("page", 1)
    per_page = _positive_int_arg("per_page", default_per_page)
    if per_page > max_per_page:
        raise ApiError(
            f"per_page ne peut pas depasser {max_per_page}",
            400,
        )
    return page, per_page


def optional_positive_int_arg(name):
    raw_value = request.args.get(name)
    if raw_value is None or raw_value == "":
        return None
    return _parse_positive_int(name, raw_value)


def _positive_int_arg(name, default):
    raw_value = request.args.get(name)
    if raw_value is None or raw_value == "":
        return default
    return _parse_positive_int(name, raw_value)


def _parse_positive_int(name, raw_value):
    try:
        value = int(raw_value)
    except (TypeError, ValueError) as error:
        raise ApiError(f"Le parametre {name} doit etre un entier positif", 400) from error
    if value < 1:
        raise ApiError(f"Le parametre {name} doit etre un entier positif", 400)
    return value


def pagination_response(pagination, schema):
    return {
        "items": schema.dump(pagination.items, many=True),
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        },
    }


def get_or_404(model, resource_id, resource_name):
    resource = db.session.get(model, resource_id)
    if resource is None:
        raise ApiError(f"{resource_name} introuvable", 404)
    return resource


def commit_or_conflict(message):
    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise ApiError(message, 409) from error
