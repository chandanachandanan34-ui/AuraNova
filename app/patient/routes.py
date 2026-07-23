"""
Patient routes.
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from datetime import datetime

from app.extensions import db
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.medical_record import MedicalRecord
from app.models.patient_document import PatientDocument

from werkzeug.utils import secure_filename
from sqlalchemy import or_
import os


bp = Blueprint("patient", __name__)


# -------------------------
# Patient Dashboard
# -------------------------

@bp.route("/dashboard")
@login_required
def dashboard():

    appointments = Appointment.query.filter_by(
        patient_id=current_user.id
    ).order_by(
        Appointment.created_at.desc()
    ).all()


    total_appointments = Appointment.query.filter_by(
        patient_id=current_user.id
    ).count()


    pending_appointments = Appointment.query.filter_by(
        patient_id=current_user.id,
        status="Pending"
    ).count()


    completed_appointments = Appointment.query.filter_by(
        patient_id=current_user.id,
        status="Completed"
    ).count()


    total_doctors = Doctor.query.count()
    total_records = MedicalRecord.query.filter_by(
        patient_id=current_user.id
    ).count()

    total_documents = PatientDocument.query.filter_by(
        patient_id=current_user.id
    ).count()


    upcoming = Appointment.query.filter_by(
        patient_id=current_user.id,
        status="Pending"
    ).first()



    return render_template(
        "patient/dashboard.html",
        user=current_user,
        appointments=appointments,
        total_appointments=total_appointments,
        pending=pending_appointments,
        completed=completed_appointments,
        doctors=total_doctors,
        total_records=total_records,
        total_documents=total_documents,
        upcoming=upcoming
    )



# -------------------------
# Available Doctors
# -------------------------

@bp.route("/doctors")
@login_required
def doctors():

    search = request.args.get("search", "").strip()

    if search:

        doctors = Doctor.query.filter(

            Doctor.available == True,

            or_(

                Doctor.full_name.ilike(f"%{search}%"),

                Doctor.specialization.ilike(f"%{search}%")

            )

        ).order_by(Doctor.full_name).all()

    else:

        doctors = Doctor.query.filter_by(
            available=True
        ).order_by(
            Doctor.full_name
        ).all()

    return render_template(
        "patient/doctors.html",
        doctors=doctors,
        search=search
    )

# -------------------------
# Book Appointment
# -------------------------

@bp.route("/book/<int:doctor_id>", methods=["GET", "POST"])
@login_required
def book_appointment(doctor_id):

    doctor = Doctor.query.get_or_404(doctor_id)


    if request.method == "POST":

        date = request.form.get("date")
        time = request.form.get("time")
        reason = request.form.get("reason")


        appointment = Appointment(

            patient_id=current_user.id,

            doctor_id=doctor.id,

            appointment_date=datetime.strptime(
                date,
                "%Y-%m-%d"
            ).date(),

            appointment_time=datetime.strptime(
                time,
                "%H:%M"
            ).time(),

            reason=reason,

            status="Pending"

        )


        db.session.add(appointment)

        db.session.commit()


        flash(
            "Appointment booked successfully!",
            "success"
        )


        return redirect(
            url_for("patient.appointments")
        )


    return render_template(
        "patient/book_appointment.html",
        doctor=doctor
    )



# -------------------------
# My Appointments
# -------------------------

@bp.route("/appointments")
@login_required
def appointments():

    appointments = Appointment.query.filter_by(
        patient_id=current_user.id
    ).order_by(
        Appointment.created_at.desc()
    ).all()


    return render_template(
        "patient/appointments.html",
        appointments=appointments
    )



# -------------------------
# Cancel Appointment
# -------------------------

@bp.route("/cancel/<int:id>")
@login_required
def cancel_appointment(id):

    appointment = Appointment.query.get_or_404(id)


    if appointment.patient_id != current_user.id:

        flash(
            "Unauthorized action!",
            "danger"
        )

        return redirect(
            url_for("patient.appointments")
        )


    appointment.status = "Cancelled"

    db.session.commit()


    flash(
        "Appointment cancelled!",
        "warning"
    )


    return redirect(
        url_for("patient.appointments")
    )
    # -------------------------
# Patient Profile
# -------------------------

@bp.route("/profile")
@login_required
def profile():

    return render_template(
        "patient/profile.html",
        user=current_user
    )


# -------------------------
# Edit Patient Profile
# -------------------------

@bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    if request.method == "POST":

        current_user.full_name = request.form.get("full_name")
        current_user.email = request.form.get("email")
        current_user.phone = request.form.get("phone")
        current_user.gender = request.form.get("gender")
        current_user.blood_group = request.form.get("blood_group")
        current_user.address = request.form.get("address")

        dob = request.form.get("date_of_birth")

        if dob:
            current_user.date_of_birth = datetime.strptime(
                dob,
                "%Y-%m-%d"
            ).date()

        else:
            current_user.date_of_birth = None

        db.session.commit()

        flash(
            "Profile updated successfully!",
            "success"
        )

        return redirect(
            url_for("patient.profile")
        )

    return render_template(
        "patient/edit_profile.html"
    )
# -------------------------
# Patient Medical Records
# -------------------------

@bp.route("/medical-records")
@login_required
def medical_records():

    records = MedicalRecord.query.filter_by(
        patient_id=current_user.id
    ).order_by(
        MedicalRecord.created_at.desc()
    ).all()

    return render_template(
        "patient/medical_records.html",
        records=records
    )

# -------------------------
# Upload Patient Document
# -------------------------

@bp.route("/upload-document", methods=["GET", "POST"])
@login_required
def upload_document():

    if request.method == "POST":

        title = request.form.get("title")

        description = request.form.get("description")

        file = request.files.get("file")

        if not file or file.filename == "":

            flash(
                "Please select a file.",
                "danger"
            )

            return redirect(
                url_for("patient.upload_document")
            )

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            bp.root_path,
            "..",
            "..",
            "uploads",
            filename
        )

        file.save(filepath)

        document = PatientDocument(

            patient_id=current_user.id,

            title=title,

            description=description,

            file_name=filename

        )

        db.session.add(document)

        db.session.commit()

        flash(
            "Document uploaded successfully!",
            "success"
        )

        return redirect(
            url_for("patient.upload_document")
        )

    documents = PatientDocument.query.filter_by(
        patient_id=current_user.id
    ).order_by(
        PatientDocument.uploaded_at.desc()
    ).all()

    return render_template(
        "patient/upload_document.html",
        documents=documents
    )

# -------------------------
# Download Patient Document
# -------------------------

@bp.route("/download-document/<int:id>")
@login_required
def download_document(id):

    document = PatientDocument.query.get_or_404(id)

    if document.patient_id != current_user.id:

        flash(
            "Unauthorized access!",
            "danger"
        )

        return redirect(
            url_for("patient.upload_document")
        )

    filepath = os.path.join(
        bp.root_path,
        "..",
        "..",
        "uploads",
        document.file_name
    )

    return send_file(
        filepath,
        as_attachment=True
    )

# -------------------------
# Delete Patient Document
# -------------------------

@bp.route("/delete-document/<int:id>")
@login_required
def delete_document(id):

    document = PatientDocument.query.get_or_404(id)

    if document.patient_id != current_user.id:

        flash(
            "Unauthorized access!",
            "danger"
        )

        return redirect(
            url_for("patient.upload_document")
        )

    filepath = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        document.file_name
    )

    if os.path.exists(filepath):
        os.remove(filepath)

    db.session.delete(document)
    db.session.commit()

    flash(
        "Document deleted successfully!",
        "success"
    )

    return redirect(
        url_for("patient.upload_document")
    )