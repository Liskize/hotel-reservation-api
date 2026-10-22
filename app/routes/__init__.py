"""API blueprints registration."""

from app.routes.client_routes import clients_bp
from app.routes.hotel_routes import hotels_bp
from app.routes.reservation_routes import reservations_bp


def register_blueprints(app):
    app.register_blueprint(hotels_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(reservations_bp)
