"""
Database models.
"""

from app.models.user import User
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.medical_record import MedicalRecord

__all__ = [
    "User",
    "Appointment",
]