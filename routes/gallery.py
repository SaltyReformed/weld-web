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
        "image": "welded_gate.jpg",
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
        "image": "trailer_repair.jpg",
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
        "image": "metal_stairs.jpg",
        "image_alt": (
            "Modern steel staircase railing with clean horizontal "
            "cable runs in a residential interior"
        ),
        "description": (
            "Contemporary cable railing for a two-story interior "
            "staircase. Brushed stainless steel posts with "
            "horizontal cable infill."
        ),
    },
    {
        "id": "proj-4",
        "title": "Structural Beam Reinforcement",
        "category": "structural",
        "image": "beam-reinforcement.jpg",
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
            "Round steel fire pit with decorative cut-out patterns "
            "glowing from the flames inside, set on a stone patio"
        ),
        "description": (
            "36-inch diameter fire pit with custom plasma-cut "
            "mountain-range pattern. Finished with high-heat "
            "clear coat."
        ),
    },
    {
        "id": "proj-6",
        "title": "Equipment Repair",
        "category": "structural",
        "image": "equipment-repair.jpg",
        "image_alt": (
            "Heavy-duty steel mounting brackets welded to a truck "
            "bed for securing equipment during transport"
        ),
        "description": (
            "Custom heavy-duty mounting brackets for a service "
            "truck. Designed to secure a generator and air "
            "compressor for daily transport."
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
