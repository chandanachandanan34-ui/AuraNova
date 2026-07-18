"""
Flask-Login user loader.
"""

from app.extensions import login_manager
from app.models import User


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database by ID.
    """

    return User.query.get(int(user_id))