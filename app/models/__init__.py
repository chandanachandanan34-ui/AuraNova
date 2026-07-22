"""
Database models.
"""

from app.models.user import User
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.medical_record import MedicalRecord
from app.models.ai_report import AIReport
from app.models.patient_document import PatientDocument

__all__ = [
    "User",
    "Appointment",
    "Doctor",
    "MedicalRecord",
    "AIReport",
]