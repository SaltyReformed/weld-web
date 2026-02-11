"""
Main Flask application for the Ironforge Welding website.

This module initializes the Flask app, registers blueprints for each
page route, configures logging, sets up CSRF protection, rate limiting,
and Flask-Mail, adds security headers, and defines custom error handlers.

Run this file directly to start the development server.

Usage:
    python app.py
"""

import logging
import os
from datetime import datetime

from flask import Flask, render_template

from config import CONFIG_MAP
from extensions import csrf, limiter, mail


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------


def configure_logging(app):
    """
    Configure application-wide logging.

    Sets up a stream handler with a consistent format.  The log level
    is DEBUG when the app is in debug mode, otherwise INFO.

    Args:
        app: The Flask application instance.
    """
    log_level = logging.DEBUG if app.debug else logging.INFO

    # Create a formatter that includes timestamp, level, and message.
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Stream handler for console output.
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)

    # Attach handler to the Flask app logger.
    app.logger.setLevel(log_level)
    app.logger.addHandler(stream_handler)

    app.logger.info("Logging configured at %s level.", logging.getLevelName(log_level))


# ---------------------------------------------------------------------------
# Security headers
# ---------------------------------------------------------------------------


def register_security_headers(app):
    """
    Add standard security headers to every HTTP response.

    These headers mitigate common web vulnerabilities such as
    clickjacking, MIME-type sniffing, and cross-site scripting.

    Args:
        app: The Flask application instance.
    """

    @app.after_request
    def set_security_headers(response):
        """Inject security headers into every response."""
        # Prevent the browser from MIME-sniffing the content type.
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Block the page from being rendered inside an iframe (clickjacking).
        response.headers["X-Frame-Options"] = "SAMEORIGIN"

        # Limit referrer information sent with outbound requests.
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Instruct browsers to only connect via HTTPS in the future.
        # max-age is one year (31 536 000 seconds).
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

        # Basic Content-Security-Policy — adjust as real assets are added.
        # Allows self-hosted resources, Google Fonts, and inline styles
        # needed by Flask/Jinja (flash messages, etc.).
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "media-src 'self'; "
            "frame-ancestors 'self';"
        )

        # Prevent browsers from caching sensitive pages.
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )

        return response

    app.logger.info("Security headers registered.")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------


def create_app(config_name=None):
    """
    Application factory that creates and configures the Flask instance.

    Uses the factory pattern so the app can be instantiated with different
    configurations for development, testing, and production.

    Args:
        config_name: Key into CONFIG_MAP (e.g. 'development', 'production').
                     Defaults to the FLASK_ENV environment variable or
                     'development' if not set.

    Returns:
        A fully configured Flask application instance.
    """
    app = Flask(__name__)

    # Determine which configuration to use.
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    config_class = CONFIG_MAP.get(config_name)
    if config_class is None:
        # Fall back to development if an unknown config name is provided.
        logging.warning(
            "Unknown config name '%s'. Falling back to development.",
            config_name,
        )
        config_class = CONFIG_MAP["development"]

    app.config.from_object(config_class)

    # Set up logging before anything else.
    configure_logging(app)
    app.logger.info("App created with '%s' configuration.", config_name)

    # Initialise extensions.
    csrf.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)
    app.logger.info("CSRF protection, rate limiter, and Flask-Mail initialised.")

    # Log mail status so it's obvious in the console whether email
    # sending is active or suppressed.
    if app.config.get("MAIL_ENABLED"):
        app.logger.info(
            "Email sending ENABLED — outbound via %s:%s.",
            app.config.get("MAIL_SERVER"),
            app.config.get("MAIL_PORT"),
        )
    else:
        app.logger.info(
            "Email sending DISABLED — submissions will be logged only. "
            "Set MAIL_ENABLED=true to activate."
        )

    # Register blueprints (route modules).
    register_blueprints(app)

    # Register error handlers.
    register_error_handlers(app)

    # Add security headers to every response.
    register_security_headers(app)

    # Inject the current year into all templates for the footer copyright.
    @app.context_processor
    def inject_current_year():
        """Make the current year available to every template."""
        return {"current_year": datetime.now().year}

    return app


# ---------------------------------------------------------------------------
# Blueprint registration
# ---------------------------------------------------------------------------


def register_blueprints(app):
    """
    Import and register all route blueprints with the Flask app.

    Each blueprint is defined in its own module inside the routes package.
    Importing here avoids circular imports.

    Args:
        app: The Flask application instance.
    """
    # Local imports to avoid circular dependency issues.
    from routes.home import home_bp  # pylint: disable=import-outside-toplevel
    from routes.services import services_bp  # pylint: disable=import-outside-toplevel
    from routes.contact import contact_bp  # pylint: disable=import-outside-toplevel
    from routes.gallery import gallery_bp  # pylint: disable=import-outside-toplevel

    app.register_blueprint(home_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(gallery_bp)

    app.logger.info("All blueprints registered successfully.")


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------


def register_error_handlers(app):
    """
    Register custom error-handling pages for common HTTP errors.

    Args:
        app: The Flask application instance.
    """

    @app.errorhandler(404)
    def page_not_found(error):
        """Render a custom 404 page."""
        app.logger.warning("404 Not Found: %s", error)
        return render_template("errors/404.html"), 404

    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Handle rate-limit (429 Too Many Requests) responses."""
        app.logger.warning("429 Rate limit hit: %s", error)
        return render_template("errors/429.html"), 429

    @app.errorhandler(500)
    def internal_server_error(error):
        """Render a custom 500 page."""
        app.logger.error("500 Internal Server Error: %s", error)
        return render_template("errors/500.html"), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Create the app with the environment-appropriate config.
    application = create_app()
    application.logger.info("Starting development server on http://127.0.0.1:5000")
    application.run(host="127.0.0.1", port=5000)
