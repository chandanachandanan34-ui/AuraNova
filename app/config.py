"""
Application configuration settings.

Configuration is loaded from environment variables via python-dotenv.
See .env.example for required variables.
"""

import os
from pathlib import Path

# Project root directory (parent of app/)
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Base configuration shared across all environments."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # MySQL connection string using PyMySQL driver
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI",
        "mysql+pymysql://username:password@localhost:3306/aauranova",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload directory
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
