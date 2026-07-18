"""
AuraNova application factory.

Creates and configures the Flask application instance using
the Application Factory Pattern.
"""

import os

from dotenv import load_dotenv
from flask import Flask, render_template

from app.config import config
from app.extensions import db, login_manager, migrate


def create_app(config_name=None):
    """
    Application factory entry point.
    """

    load_dotenv()

    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app.config.from_object(
        config.get(
            config_name,
            config["default"]
        )
    )

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Import models
    from app.models import User  # noqa: F401

    # Register user loader
    from app.utils import login  # noqa: F401

    _register_blueprints(app)
    _register_core_routes(app)

    return app


def _register_blueprints(app):
    """
    Register all blueprints.
    """

    from app.admin.routes import bp as admin_bp
    from app.ai.routes import bp as ai_bp
    from app.auth.routes import bp as auth_bp
    from app.doctor.routes import bp as doctor_bp
    from app.patient.routes import bp as patient_bp

    app.register_blueprint(
        auth_bp,
        url_prefix="/auth"
    )

    app.register_blueprint(
        admin_bp,
        url_prefix="/admin"
    )

    app.register_blueprint(
        doctor_bp,
        url_prefix="/doctor"
    )

    app.register_blueprint(
        patient_bp,
        url_prefix="/patient"
    )

    app.register_blueprint(
        ai_bp,
        url_prefix="/ai"
    )


def _register_core_routes(app):
    """
    Register common application routes.
    """

    @app.context_processor
    def inject_globals():
        from datetime import UTC, datetime

        return {
            "current_year": datetime.now(UTC).year
        }

    @app.route("/")
    def index():
        """
        Landing page.
        """
        return render_template("index.html")