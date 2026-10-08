import argparse
import os
import smtplib
import ssl
from email.message import EmailMessage


DEFAULT_SMTP = {
    "gmail": {"host": "smtp.gmail.com", "port": 465},
    "outlook": {"host": "smtp-mail.outlook.com", "port": 587},
    "yahoo": {"host": "smtp.mail.yahoo.com", "port": 465},
}


def send_real_email(to_email, subject, body, username, password, provider="gmail"):
    provider = provider.lower()
    if provider not in DEFAULT_SMTP:
        raise ValueError(f"Unsupported provider: {provider}. Use gmail, outlook, or yahoo.")

    cfg = DEFAULT_SMTP[provider]
    host = cfg["host"]
    port = cfg["port"]

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = to_email
    msg.set_content(body)

    context = ssl.create_default_context()

    if provider == "gmail":
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.send_message(msg)
    elif provider in ("outlook", "yahoo"):
        with smtplib.SMTP(host, port) as server:
            server.starttls(context=context)
            server.login(username, password)
            server.send_message(msg)

    print(f"✅ Real email sent successfully to {to_email} using {provider} SMTP.")


def get_credentials(args):
    username = args.username or os.getenv("EMAIL_USER")
    password = args.password or os.getenv("EMAIL_PASS")

    if not username or not password:
        raise ValueError(
            "Email username/password not provided. Use --username/--password or set EMAIL_USER/EMAIL_PASS environment variables."
        )
    return username, password


def main():
    parser = argparse.ArgumentParser(description="Send a real email using SMTP")
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", default="Test Email", help="Email subject")
    parser.add_argument("--body", default="Hello! This is a real SMTP email test.", help="Email body")
    parser.add_argument("--provider", choices=["gmail", "outlook", "yahoo"], default="gmail", help="SMTP provider")
    parser.add_argument("--username", help="Email account username")
    parser.add_argument("--password", help="App password or account password")
    args = parser.parse_args()

    username, password = get_credentials(args)
    send_real_email(args.to, args.subject, args.body, username, password, args.provider)


if __name__ == "__main__":
    main()
