# Selenium Demo Starter

This repository contains a safe, local-only Selenium example for learning browser automation.

What it includes:
- A tiny local Flask app with a sample form
- A Selenium script that opens the app, fills in the form, and submits it
- A simple setup guide for local testing

This project is intended for educational and testing purposes only. It does not target real production services, bypass account protections, evade CAPTCHAs, or automate unauthorized access.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Then open the browser automation script:

```bash
python selenium_template.py
```

The app will run locally in the browser at:

- http://localhost:5000

## Files

- `app.py` – local demo form app
- `selenium_template.py` – Selenium automation example
- `requirements.txt` – Python dependencies
