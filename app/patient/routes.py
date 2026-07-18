"""
Patient portal routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db

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

        # Update current user's information
        current_user.full_name = full_name
        current_user.email = email

        # Save changes to the database
        db.session.commit()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("patient.profile"))

    return render_template("patient/edit_profile.html")