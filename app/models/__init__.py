"""
Database models.
"""

from app.models.user import User
from app.models.appointment import Appointment

__all__ = [
    "User",
    "Appointment",
]