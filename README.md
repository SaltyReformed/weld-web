# Ironforge Welding — Prototype Website

A Flask-based prototype website for a one-man welding business. Features a hero
landing page, services gallery with expand/collapse cards, and a contact/quote
request form with client- and server-side validation.

## Project Structure

```
welding_site/
├── app.py                    # Application factory and entry point
├── config.py                 # Environment-specific configuration
├── requirements.txt          # Python dependencies
├── routes/
│   ├── __init__.py           # Routes package
│   ├── home.py               # Home / hero page blueprint
│   ├── services.py           # Services gallery blueprint
│   └── contact.py            # Contact form blueprint (GET + POST)
├── static/
│   ├── css/
│   │   └── styles.css        # All CSS (no inline styles in HTML)
│   ├── js/
│   │   └── main.js           # All JavaScript (no inline scripts)
│   └── images/               # Place photos here
└── templates/
    ├── base.html             # Base layout with nav, flash, footer
    ├── home.html             # Home page
    ├── services.html         # Services gallery
    ├── contact.html          # Quote request form
    └── errors/
        ├── 404.html          # Custom 404 page
        └── 500.html          # Custom 500 page
```

## Quick Start

### Prerequisites

- Python 3.10 or later
- pip

### Windows (PowerShell)

```powershell
# Clone or copy the project, then cd into it
cd welding_site

# Create a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the dev server
python app.py
```

### Linux (Bash)

```bash
cd welding_site

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the dev server
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## Pages

| URL         | Description                              |
|-------------|------------------------------------------|
| `/`         | Home — hero section, highlights, about   |
| `/services` | Services gallery with toggle details     |
| `/contact`  | Quote request form (demo — no email)     |

## Design Decisions

- **Separation of concerns**: HTML templates contain zero CSS or JavaScript.
  All styles live in `static/css/styles.css` and all scripts in
  `static/js/main.js`.
- **Flask Blueprints**: Each page is its own Blueprint so the project stays
  organized as it grows.
- **Prototype form**: The contact form validates on both client and server
  side. Submissions are logged to the console (no email or database yet).
- **Industrial aesthetic**: Dark background, amber/spark accent color, bold
  condensed headings — fits the welding trade.

## Next Steps

Some ideas for expanding the prototype:

- **Add real photos** — drop images into `static/images/` and reference them
  in the templates.
- **Email integration** — wire up Flask-Mail or an SMTP service so the
  contact form actually sends quotes.
- **Database** — use Flask-SQLAlchemy + SQLite to persist quote requests and
  add an admin view.
- **Testimonials** — add a testimonials section or page.
- **Deployment** — host on a VPS with Gunicorn + Nginx, or use a platform
  like Railway, Render, or PythonAnywhere.
