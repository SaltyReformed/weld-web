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
    """

    # Pull secret key from environment variable, fall back to dev default.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    DEBUG = False
    TESTING = False


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
    """Testing configuration with testing mode enabled."""

    TESTING = True


# Map environment names to configuration classes for easy lookup.
CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
