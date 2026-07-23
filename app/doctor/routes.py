"""
Doctor portal routes.
"""

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    abort,
)

from flask_login import (
    login_required,
    current_user,
)

from app.extensions import db
from app.models import (
    User,
    Doctor,
    Appointment,
    MedicalRecord,
    PatientDocument,
)
from app.doctor.forms import (
    DoctorProfileForm,
    MedicalRecordForm,
)

bp = Blueprint("doctor", __name__)


@bp.route("/dashboard")
@login_required
def dashboard():
    """
    Doctor Dashboard.
    """

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first()


    appointments = []


    if doctor:

        appointments = Appointment.query.filter_by(
            doctor_id=doctor.id
        ).all()


    total = len(appointments)


    pending = len(
        [
            a for a in appointments
            if a.status == "Pending"
        ]
    )


    approved  = len(
        [
            a for a in appointments
            if a.status == "Approved"
        ]
    )


    return render_template(
        "doctor/dashboard.html",
        doctor=doctor,
        appointments=appointments,
        total=total,
        pending=pending,
        approved=approved 
    )


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    Doctor Profile.
    """

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first()

    form = DoctorProfileForm()

    if form.validate_on_submit():

        doctor.specialization = form.specialization.data
        doctor.qualification = form.qualification.data
        doctor.experience = form.experience.data
        doctor.phone = form.phone.data

        db.session.commit()

        flash(
            "Profile updated successfully!",
            "success"
        )

        return redirect(
            url_for("doctor.profile")
        )

    if doctor:

        form.specialization.data = doctor.specialization
        form.qualification.data = doctor.qualification
        form.experience.data = doctor.experience
        form.phone.data = doctor.phone

    return render_template(
        "doctor/profile.html",
        form=form,
        doctor=doctor
    )

# -------------------------
# Doctor Appointments
# -------------------------

@bp.route("/appointments")
@login_required
def appointments():

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    appointments = Appointment.query.filter_by(
        doctor_id=doctor.id
    ).order_by(
        Appointment.appointment_date
    ).all()

    return render_template(
        "doctor/appointments.html",
        doctor=doctor,
        appointments=appointments
    )


# -------------------------
# Accept Appointment
# -------------------------

@bp.route("/accept/<int:id>")
@login_required
def accept_appointment(id):

    appointment = Appointment.query.get_or_404(id)

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    if appointment.doctor_id != doctor.id:

        abort(403)

    appointment.status = "Confirmed"

    db.session.commit()

    flash(
        "Appointment confirmed successfully!",
        "success"
    )

    return redirect(
        url_for("doctor.appointments")
    )


# -------------------------
# Reject Appointment
# -------------------------

@bp.route("/reject/<int:id>")
@login_required
def reject_appointment(id):

    appointment = Appointment.query.get_or_404(id)

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    if appointment.doctor_id != doctor.id:

        abort(403)

    appointment.status = "Rejected"

    db.session.commit()

    flash(
        "Appointment rejected.",
        "warning"
    )

    return redirect(
        url_for("doctor.appointments")
    )


# -------------------------
# Complete Appointment
# -------------------------

@bp.route("/complete/<int:id>")
@login_required
def complete_appointment(id):

    appointment = Appointment.query.get_or_404(id)

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    if appointment.doctor_id != doctor.id:

        abort(403)

    appointment.status = "Completed"

    db.session.commit()

    flash(
        "Appointment marked as completed.",
        "success"
    )

    return redirect(
        url_for("doctor.appointments")
    )
       

# -------------------------
# Add Medical Record
# -------------------------

@bp.route("/medical-record/<int:id>", methods=["GET", "POST"])
@login_required
def add_medical_record(id):

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    appointment = Appointment.query.get_or_404(id)

    if appointment.doctor_id != doctor.id:
        abort(403)

    existing = MedicalRecord.query.filter_by(
        appointment_id=appointment.id
    ).first()

    if existing:

        flash(
            "Medical record already exists.",
            "warning"
        )

        return redirect(
            url_for("doctor.appointments")
        )

    form = MedicalRecordForm()

    if form.validate_on_submit():

        record = MedicalRecord(

            patient_id=appointment.patient_id,

            doctor_id=doctor.id,

            appointment_id=appointment.id,

            diagnosis=form.diagnosis.data,

            symptoms=form.symptoms.data,

            prescription=form.prescription.data,

            notes=form.notes.data,
        )

        db.session.add(record)

        appointment.status = "Completed"

        db.session.commit()

        flash(
            "Medical Record saved successfully!",
            "success"
        )

        return redirect(
            url_for("doctor.appointments")
        )

    return render_template(
        "doctor/add_medical_record.html",
        form=form,
        appointment=appointment
    )

# -------------------------
# Doctor Medical Records
# -------------------------

@bp.route("/medical-records")
@login_required
def medical_records():

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    records = MedicalRecord.query.filter_by(
        doctor_id=doctor.id
    ).order_by(
        MedicalRecord.created_at.desc()
    ).all()

    return render_template(
        "doctor/medical_records.html",
        records=records
    )

# -------------------------
# Doctor View Patient Details
# -------------------------

@bp.route("/patient/<int:id>")
@login_required
def patient_details(id):

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    patient = User.query.filter_by(
        id=id,
        role="patient"
    ).first_or_404()

    appointments = Appointment.query.filter_by(
        patient_id=patient.id
    ).order_by(
        Appointment.created_at.desc()
    ).all()

    medical_records = MedicalRecord.query.filter_by(
        patient_id=patient.id
    ).order_by(
        MedicalRecord.created_at.desc()
    ).all()

    documents = PatientDocument.query.filter_by(
        patient_id=patient.id
    ).order_by(
        PatientDocument.uploaded_at.desc()
    ).all()

    return render_template(
        "doctor/patient_details.html",
        patient=patient,
        appointments=appointments,
        medical_records=medical_records,
        documents=documents
    )