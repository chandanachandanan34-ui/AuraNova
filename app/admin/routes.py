"""
Admin routes.
"""
from flask import abort
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from werkzeug.security import generate_password_hash

from app.extensions import db
from flask_login import login_required

from app.models import (
    User,
    Doctor,
    Appointment,
    AIReport,
    PatientDocument,
)
from flask_mail import Message
from app.extensions import mail

bp = Blueprint("admin", __name__)


@bp.route("/dashboard")
@login_required
def dashboard():

    total_patients = User.query.filter_by(role="patient").count()

    total_doctors = Doctor.query.count()

    total_appointments = Appointment.query.count()

    total_ai_reports = AIReport.query.count()

    total_documents = PatientDocument.query.count()

    pending = Appointment.query.filter_by(
        status="Pending"
    ).count()

    approved = Appointment.query.filter_by(
        status="Approved"
    ).count()

    completed = Appointment.query.filter_by(
        status="Completed"
    ).count()

    cancelled = Appointment.query.filter_by(
        status="Cancelled"
    ).count()

    return render_template(
        "admin/dashboard.html",
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_appointments=total_appointments,
        total_ai_reports=total_ai_reports,
        total_documents=total_documents,
        pending=pending,
        approved=approved,
        completed=completed,
        cancelled=cancelled,
    )
@bp.route("/add-doctor", methods=["GET", "POST"])
@login_required
def add_doctor():

    if request.method == "POST":

        email = request.form["email"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:

            flash("Email already exists.", "danger")

            return redirect(url_for("admin.add_doctor"))

        user = User(
            full_name=request.form["full_name"],
            email=email,
            password=generate_password_hash(request.form["password"]),
            role="doctor",
        )

        db.session.add(user)
        db.session.commit()

        doctor = Doctor(
            user_id=user.id,
            full_name=request.form["full_name"],
            specialization=request.form["specialization"],
            qualification=request.form["qualification"],
            experience=request.form["experience"] or 0,
            email=email,
            phone=request.form["phone"],
            available=True,
        )

        db.session.add(doctor)
        db.session.commit()

        flash("Doctor added successfully!", "success")

        return redirect(url_for("admin.view_doctors"))

    return render_template("admin/add_doctor.html")


@bp.route("/view-doctors")
@login_required
def view_doctors():

    doctors = Doctor.query.all()

    return render_template(
        "admin/view_doctors.html",
        doctors=doctors,
    )


@bp.route("/manage-appointments")
@login_required
def manage_appointments():

    appointments = Appointment.query.all()

    return render_template(
        "admin/manage_appointments.html",
        appointments=appointments,
    )

@bp.route("/approve-appointment/<int:id>")
@login_required
def approve_appointment(id):

    appointment = Appointment.query.get_or_404(id)

    appointment.status = "Approved"

    db.session.commit()

    try:

        msg = Message(
            subject="AuraNova - Appointment Approved",
            recipients=[appointment.patient.email]
        )

        msg.body = f"""
Hello {appointment.patient.full_name},

Great news!

Your appointment has been APPROVED.

Doctor:
Dr. {appointment.doctor.full_name}

Date:
{appointment.appointment_date}

Time:
{appointment.appointment_time}

Please visit the hospital/clinic on time.

Thank you for choosing AuraNova.

Regards,
AuraNova Healthcare Team
"""

        mail.send(msg)

    except Exception as e:

        print("Email Error:", e)

    flash(
        "Appointment approved and email sent!",
        "success"
    )

    return redirect(
        url_for("admin.manage_appointments")
    )

@bp.route("/reject-appointment/<int:id>")
@login_required
def reject_appointment(id):

    appointment = Appointment.query.get_or_404(id)

    appointment.status = "Rejected"

    db.session.commit()

    try:

        msg = Message(
            subject="AuraNova - Appointment Rejected",
            recipients=[appointment.patient.email]
        )

        msg.body = f"""
Hello {appointment.patient.full_name},

We regret to inform you that your appointment has been REJECTED.

Doctor:
Dr. {appointment.doctor.full_name}

Date:
{appointment.appointment_date}

Time:
{appointment.appointment_time}

You may log in to AuraNova and book another appointment.

Regards,
AuraNova Healthcare Team
"""

        mail.send(msg)

    except Exception as e:

        print("Email Error:", e)

    flash(
        "Appointment rejected and email sent!",
        "warning"
    )

    return redirect(
        url_for("admin.manage_appointments")
    )


@bp.route("/edit-doctor/<int:id>", methods=["GET", "POST"])
@login_required
def edit_doctor(id):

    doctor = Doctor.query.get_or_404(id)

    if request.method == "POST":

        doctor.full_name = request.form["full_name"]
        doctor.specialization = request.form["specialization"]
        doctor.qualification = request.form["qualification"]
        doctor.experience = request.form["experience"]
        doctor.phone = request.form["phone"]

        db.session.commit()

        flash(
            "Doctor updated successfully!",
            "success",
        )

        return redirect(
            url_for("admin.view_doctors")
        )

    return render_template(
        "admin/edit_doctor.html",
        doctor=doctor,
    )

@bp.route("/delete-doctor/<int:id>")
@login_required
def delete_doctor(id):

    doctor = Doctor.query.get_or_404(id)

    user = User.query.get(doctor.user_id)

    db.session.delete(doctor)

    if user:
        db.session.delete(user)

    db.session.commit()

    flash(
        "Doctor deleted successfully!",
        "success",
    )

    return redirect(
        url_for("admin.view_doctors")
    )