"""
Portfolio / Gallery page blueprint for the Ironforge Welding website.

Renders a filterable gallery of completed projects.  Project data is
defined here as placeholder content for the prototype; in production
this would come from a database or CMS with admin-uploaded photos.
"""

import logging

from flask import Blueprint, render_template, request

# Module-level logger for this blueprint.
logger = logging.getLogger(__name__)

gallery_bp = Blueprint("gallery", __name__)

# Valid categories used for client-side filtering buttons.
CATEGORIES = [
    {"slug": "all", "label": "All Projects"},
    {"slug": "fabrication", "label": "Fabrication"},
    {"slug": "repair", "label": "Repair"},
    {"slug": "structural", "label": "Structural"},
    {"slug": "decorative", "label": "Decorative"},
]

# Placeholder portfolio items for the prototype.
# Each item maps to an image in static/images/ and a filter category.
PROJECTS = [
    {
        "id": "proj-1",
        "title": "Custom Driveway Gate",
        "category": "fabrication",
        "image": "driveway-gate.jpg",
        "image_alt": (
            "Ornamental wrought-iron driveway gate with scrollwork "
            "detail, installed between stone pillars"
        ),
        "description": (
            "Hand-built double-swing driveway gate with decorative "
            "scrollwork. Powder-coated satin black for durability."
        ),
    },
    {
        "id": "proj-2",
        "title": "Trailer Frame Repair",
        "category": "repair",
        "image": "trailer-frame.jpg",
        "image_alt": (
            "Repaired flatbed trailer frame showing fresh weld beads "
            "on reinforced cross-members"
        ),
        "description": (
            "Cracked cross-members on a 24-foot flatbed trailer. "
            "Cut out the damaged sections, plated and re-welded. "
            "Back on the road the same week."
        ),
    },
    {
        "id": "proj-3",
        "title": "Staircase Railing",
        "category": "decorative",
        "image": "stair-railing.jpg",
        "image_alt": (
            "Modern steel staircase railing with clean horizontal "
            "steel runs in a residential interior"
        ),
        "description": (
            "Contemporary steel railing for a two-story "
            "interior staircase. Brushed stainless steel"
            "posts with horizontal brushed stainless infill."
        ),
    },
    {
        "id": "proj-4",
        "title": "Structural Beam Reinforcement",
        "category": "structural",
        "image": "i-beam-weld.jpg",
        "image_alt": (
            "Heavy steel I-beam with fresh gusset plates welded "
            "at the connection point inside a commercial building"
        ),
        "description": (
            "Gusset plate reinforcement on load-bearing I-beam "
            "connections for a commercial renovation. Passed "
            "structural inspection on the first attempt."
        ),
    },
    {
        "id": "proj-5",
        "title": "Custom Fire Pit",
        "category": "fabrication",
        "image": "custom-fire-pit.jpg",
        "image_alt": (
            "Square steel fire pit with decorative cut-out patterns "
            "firewood stacked inside, set on a sand patio"
        ),
        "description": (
            "36-inch square fire pit. Finished with high-heat " "clear coat."
        ),
    },
    {
        "id": "proj-6",
        "title": "Equipment Repair",
        "category": "repair",
        "image": "equipment-repair.jpg",
        "image_alt": (
            "Professional welder repairing a cracked excavator scoop "
            "with heavy-duty welding equipment in a workshop"
        ),
        "description": (
            "Structural repair and reinforcement of a worn excavator "
            "scoop. Cracks were welded, weak points rebuilt, and "
            "high-wear areas reinforced to restore strength and "
            "extend the life of the equipment."
        ),
    },
]


@gallery_bp.route("/gallery")
def gallery():
    """
    Render the portfolio / gallery page.

    Accepts an optional ``category`` query parameter for server-side
    filtering (the page also supports client-side JS filtering).

    Returns:
        Rendered HTML for the gallery page.
    """
    # Read optional category filter from query string.
    active_category = request.args.get("category", "all").strip().lower()

    # Validate category — fall back to "all" if unrecognised.
    valid_slugs = {cat["slug"] for cat in CATEGORIES}
    if active_category not in valid_slugs:
        logger.warning(
            "Unknown gallery category '%s'. Falling back to 'all'.",
            active_category,
        )
        active_category = "all"

    # Filter projects if a specific category was requested.
    if active_category == "all":
        filtered_projects = PROJECTS
    else:
        filtered_projects = [p for p in PROJECTS if p["category"] == active_category]

    logger.info(
        "Gallery page requested — category: '%s', showing %d projects.",
        active_category,
        len(filtered_projects),
    )

    return render_template(
        "gallery.html",
        projects=filtered_projects,
        categories=CATEGORIES,
        active_category=active_category,
    )
