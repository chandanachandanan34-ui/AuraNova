
from datetime import datetime

from app.extensions import db


class AIReport(db.Model):

    __tablename__ = "ai_reports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    symptoms = db.Column(
        db.Text,
        nullable=False
    )

    condition = db.Column(
        db.Text,
        nullable=False
    )

    severity = db.Column(
        db.String(30),
        nullable=False
    )

    doctor = db.Column(
        db.String(150),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.now
    )

    patient = db.relationship(
        "User",
        backref="ai_reports"
    )