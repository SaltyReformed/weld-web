"""
Home page blueprint for the Ironforge Welding website.

Handles the root URL and renders the hero landing page.
"""

import logging

from flask import Blueprint, render_template

# Module-level logger for this blueprint.
logger = logging.getLogger(__name__)

# Define the blueprint with a url_prefix of "/" (site root).
home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    """
    Render the home / hero landing page.

    Returns:
        Rendered HTML for the home page.
    """
    logger.info("Home page requested.")
    return render_template("home.html")
