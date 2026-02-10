"""
Services page blueprint for the Ironforge Welding website.

Renders a gallery of welding services offered by the business.
Service data is defined here as placeholder content for the prototype.
"""

import logging

from flask import Blueprint, render_template

# Module-level logger for this blueprint.
logger = logging.getLogger(__name__)

services_bp = Blueprint("services", __name__)

# Placeholder service data for the prototype.
# In production this could come from a database or CMS.
# Each service includes an "image" key pointing to a file in static/images/.
# Replace the placeholder filenames with real photos as they become available.
SERVICES = [
    {
        "id": "mig",
        "title": "MIG Welding",
        "short_description": "Versatile wire-feed welding for steel and aluminum.",
        "long_description": (
            "Metal Inert Gas (MIG) welding is ideal for a wide range of "
            "projects — from automotive repair to structural fabrication. "
            "Fast, clean, and strong."
        ),
        "icon": "🔩",
        "image": "bright-welder.jpg",
    },
    {
        "id": "tig",
        "title": "TIG Welding",
        "short_description": "Precision welding for critical joints and thin materials.",
        "long_description": (
            "Tungsten Inert Gas (TIG) welding delivers the highest quality "
            "welds with pinpoint control. Perfect for stainless steel, "
            "aluminum, and decorative work."
        ),
        "icon": "⚡",
        "image": "close-welding.jpg",
    },
    {
        "id": "stick",
        "title": "Stick Welding",
        "short_description": "Rugged, portable welding for heavy structural work.",
        "long_description": (
            "Shielded Metal Arc Welding (SMAW) handles the toughest jobs — "
            "thick steel, outdoor conditions, and heavy structural "
            "applications where durability matters most."
        ),
        "icon": "🔧",
        "image": "seated-welder.jpg",
    },
    {
        "id": "fabrication",
        "title": "Custom Fabrication",
        "short_description": "From concept to finished piece — built to your specs.",
        "long_description": (
            "Need something custom? From gates and railings to truck "
            "bumpers and equipment mounts, every piece is hand-crafted "
            "to your exact specifications."
        ),
        "icon": "🛠️",
        "image": "bright-welder.jpg",
    },
    {
        "id": "repair",
        "title": "Welding Repair",
        "short_description": "Fix broken equipment, trailers, and metal structures.",
        "long_description": (
            "Cracked frames, broken hinges, snapped brackets — if it's "
            "metal, it can be fixed. On-site repair available for "
            "equipment that can't be moved."
        ),
        "icon": "🔥",
        "image": "dark-welding.jpg",
    },
    {
        "id": "mobile",
        "title": "Mobile Welding",
        "short_description": "We come to you — on-site service within 50 miles.",
        "long_description": (
            "Fully equipped mobile welding rig ready to roll. Farm "
            "equipment, construction sites, residential projects — "
            "wherever the job is, we'll be there."
        ),
        "icon": "🚛",
        "image": "close-welding.jpg",
    },
]


@services_bp.route("/services")
def services():
    """
    Render the services gallery page.

    Passes the SERVICES list to the template so each service
    card can be rendered dynamically.

    Returns:
        Rendered HTML for the services page.
    """
    logger.info("Services page requested. Rendering %s services.", len(SERVICES))
    return render_template("services.html", services=SERVICES)
