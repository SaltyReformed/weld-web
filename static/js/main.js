/**
 * @file main.js
 * @description Client-side interactivity for the Ironforge Welding website.
 *
 * Handles:
 *  - Mobile navigation toggle (hamburger menu)
 *  - Flash message dismiss buttons
 *  - Service card expand / collapse
 *  - Client-side contact form validation
 *
 * No external dependencies — vanilla ES6.
 */

"use strict";

/* ==========================================================================
   Utility Helpers
   ========================================================================== */

/**
 * Safely select a single DOM element.
 * @param {string} selector - CSS selector string.
 * @param {Element} [parent=document] - Parent element to search within.
 * @returns {Element|null} The matched element or null.
 */
function qs(selector, parent) {
    return (parent || document).querySelector(selector);
}

/**
 * Safely select multiple DOM elements and return as an array.
 * @param {string} selector - CSS selector string.
 * @param {Element} [parent=document] - Parent element to search within.
 * @returns {Element[]} Array of matched elements.
 */
function qsa(selector, parent) {
    return Array.from((parent || document).querySelectorAll(selector));
}

/* ==========================================================================
   Mobile Navigation Toggle
   ========================================================================== */

/**
 * Initialise the hamburger menu toggle for mobile viewports.
 * Adds click handling and updates ARIA attributes.
 */
function initNavToggle() {
    var toggleBtn = qs("#nav-toggle");
    var navLinks = qs("#nav-links");

    if (!toggleBtn || !navLinks) {
        return; // Elements not found — nothing to do.
    }

    toggleBtn.addEventListener("click", function () {
        var isOpen = navLinks.classList.toggle("open");
        toggleBtn.classList.toggle("open");

        // Update ARIA attribute so screen readers know the state.
        toggleBtn.setAttribute("aria-expanded", String(isOpen));
    });

    // Close the menu when a link is clicked (smooth UX on mobile).
    qsa("a", navLinks).forEach(function (link) {
        link.addEventListener("click", function () {
            navLinks.classList.remove("open");
            toggleBtn.classList.remove("open");
            toggleBtn.setAttribute("aria-expanded", "false");
        });
    });
}

/* ==========================================================================
   Flash Message Dismiss
   ========================================================================== */

/**
 * Attach click handlers to flash message close buttons so users
 * can dismiss notifications.
 */
function initFlashDismiss() {
    qsa(".flash-close").forEach(function (btn) {
        btn.addEventListener("click", function () {
            var flashMsg = btn.closest(".flash-message");
            if (flashMsg) {
                // Fade out, then remove from the DOM.
                flashMsg.style.opacity = "0";
                flashMsg.style.transform = "translateY(-8px)";
                setTimeout(function () {
                    flashMsg.remove();
                }, 300);
            }
        });
    });
}

/* ==========================================================================
   Service Card Expand / Collapse
   ========================================================================== */

/**
 * Set up "Learn More" / "Show Less" toggle buttons on service cards.
 * Uses a CSS class to animate the detail panel open and closed.
 */
function initServiceToggles() {
    qsa(".service-toggle").forEach(function (btn) {
        btn.addEventListener("click", function () {
            // Find the detail panel associated with this button.
            var card = btn.closest(".service-card");
            if (!card) {
                return;
            }

            var detail = qs(".service-detail", card);
            if (!detail) {
                return;
            }

            var isExpanded = detail.classList.toggle("expanded");

            // Update button text and ARIA state.
            btn.textContent = isExpanded ? "Show Less" : "Learn More";
            btn.setAttribute("aria-expanded", String(isExpanded));
        });
    });
}

/* ==========================================================================
   Client-Side Form Validation
   ========================================================================== */

/**
 * Validate a single form field and display/clear its error message.
 *
 * @param {HTMLInputElement|HTMLTextAreaElement} field - The form field.
 * @param {string} errorId - The ID of the associated error <span>.
 * @param {string} message - Error message to show if the field is invalid.
 * @param {Function} [customCheck] - Optional extra validation function.
 *        Receives the trimmed value and should return true if valid.
 * @returns {boolean} True if the field passes validation.
 */
function validateField(field, errorId, message, customCheck) {
    var errorSpan = qs("#" + errorId);
    var value = field.value.trim();

    // Determine validity: required check + optional custom check.
    var isValid = value.length > 0;
    if (isValid && typeof customCheck === "function") {
        isValid = customCheck(value);
    }

    if (!isValid) {
        field.classList.add("invalid");
        if (errorSpan) {
            errorSpan.textContent = message;
        }
    } else {
        field.classList.remove("invalid");
        if (errorSpan) {
            errorSpan.textContent = "";
        }
    }

    return isValid;
}

/**
 * Attach client-side validation to the quote request form.
 * Validates on submit and also clears errors on input (live feedback).
 */
function initFormValidation() {
    var form = qs("#quote-form");
    if (!form) {
        return; // Form not on this page.
    }

    var nameField = qs("#name", form);
    var emailField = qs("#email", form);
    var messageField = qs("#message", form);

    // Simple email format check (not exhaustive — server validates too).
    function isEmailLike(value) {
        return value.indexOf("@") > 0 && value.indexOf(".") > 0;
    }

    // Validate all fields on submit; prevent submission if any fail.
    form.addEventListener("submit", function (event) {
        var allValid = true;

        if (!validateField(nameField, "name-error", "Name is required.")) {
            allValid = false;
        }
        if (!validateField(emailField, "email-error", "Please enter a valid email.", isEmailLike)) {
            allValid = false;
        }
        if (!validateField(messageField, "message-error", "Please describe your project.")) {
            allValid = false;
        }

        if (!allValid) {
            event.preventDefault(); // Stop the form from submitting.
        }
    });

    // Clear individual field errors as the user types (live feedback).
    [nameField, emailField, messageField].forEach(function (field) {
        if (!field) {
            return;
        }
        field.addEventListener("input", function () {
            field.classList.remove("invalid");
            var errorSpan = qs("#" + field.id + "-error");
            if (errorSpan) {
                errorSpan.textContent = "";
            }
        });
    });
}

/**
 * Pause hero background video if the user prefers reduced motion.
 */
function initHeroVideo() {
    var video = qs(".hero-video");
    if (!video) {
        return;
    }

    var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)");

    if (prefersReduced.matches) {
        video.pause();
    }

    // Listen for changes (user toggles the OS setting mid-session).
    prefersReduced.addEventListener("change", function (e) {
        if (e.matches) {
            video.pause();
        } else {
            video.play();
        }
    });
}

/* ==========================================================================
   Initialise Everything on DOM Ready
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
    initNavToggle();
    initFlashDismiss();
    initServiceToggles();
    initFormValidation();
    initHeroVideo();
});
