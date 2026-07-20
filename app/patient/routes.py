"""
Patient routes.
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from datetime import datetime

from app.extensions import db
from app.models.doctor import Doctor
from app.models.appointment import Appointment


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
        upcoming=upcoming
    )



@bp.route("/doctors")
@login_required
def doctors():

    search = request.args.get("search", "")

    if search:

        doctors = Doctor.query.filter(
            Doctor.specialization.ilike(f"%{search}%"),
            Doctor.available == True
        ).all()

    else:

        doctors = Doctor.query.filter_by(
            available=True
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