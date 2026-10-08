# Local Temporary Mail Sandbox

This project is a local-only mock email inbox & OTP demo.

It is intended for learning, testing web UI flows, and browser automation in a sandbox.
It does not connect to any external service, real email provider, or production registration system.

## Features

- Create a random temporary inbox like `user123@local.test`
- View inbox messages locally
- Trigger OTP generation for testing
- Simple web UI
- Selenium automation example

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Then open:

- http://localhost:5000

You can also run the browser automation sample:

```bash
python selenium_demo.py
```

## Notes

This is a sandbox-only project for testing and educational purposes.
