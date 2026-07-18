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
from app.models import User

bp = Blueprint("auth", __name__)


@bp.route("/")
def auth_home():
    """
    Test route for authentication blueprint.
    """
    return "Auth Blueprint Working"


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

        # Check empty fields
        if not full_name or not email or not password or not confirm_password:
            flash("Please fill in all fields.", "danger")
            return render_template("auth/register.html")

        # Password match
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        # Email already exists
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
            role="patient",
        )

        # Save user
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

        # Find user
        user = User.query.filter_by(email=email).first()

        # Invalid email
        if user is None:
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html")

        # Check password
        if not check_password_hash(user.password, password):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html")

        # Login user
        login_user(user)

        flash("Login successful!", "success")

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