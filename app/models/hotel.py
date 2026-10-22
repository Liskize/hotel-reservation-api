from datetime import datetime, timezone

from app.extensions import db


class Hotel(db.Model):
    __tablename__ = "hotels"
    __table_args__ = (
        db.CheckConstraint(
            "nombre_chambres > 0",
            name="ck_hotels_nombre_chambres_positive",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120), nullable=False)
    ville = db.Column(db.String(100), nullable=False, index=True)
    adresse = db.Column(db.String(255), nullable=False)
    nombre_chambres = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    reservations = db.relationship(
        "Reservation",
        back_populates="hotel",
        lazy="select",
    )

    def __repr__(self):
        return f"<Hotel {self.id}: {self.nom}>"
