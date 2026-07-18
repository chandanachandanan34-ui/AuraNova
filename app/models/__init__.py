"""
Database models.
"""

from app.models.user import User
from app.models.appointment import Appointment
from app.models.doctor import Doctor

__all__ = [
    "User",
    "Appointment",
]