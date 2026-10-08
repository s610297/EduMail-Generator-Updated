import argparse
import json
import os
import random
import string
from datetime import datetime

DATA_FILE = "mail_data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def create_user(domain, alias):
    alias = alias.strip().lower()
    email = f"{alias}@{domain}"
    data = load_data()
    if email not in data:
        data[email] = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "otp": None,
            "messages": []
        }
        save_data(data)
    return email


def generate_otp(email, length=6):
    data = load_data()
    if email not in data:
        return None
    otp = "".join(random.choice(string.digits) for _ in range(length))
    data[email]["otp"] = otp
    data[email]["messages"].append({
        "from": "system@local",
        "subject": "Your OTP Code",
        "body": f"Your OTP is: {otp}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_data(data)
    return otp


def send_message(to_email, sender, subject, body):
    data = load_data()
    if to_email not in data:
        return False
    data[to_email]["messages"].append({
        "from": sender,
        "subject": subject,
        "body": body,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_data(data)
    return True


def inbox(email):
    data = load_data()
    if email not in data:
        return None

    info = data[email]
    output = f"\n{'=' * 70}\n"
    output += f"📧 EMAIL: {email}\n"
    output += f"Created: {info['created_at']}\n"
    output += f"OTP: {info['otp'] or '❌ Not generated yet'}\n"
    output += f"Total Messages: {len(info['messages'])}\n"
    output += f"{'=' * 70}\n"

    if not info["messages"]:
        output += "\n✓ No messages yet.\n"
        return output

    output += "\n📬 INBOX MESSAGES:\n"
    for i, msg in enumerate(info["messages"], 1):
        output += f"\n{i}. 📨 From: {msg['from']}\n"
        output += f"   Subject: {msg['subject']}\n"
        output += f"   Time: {msg['timestamp']}\n"
        output += f"   Body: {msg['body']}\n"

    return output


def list_emails():
    data = load_data()
    return list(data.keys())


def interactive_mode():
    """Interactive mode - user input"""
    print("\n" + "=" * 70)
    print("🎯 LOCAL MOCK EMAIL SYSTEM - INTERACTIVE MODE")
    print("=" * 70)

    domain = "ku.ac.bd"
    print(f"\n📌 Domain: {domain}\n")

    # Step 1: User creates custom email
    print("Step 1️⃣  - Create Custom Email")
    print("-" * 70)
    alias = input("Enter custom email name (without @ku.ac.bd): ").strip()
    
    if not alias:
        print("❌ Email name cannot be empty!")
        return

    email = create_user(domain, alias)
    print(f"✅ Email Created: {email}\n")

    # Step 2: Generate OTP
    print("Step 2️⃣  - Generate OTP")
    print("-" * 70)
    otp = generate_otp(email, 6)
    print(f"✅ OTP Generated: {otp}\n")

    # Step 3: Send messages
    print("Step 3️⃣  - Send Messages to Inbox")
    print("-" * 70)
    
    # Message 1
    send_message(email, "admin@ku.ac.bd", "Welcome", "Welcome to KU portal. Your account is ready.")
    print("✅ Message 1 sent from admin@ku.ac.bd\n")
    
    # Message 2
    send_message(email, "teacher@ku.ac.bd", "Assignment", "Submit your assignment by Friday")
    print("✅ Message 2 sent from teacher@ku.ac.bd\n")

    # Step 4: View inbox
    print("Step 4️⃣  - View Inbox with OTP & Messages")
    print("-" * 70)
    result = inbox(email)
    if result:
        print(result)

    print("\n" + "=" * 70)
    print("✅ PROCESS COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"   Email: {email}")
    print(f"   OTP: {otp}")
    print(f"   Messages in Inbox: 2 + 1 OTP = 3 total")
    print("\n")


def main():
    parser = argparse.ArgumentParser(description="Local mock email + inbox + OTP simulator")
    parser.add_argument("command", nargs="?", choices=["create", "otp", "send", "inbox", "list", "interactive"])
    parser.add_argument("value", nargs="?")
    parser.add_argument("--domain", default="ku.ac.bd")
    parser.add_argument("--sender", default="admin@local")
    parser.add_argument("--subject", default="Notice")
    parser.add_argument("--body", default="Hello")
    parser.add_argument("--length", type=int, default=6)

    args = parser.parse_args()

    # If no command, run interactive mode
    if not args.command or args.command == "interactive":
        interactive_mode()
        return

    if args.command == "create":
        if not args.value:
            print("Use: python email_system.py create <alias>")
            return
        email = create_user(args.domain, args.value)
        print(f"✅ Created: {email}")

    elif args.command == "otp":
        if not args.value:
            print("Use: python email_system.py otp <email>")
            return
        otp = generate_otp(args.value, args.length)
        if otp is None:
            print(f"❌ Email {args.value} not found")
        else:
            print(f"✅ OTP for {args.value}: {otp}")

    elif args.command == "send":
        if not args.value:
            print("Use: python email_system.py send <to_email>")
            return
        ok = send_message(args.value, args.sender, args.subject, args.body)
        if ok:
            print(f"✅ Message sent to {args.value}")
        else:
            print(f"❌ Email {args.value} not found")

    elif args.command == "inbox":
        if not args.value:
            print("Use: python email_system.py inbox <email>")
            return
        result = inbox(args.value)
        if result is None:
            print(f"❌ Email {args.value} not found")
        else:
            print(result)

    elif args.command == "list":
        emails = list_emails()
        if not emails:
            print("❌ No emails found")
        else:
            print("\n📧 Saved Emails:")
            for i, email in enumerate(emails, 1):
                print(f"   {i}. {email}")
            print()


if __name__ == "__main__":
    main()
