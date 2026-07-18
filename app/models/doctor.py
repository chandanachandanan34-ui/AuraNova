"""
Doctor model.
"""

from datetime import datetime

from app.extensions import db


class Doctor(db.Model):
    """
    Doctor information.
    """

    __tablename__ = "doctors"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    specialization = db.Column(
        db.String(100),
        nullable=False
    )

    qualification = db.Column(
        db.String(100),
        nullable=False
    )

    experience = db.Column(
        db.Integer,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    available = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Doctor {self.full_name}>"