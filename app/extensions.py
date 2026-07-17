"""
Shared Flask extension instances.

Extensions are initialized here and bound to the application
inside the application factory (create_app).
"""

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
