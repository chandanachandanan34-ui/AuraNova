"""
AuraNova application factory.

Creates and configures the Flask application instance using
the Application Factory Pattern.
"""

import os

from dotenv import load_dotenv
from flask import Flask

from app.config import config
from app.extensions import db, login_manager, migrate


def create_app(config_name=None):
    """
    Application factory entry point.

    Args:
        config_name: Configuration key ('development', 'production', 'testing').
                     Defaults to FLASK_ENV environment variable or 'development'.

    Returns:
        Configured Flask application instance.
    """

    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)

    # Resolve configuration profile
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app.config.from_object(
        config.get(config_name, config["default"])
    )

    # Initialize extensions
    db.init_app(app)

    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Import all database models
    

    # Register Flask-Login user loader
    from app.utils import login  # noqa: F401

    # Import models so Flask-Migrate can detect them
    from app.models import User  # noqa: F401

    # Register blueprints
    _register_blueprints(app)

    # Register core routes
    _register_core_routes(app)

    return app


def _register_blueprints(app):
    """
    Register all application blueprints.
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
    Register application-wide routes.
    """

    @app.context_processor
    def inject_globals():
        """
        Inject variables available in all templates.
        """

        from datetime import UTC, datetime

        return {
            "current_year": datetime.now(UTC).year
        }


    @app.route("/")
    def index():
        """
        Application homepage.
        """

        from flask import render_template

        return render_template("index.html")