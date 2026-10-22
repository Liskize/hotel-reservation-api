from flask import Flask, jsonify

from app.config import Config
from app.errors import register_error_handlers
from app.extensions import db, migrate
from app.routes import register_blueprints


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models after the extension initialization so Alembic can detect
    # every table when running ``flask db migrate``.
    from app import models  # noqa: F401

    register_blueprints(app)
    register_error_handlers(app)

    @app.get("/")
    def accueil():
        return jsonify(
            {
                "application": "API de reservations hotelieres",
                "version": "1.0.0",
                "message": "Bienvenue sur notre API REST",
            }
        ), 200

    @app.get("/api/v1/health")
    def health():
        return jsonify(
            {
                "status": "OK",
                "message": "API operationnelle",
            }
        ), 200

    return app
