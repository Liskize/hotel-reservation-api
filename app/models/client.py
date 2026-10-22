from datetime import datetime, timezone

from app.extensions import db


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    telephone = db.Column(db.String(30), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    reservations = db.relationship(
        "Reservation",
        back_populates="client",
        lazy="select",
    )

    def __repr__(self):
        return f"<Client {self.id}: {self.email}>"
