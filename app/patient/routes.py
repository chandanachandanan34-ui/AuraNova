"""
Patient portal routes.
"""

from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Appointment

bp = Blueprint("patient", __name__)


@bp.route("/dashboard")
@login_required
def dashboard():
    """
    Display the patient dashboard.
    """
    return render_template("patient/dashboard.html")


@bp.route("/profile")
@login_required
def profile():
    """
    Display the patient's profile.
    """
    return render_template("patient/profile.html")


@bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    """
    Edit the logged-in user's profile.
    """

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")

        # Basic validation
        if not full_name or not email:
            flash("All fields are required.", "danger")
            return render_template("patient/edit_profile.html")

        current_user.full_name = full_name
        current_user.email = email

        db.session.commit()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("patient.profile"))

    return render_template("patient/edit_profile.html")


@bp.route("/book-appointment", methods=["GET", "POST"])
@login_required
def book_appointment():
    """
    Book a new appointment.
    """

    if request.method == "POST":

        doctor_name = request.form.get("doctor_name")
        appointment_date = request.form.get("appointment_date")
        appointment_time = request.form.get("appointment_time")
        reason = request.form.get("reason")

        if not doctor_name or not appointment_date or not appointment_time or not reason:
            flash("Please fill in all fields.", "danger")
            return render_template("patient/book_appointment.html")

        appointment = Appointment(
            patient_id=current_user.id,
            doctor_name=doctor_name,
            appointment_date=datetime.strptime(
                appointment_date,
                "%Y-%m-%d"
            ).date(),
            appointment_time=datetime.strptime(
                appointment_time,
                "%H:%M"
            ).time(),
            reason=reason,
            status="Pending"
        )

        db.session.add(appointment)
        db.session.commit()

        flash("Appointment booked successfully!", "success")

        return redirect(url_for("patient.dashboard"))

    return render_template("patient/book_appointment.html")