"""
Patient portal routes.
"""

from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("patient", __name__)


@bp.route("/dashboard")
@login_required
def dashboard():
    """
    Display the patient dashboard.
    """

    return render_template("patient/dashboard.html")