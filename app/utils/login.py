"""
Flask-Login user loader placeholder.

Will be implemented when authentication models are added.
"""

from app.extensions import login_manager


@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID. Returns None until auth models are implemented."""
    return None
