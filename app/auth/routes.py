"""
Authentication routes.
"""

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from app.extensions import db
from app.models import User, Doctor

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    User Registration.
    """

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = "patient"

        # Check empty fields
        if not full_name or not email or not password or not confirm_password:
            flash("Please fill in all fields.", "danger")
            return render_template("auth/register.html")

        # Check password match
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        # Check existing email
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email is already registered.", "danger")
            return render_template("auth/register.html")

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create user
        new_user = User(
            full_name=full_name,
            email=email,
            password=hashed_password,
            role=role,
        )

        db.session.add(new_user)
        db.session.commit()

        

        flash("Registration successful! Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    User Login.
    """

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html")

        if not check_password_hash(user.password, password):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html")

        login_user(user)

        flash("Login successful!", "success")

        # Redirect based on role
        if user.role == "doctor":
            return redirect(url_for("doctor.dashboard"))

        elif user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("patient.dashboard"))

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    """
    Logout current user.
    """

    logout_user()

    flash("You have been logged out successfully.", "success")

    return redirect(url_for("auth.login"))