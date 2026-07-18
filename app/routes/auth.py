"""
Authentication routes.
"""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
)

from app.extensions import db
from app.forms.auth_forms import RegisterForm, LoginForm
from app.models.user import User
from app.models.doctor import Doctor


bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
)


@bp.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_user:
            flash(
                "Email already exists.",
                "danger",
            )
            return redirect(
                url_for("auth.register")
            )

        user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=generate_password_hash(
                form.password.data
            ),
            role=form.role.data,
        )

        db.session.add(user)
        db.session.commit()

        if user.role == "doctor":

            doctor = Doctor(
                user_id=user.id,
                full_name=user.full_name,
                specialization="General",
                qualification="Not Added",
                experience=0,
                email=user.email,
                phone="Not Added",
            )

            db.session.add(doctor)
            db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success",
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/register.html",
        form=form,
    )


@bp.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if (
            user
            and check_password_hash(
                user.password,
                form.password.data,
            )
        ):

            login_user(user)

            flash(
                "Login successful.",
                "success",
            )

            return redirect(
                url_for("main.index")
            )

        flash(
            "Invalid email or password.",
            "danger",
        )

    return render_template(
        "auth/login.html",
        form=form,
    )


@bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "success",
    )

    return redirect(
        url_for("auth.login")
    )