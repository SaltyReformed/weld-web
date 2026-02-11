"""
Shared Flask extension instances for the Ironforge Welding application.

Extensions are instantiated here (without an app) and later initialised
via ``init_app()`` inside the application factory in ``app.py``.  This
pattern avoids circular imports when route modules need to reference
extension objects (e.g. the rate limiter decorator).
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

# CSRF protection — guards all POST forms against cross-site request forgery.
csrf = CSRFProtect()

# Rate limiter — prevents abuse of public endpoints (especially the form).
# The key_func identifies clients by IP address.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["120 per minute"],  # generous global default
)
