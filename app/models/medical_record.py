"""
Medical Record model.
"""

from datetime import datetime

from app.extensions import db


class MedicalRecord(db.Model):

    __tablename__ = "medical_records"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=False
    )

    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey("appointments.id"),
        nullable=False
    )

    diagnosis = db.Column(
        db.Text,
        nullable=False
    )

    symptoms = db.Column(
        db.Text
    )

    prescription = db.Column(
        db.Text
    )

    notes = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    patient = db.relationship(
        "User",
        backref="medical_records"
    )

    doctor = db.relationship(
        "Doctor",
        backref="medical_records"
    )

    appointment = db.relationship(
        "Appointment",
        backref="medical_record",
        uselist=False
    )