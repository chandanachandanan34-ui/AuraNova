"""
Doctor portal routes.
"""

from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
)

from flask_login import (
    login_required,
    current_user,
)

from app.extensions import db
from app.models import Doctor, Appointment
from app.doctor.forms import DoctorProfileForm

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


    confirmed = len(
        [
            a for a in appointments
            if a.status == "Confirmed"
        ]
    )


    return render_template(
        "doctor/dashboard.html",
        doctor=doctor,
        appointments=appointments,
        total=total,
        pending=pending,
        confirmed=confirmed
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
# Confirm Appointment
# -------------------------

@bp.route("/appointment/<int:id>/confirm")
@login_required
def confirm_appointment(id):

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    appointment = Appointment.query.get_or_404(id)

    if appointment.doctor_id != doctor.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("doctor.appointments"))

    appointment.status = "Confirmed"

    db.session.commit()

    flash(
        "Appointment confirmed successfully!",
        "success",
    )

    return redirect(
        url_for("doctor.appointments")
    )


# -------------------------
# Reject Appointment
# -------------------------

@bp.route("/appointment/<int:id>/reject")
@login_required
def reject_appointment(id):

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    appointment = Appointment.query.get_or_404(id)

    if appointment.doctor_id != doctor.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("doctor.appointments"))

    appointment.status = "Rejected"

    db.session.commit()

    flash(
        "Appointment rejected successfully!",
        "success",
    )

    return redirect(
        url_for("doctor.appointments")
    )