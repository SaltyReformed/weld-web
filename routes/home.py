"""
Home page blueprint for the Ironforge Welding website.

Handles the root URL and renders the hero landing page.
Provides placeholder testimonial data for the social proof section.
"""

import logging

from flask import Blueprint, render_template

# Module-level logger for this blueprint.
logger = logging.getLogger(__name__)

# Define the blueprint with a url_prefix of "/" (site root).
home_bp = Blueprint("home", __name__)

# Placeholder testimonials for the prototype.
# In production these could come from a database, Google Reviews API,
# or a lightweight CMS.
TESTIMONIALS = [
    {
        "id": "t1",
        "name": "Mike Henderson",
        "role": "Ranch Owner, Henderson Cattle Co.",
        "quote": (
            "Called Ironforge for an emergency repair on our cattle chute. "
            "He drove out the same afternoon, welded it solid, and charged "
            "a fair price. That chute's tougher now than the day it was new."
        ),
        "rating": 5,
    },
    {
        "id": "t2",
        "name": "Sarah Cortez",
        "role": "General Contractor, Cortez Builds",
        "quote": (
            "We sub out all our structural steel and railing work to "
            "Ironforge. Every weld passes inspection the first time, "
            "and he's never missed a deadline on us. Reliable as it gets."
        ),
        "rating": 5,
    },
    {
        "id": "t3",
        "name": "Jake Drummond",
        "role": "Homeowner",
        "quote": (
            "I wanted a custom fire pit for the backyard and Ironforge "
            "knocked it out of the park. He listened to what I wanted, "
            "offered some design ideas, and delivered a piece that "
            "looks like it cost three times what I paid."
        ),
        "rating": 5,
    },
]


@home_bp.route("/")
def index():
    """
    Render the home / hero landing page.

    Passes placeholder testimonials to the template for the
    social proof section.

    Returns:
        Rendered HTML for the home page.
    """
    logger.info("Home page requested.")
    return render_template("home.html", testimonials=TESTIMONIALS)
