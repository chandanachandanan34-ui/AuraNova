"""
Doctor forms.
"""

from flask_wtf import FlaskForm

from wtforms import (
    SelectField,
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
)

from wtforms.validators import (
    DataRequired,
    NumberRange,
)


class DoctorProfileForm(FlaskForm):

    specialization = SelectField(
        "Specialization",
        choices=[
            ("General Physician", "General Physician"),
            ("Cardiologist", "Cardiologist"),
            ("Dermatologist", "Dermatologist"),
            ("Neurologist", "Neurologist"),
            ("Orthopedic", "Orthopedic"),
            ("Pediatrician", "Pediatrician"),
            ("Psychiatrist", "Psychiatrist"),
            ("Gynecologist", "Gynecologist"),
            ("ENT Specialist", "ENT Specialist"),
            ("Ophthalmologist", "Ophthalmologist"),
        ],
        validators=[DataRequired()]
    )

    qualification = SelectField(
        "Qualification",
        choices=[
            ("MBBS", "MBBS"),
            ("MD", "MD"),
            ("MS", "MS"),
            ("DM", "DM"),
            ("MCh", "MCh"),
            ("BDS", "BDS"),
            ("MDS", "MDS"),
            ("BHMS", "BHMS"),
            ("BAMS", "BAMS"),
            ("BUMS", "BUMS"),
        ],
        validators=[DataRequired()]
    )

    experience = IntegerField(
        "Experience (Years)",
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[DataRequired()]
    )

    submit = SubmitField("Update Profile")


# ----------------------------------
# Medical Record Form
# ----------------------------------

class MedicalRecordForm(FlaskForm):

    diagnosis = TextAreaField(
        "Diagnosis",
        validators=[DataRequired()]
    )

    symptoms = TextAreaField(
        "Symptoms"
    )

    prescription = TextAreaField(
        "Prescription"
    )

    notes = TextAreaField(
        "Doctor Notes"
    )

    submit = SubmitField(
        "Save Medical Record"
    )