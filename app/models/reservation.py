from datetime import datetime, timezone

from app.extensions import db


STATUTS_RESERVATION = ("EN_ATTENTE", "CONFIRMEE", "ANNULEE", "TERMINEE")


class Reservation(db.Model):
    __tablename__ = "reservations"
    __table_args__ = (
        db.CheckConstraint(
            "date_fin > date_debut",
            name="ck_reservations_dates_coherentes",
        ),
        db.CheckConstraint(
            "statut IN ('EN_ATTENTE', 'CONFIRMEE', 'ANNULEE', 'TERMINEE')",
            name="ck_reservations_statut_valide",
        ),
        db.CheckConstraint(
            "montant_total IS NULL OR montant_total >= 0",
            name="ck_reservations_montant_positif",
        ),
        db.UniqueConstraint(
            "hotel_id",
            "client_id",
            "date_debut",
            "date_fin",
            name="uq_reservations_doublon_exact",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(
        db.Integer,
        db.ForeignKey("hotels.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    client_id = db.Column(
        db.Integer,
        db.ForeignKey("clients.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    statut = db.Column(db.String(20), nullable=False, default="EN_ATTENTE")
    montant_total = db.Column(db.Numeric(10, 2), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    hotel = db.relationship("Hotel", back_populates="reservations")
    client = db.relationship("Client", back_populates="reservations")

    def __repr__(self):
        return f"<Reservation {self.id}: hotel={self.hotel_id}, client={self.client_id}>"
