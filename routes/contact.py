"""
Contact / Quote Request blueprint for the Ironforge Welding website.

Handles both GET (render the form) and POST (process the submission)
requests.  When MAIL_ENABLED is true in the app config, form
submissions are emailed to the business owner via Flask-Mail.
Otherwise they are logged to the console (useful during development).

Rate limiting is applied to the POST endpoint to prevent abuse.
"""

import logging

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_mail import Message

# Import the shared limiter and mail instances so the decorator and
# the send function can be used from this module.
from extensions import limiter, mail

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

# Human-readable labels for the notification email.
SERVICE_LABELS = {
    "mig": "MIG Welding",
    "tig": "TIG Welding",
    "stick": "Stick Welding",
    "fabrication": "Custom Fabrication",
    "repair": "Welding Repair",
    "mobile": "Mobile Welding",
    "other": "Other / Not Sure",
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


def send_quote_email(name, email, phone, service_type, message_body):
    """
    Send a quote-request notification email to the business owner.

    If MAIL_ENABLED is false the email content is logged instead.
    Any SMTP errors are caught and logged so the user still sees a
    success message (the submission is not lost — it's in the logs).

    Args:
        name: Customer's full name.
        email: Customer's email address.
        phone: Customer's phone number (or "not provided").
        service_type: The service slug (or "not specified").
        message_body: Free-text project description.
    """
    # Build a readable service label for the email.
    service_label = SERVICE_LABELS.get(service_type, service_type)

    # Compose the notification email body.
    body_lines = [
        "New quote request from the Ironforge Welding website.",
        "",
        "--- Customer Details ---",
        "Name:    %s" % name,
        "Email:   %s" % email,
        "Phone:   %s" % phone,
        "Service: %s" % service_label,
        "",
        "--- Project Description ---",
        message_body,
        "",
        "---",
        "Reply directly to this email to respond to the customer.",
    ]
    body_text = "\n".join(body_lines)

    # Check if email sending is enabled.
    if not current_app.config.get("MAIL_ENABLED"):
        logger.info(
            "MAIL_ENABLED is false — email NOT sent.  Contents:\n%s",
            body_text,
        )
        return

    recipient = current_app.config.get("QUOTE_RECIPIENT_EMAIL")
    subject = "New Quote Request from %s" % name

    msg = Message(
        subject=subject,
        recipients=[recipient],
        body=body_text,
        reply_to=email,  # Let the owner reply straight to the customer.
    )

    try:
        mail.send(msg)
        logger.info(
            "Quote notification email sent to %s for customer %s.",
            recipient,
            email,
        )
    except Exception:  # pylint: disable=broad-except
        # Log the full traceback so we can diagnose SMTP issues without
        # crashing the request.  The user still gets a success flash —
        # the submission is preserved in the application logs.
        logger.exception(
            "Failed to send quote notification email for customer %s.",
            email,
        )


@contact_bp.route("/contact", methods=["GET"])
def contact():
    """
    Render the contact / quote request form.

    Returns:
        Rendered HTML for the contact page.
    """
    logger.info("Contact page requested (GET).")
    # Pass an empty dict so templates can always call form_data.get()
    # without guarding against None.
    return render_template("contact.html", form_data={})


@contact_bp.route("/contact", methods=["POST"])
@limiter.limit("5 per minute")  # Prevent rapid-fire form spam.
def contact_submit():
    """
    Process a submitted contact / quote request form.

    Validates the form data.  On success, sends (or logs) a
    notification email and redirects with a success flash message.
    On failure, re-renders the form with error messages **and the
    user's original input** so they don't have to retype everything.

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

        # Re-render the form, passing back the submitted data so the
        # user's input is preserved in the form fields.
        return (
            render_template("contact.html", form_data=request.form),
            400,
        )

    # Extract sanitised values.
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    service_type = request.form.get("service_type", "").strip() or "not specified"
    phone = request.form.get("phone", "").strip() or "not provided"
    message_body = request.form.get("message", "").strip()

    logger.info(
        "Quote request received — Name: %s | Email: %s | Service: %s " "| Phone: %s",
        name,
        email,
        service_type,
        phone,
    )

    # Attempt to send (or log) the notification email.
    send_quote_email(name, email, phone, service_type, message_body)

    flash(
        "Thanks, " + name + "! Your quote request has been received. "
        "We'll be in touch within 24 hours.",
        "success",
    )

    return redirect(url_for("contact.contact"))
