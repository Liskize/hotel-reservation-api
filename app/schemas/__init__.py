"""Marshmallow schemas used by the REST API."""

from app.schemas.client_schema import client_schema
from app.schemas.hotel_schema import hotel_schema
from app.schemas.reservation_schema import reservation_schema

__all__ = ["client_schema", "hotel_schema", "reservation_schema"]
