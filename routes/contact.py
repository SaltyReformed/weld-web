"""
Contact / Quote Request blueprint for the Ironforge Welding website.

Handles both GET (render the form) and POST (process the submission)
requests. In this prototype, form submissions are logged and a flash
message is displayed — no emails are actually sent.
"""

import logging

from flask import Blueprint, flash, redirect, render_template, request, url_for

# Module-level logger for this blueprint.
logger = logging.getLogger(__name__)

contact_bp = Blueprint("contact", __name__)

# Valid service types the form will accept.
VALID_SERVICE_TYPES = {
    "mig",
    "tig",
    "stick",
    "fabrication",
    "repair",
    "mobile",
    "other",
}


def validate_contact_form(form_data):
    """
    Validate the contact / quote request form data.

    Checks that required fields are present, the email looks reasonable,
    and the service type is one of the allowed values.

    Args:
        form_data: An ImmutableMultiDict from request.form.

    Returns:
        A tuple of (is_valid: bool, errors: list[str]).
    """
    errors = []

    # Check required text fields.
    name = form_data.get("name", "").strip()
    if not name:
        errors.append("Name is required.")

    email = form_data.get("email", "").strip()
    if not email:
        errors.append("Email is required.")
    elif "@" not in email or "." not in email:
        # Simple sanity check — not a full RFC 5322 validation.
        errors.append("Please enter a valid email address.")

    service_type = form_data.get("service_type", "").strip()
    if service_type and service_type not in VALID_SERVICE_TYPES:
        errors.append("Invalid service type selected.")

    message = form_data.get("message", "").strip()
    if not message:
        errors.append("Please include a brief description of your project.")

    return (len(errors) == 0, errors)


@contact_bp.route("/contact", methods=["GET"])
def contact():
    """
    Render the contact / quote request form.

    Returns:
        Rendered HTML for the contact page.
    """
    logger.info("Contact page requested (GET).")
    return render_template("contact.html")


@contact_bp.route("/contact", methods=["POST"])
def contact_submit():
    """
    Process a submitted contact / quote request form.

    Validates the form data. On success, logs the submission details
    and redirects with a success flash message. On failure, re-renders
    the form with error messages.

    Returns:
        A redirect to the contact page (on success) or the re-rendered
        contact form template (on validation failure).
    """
    logger.info("Contact form submitted (POST).")

    is_valid, errors = validate_contact_form(request.form)

    if not is_valid:
        # Log each validation error for debugging.
        for err in errors:
            logger.warning("Form validation error: %s", err)
            flash(err, "error")
        # Re-render the form so the user can correct their input.
        return render_template("contact.html"), 400

    # Extract sanitized values for logging.
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    service_type = request.form.get("service_type", "").strip() or "not specified"
    phone = request.form.get("phone", "").strip() or "not provided"

    logger.info(
        "Quote request received — Name: %s | Email: %s | Service: %s | Phone: %s",
        name,
        email,
        service_type,
        phone,
    )

    # In a production app this is where you would send an email,
    # write to a database, or push to a CRM. For the prototype
    # we just flash a success message.
    flash(
        "Thanks, " + name + "! Your quote request has been received. "
        "We'll be in touch within 24 hours.",
        "success",
    )

    return redirect(url_for("contact.contact"))
