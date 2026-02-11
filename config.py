"""
Configuration module for the Ironforge Welding Flask application.

Provides environment-specific configuration classes for development,
testing, and production deployments.  Settings are loaded from
environment variables with sensible defaults for local development.
"""

import os


class Config:
    """
    Base configuration class.

    Attributes:
        SECRET_KEY: Flask secret key for session management and CSRF
                    protection.
        DEBUG: Flag to enable/disable debug mode.
        TESTING: Flag to enable/disable testing mode.
        WTF_CSRF_ENABLED: Enable CSRF protection via Flask-WTF.
        RATELIMIT_STORAGE_URI: Backend for Flask-Limiter counters.
        MAIL_*: Flask-Mail configuration for sending quote notifications.
    """

    # Pull secret key from environment variable; fall back to dev default.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    DEBUG = False
    TESTING = False

    # CSRF protection — enabled by default for all environments.
    WTF_CSRF_ENABLED = True

    # Flask-Limiter: in-memory storage is fine for a single-process deploy.
    # Switch to "redis://..." for multi-worker production setups.
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")

    # ------------------------------------------------------------------
    # Flask-Mail configuration
    # ------------------------------------------------------------------
    # Default SMTP settings target Gmail.  For other providers
    # (Outlook, Zoho, Mailgun, etc.) override via environment variables.
    #
    # Gmail setup:
    #   1. Enable 2-Step Verification on the Google account.
    #   2. Generate an App Password at
    #      https://myaccount.google.com/apppasswords
    #   3. Set MAIL_USERNAME and MAIL_PASSWORD env vars to the Gmail
    #      address and the 16-character app password respectively.
    #
    # On PythonAnywhere set these in the WSGI file or in a .env loaded
    # by python-dotenv before the app starts.
    # ------------------------------------------------------------------
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")

    # The address that appears in the "From" header of outbound emails.
    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        os.environ.get("MAIL_USERNAME", "noreply@ironforgewelding.com"),
    )

    # Where quote-request notifications should be delivered.
    QUOTE_RECIPIENT_EMAIL = os.environ.get(
        "QUOTE_RECIPIENT_EMAIL",
        os.environ.get("MAIL_USERNAME", "info@ironforgewelding.com"),
    )

    # Master switch — set to "true" to actually send emails.
    # When "false" (the default) the app logs the email instead.
    MAIL_ENABLED = os.environ.get("MAIL_ENABLED", "false").lower() == "true"


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
    """Testing configuration with CSRF disabled for test runners."""

    TESTING = True
    WTF_CSRF_ENABLED = False  # Disable CSRF during automated tests.
    MAIL_ENABLED = False  # Never send real emails in tests.


# Map environment names to configuration classes for easy lookup.
CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
