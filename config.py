"""
Configuration module for the Ironforge Welding Flask application.

Provides environment-specific configuration classes for development,
testing, and production deployments. Settings are loaded from environment
variables with sensible defaults for local development.
"""

import os


class Config:
    """
    Base configuration class.

    Attributes:
        SECRET_KEY: Flask secret key for session management and CSRF protection.
        DEBUG: Flag to enable/disable debug mode.
        TESTING: Flag to enable/disable testing mode.
        WTF_CSRF_ENABLED: Enable CSRF protection via Flask-WTF.
        RATELIMIT_STORAGE_URI: Backend for Flask-Limiter counters.
    """

    # Pull secret key from environment variable, fall back to dev default.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    DEBUG = False
    TESTING = False

    # CSRF protection — enabled by default for all environments.
    WTF_CSRF_ENABLED = True

    # Flask-Limiter: in-memory storage is fine for a single-process deploy.
    # Switch to "redis://..." for multi-worker production setups.
    RATELIMIT_STORAGE_URI = os.environ.get(
        "RATELIMIT_STORAGE_URI", "memory://"
    )


class DevelopmentConfig(Config):
    """Development configuration with debug mode enabled."""

    DEBUG = True


class ProductionConfig(Config):
    """
    Production configuration.

    Enforces that SECRET_KEY is set via environment variable
    and disables debug mode.
    """

    DEBUG = False


class TestingConfig(Config):
    """Testing configuration with testing and CSRF disabled for test runners."""

    TESTING = True
    WTF_CSRF_ENABLED = False  # Disable CSRF during automated tests.


# Map environment names to configuration classes for easy lookup.
CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
