"""
Patient routes.
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint("patient", __name__)


@bp.route("/dashboard")
@login_required
def dashboard():
    """
    Patient dashboard.
    """
    return render_template(
        "patient/dashboard.html",
        user=current_user
    )