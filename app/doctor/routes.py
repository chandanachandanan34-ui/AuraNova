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
from app.models import Doctor
from app.doctor.forms import DoctorProfileForm

bp = Blueprint("doctor", __name__)


@bp.route("/dashboard")
@login_required
def dashboard():
    """
    Doctor Dashboard.
    """

    return render_template(
        "doctor/dashboard.html"
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