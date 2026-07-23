from datetime import datetime

from flask_login import UserMixin

from app.extensions import db


class User(UserMixin, db.Model):

    __tablename__ = "users"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    full_name = db.Column(
        db.String(100),
        nullable=False
    )


    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )


    password = db.Column(
        db.String(255),
        nullable=False
    )


    role = db.Column(
        db.String(20),
        nullable=False
    )

    phone = db.Column(
        db.String(20)
)

    gender = db.Column(
        db.String(20)
)

    blood_group = db.Column(
        db.String(10)
)

    address = db.Column(
        db.String(255)
)

    date_of_birth = db.Column(
        db.Date
)


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    appointments = db.relationship(
        "Appointment",
        back_populates="patient",
        lazy=True,
        cascade="all, delete-orphan"
    )