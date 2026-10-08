import random
import string
import argparse
import json
import csv
from datetime import datetime
from pathlib import Path

class AdvancedEmailGenerator:
    def __init__(self, domain="local.test"):
        self.domain = domain
        self.emails = []
        self.inbox = {}
        self.otp_codes = {}

    def generate_alias(self, length=10):
        """Random alias generate করবে"""
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_custom_email(self, custom_alias):
        """Custom নাম দিয়ে email তৈরি করবে"""
        custom_alias = custom_alias.strip().lower()
        email = f"{custom_alias}@{self.domain}"
        self.emails.append(email)
        self.inbox[email] = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "messages": [],
            "otp": None
        }
        return email

    def generate_random_email(self, pattern="user"):
        """Random pattern দিয়ে email তৈরি করবে"""
        alias = f"{pattern}{random.randint(1000, 9999)}"
        email = f"{alias}@{self.domain}"
        self.emails.append(email)
        self.inbox[email] = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "messages": [],
            "otp": None
        }
        return email

    def generate_bulk(self, count=10, pattern="user"):
        """Bulk email generate করবে"""
        emails = []
        for _ in range(count):
            email = self.generate_random_email(pattern)
            emails.append(email)
        return emails

    def generate_otp(self, email, length=6):
        """OTP generate করবে"""
        if email not in self.inbox:
            return None
        
        otp = ''.join(random.choice(string.digits) for _ in range(length))
        self.inbox[email]["otp"] = otp
        self.inbox[email]["messages"].append({
            "from": "system@local",
            "subject": "Your OTP Code",
            "body": f"Your activation code is: {otp}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return otp

    def add_message(self, email, sender, subject, body):
        """Email-এ message add করবে"""
        if email not in self.inbox:
            return False
        
        self.inbox[email]["messages"].append({
            "from": sender,
            "subject": subject,
            "body": body,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return True

    def view_inbox(self, email):
        """একটি inbox দেখবে"""
        if email not in self.inbox:
            return None
        return self.inbox[email]

    def view_all_inboxes(self):
        """সব inboxes দেখবে"""
        return self.inbox

    def list_emails(self):
        """সব email list করবে"""
        return self.emails

    def save_to_file(self, filename="emails.txt"):
        """File-এ save করবে"""
        with open(filename, 'w') as f:
            for email in self.emails:
                f.write(email + '\n')
        return f"Saved {len(self.emails)} emails to {filename}"

    def save_to_json(self, filename="inbox.json"):
        """JSON file-এ save করবে"""
        with open(filename, 'w') as f:
            json.dump(self.inbox, f, indent=2)
        return f"Saved inbox to {filename}"

    def save_to_csv(self, filename="emails.csv"):
        """CSV file-এ save করবে"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Email', 'Domain', 'Created At', 'OTP', 'Messages Count'])
            for email, data in self.inbox.items():
                writer.writerow([
                    email,
                    self.domain,
                    data['created_at'],
                    data['otp'] or 'N/A',
                    len(data['messages'])
                ])
        return f"Saved inbox to {filename}"

    def to_json(self):
        """JSON format-এ return করবে"""
        return json.dumps({
            "domain": self.domain,
            "total_emails": len(self.emails),
            "emails": self.emails,
            "inbox_details": self.inbox,
            "generated_at": datetime.now().isoformat()
        }, indent=2)

    def display_inbox(self, email):
        """Inbox সুন্দরভাবে display করবে"""
        if email not in self.inbox:
            return f"Email {email} not found in inbox"
        
        inbox_data = self.inbox[email]
        output = f"\n{'='*60}\n"
        output += f"Email: {email}\n"
        output += f"Created: {inbox_data['created_at']}\n"
        output += f"OTP: {inbox_data['otp'] or 'Not generated yet'}\n"
        output += f"Messages: {len(inbox_data['messages'])}\n"
        output += f"{'='*60}\n"
        
        if inbox_data['messages']:
            output += "\nMessages:\n"
            for i, msg in enumerate(inbox_data['messages'], 1):
                output += f"\n{i}. From: {msg['from']}\n"
                output += f"   Subject: {msg['subject']}\n"
                output += f"   Time: {msg['timestamp']}\n"
                output += f"   Body: {msg['body']}\n"
        else:
            output += "\nNo messages yet.\n"
        
        return output


def main():
    parser = argparse.ArgumentParser(
        description="Advanced Email Generator - Custom emails, Inbox, OTP support"
    )
    
    # Main arguments
    parser.add_argument('domain', nargs='?', default='local.test', help='Domain (e.g., ku.ac.bd)')
    
    # Generation options
    parser.add_argument('--custom', help='Create custom email (e.g., --custom john)')
    parser.add_argument('--count', type=int, default=1, help='Generate multiple emails')
    parser.add_argument('--pattern', default='user', help='Pattern for random emails')
    
    # OTP options
    parser.add_argument('--otp', help='Generate OTP for email (e.g., --otp user1@ku.ac.bd)')
    parser.add_argument('--otp-length', type=int, default=6, help='OTP length')
    
    # View/Display options
    parser.add_argument('--inbox', help='View inbox for email (e.g., --inbox user1@ku.ac.bd)')
    parser.add_argument('--list', action='store_true', help='List all generated emails')
    parser.add_argument('--show-all', action='store_true', help='Show all inbox details')
    
    # Save options
    parser.add_argument('--save', help='Save emails to file')
    parser.add_argument('--save-json', help='Save inbox to JSON file')
    parser.add_argument('--save-csv', help='Save inbox to CSV file')
    
    # Output format
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    gen = AdvancedEmailGenerator(domain=args.domain)

    # Generate emails
    if args.custom:
        email = gen.generate_custom_email(args.custom)
        print(f"Created: {email}")
    else:
        emails = gen.generate_bulk(count=args.count, pattern=args.pattern)
        if not args.list and not args.inbox and not args.show_all:
            for i, email in enumerate(emails, 1):
                print(f"{i}. {email}")

    # Generate OTP
    if args.otp:
        otp = gen.generate_otp(args.otp, args.otp_length)
        if otp:
            print(f"\nOTP generated for {args.otp}: {otp}")
        else:
            print(f"Email {args.otp} not found")

    # View inbox
    if args.inbox:
        print(gen.display_inbox(args.inbox))

    # Show all inboxes
    if args.show_all:
        print(gen.to_json())

    # List emails
    if args.list:
        print("\nAll Generated Emails:")
        for i, email in enumerate(gen.list_emails(), 1):
            print(f"{i}. {email}")

    # Save files
    if args.save:
        print(f"\n{gen.save_to_file(args.save)}")
    
    if args.save_json:
        print(f"\n{gen.save_to_json(args.save_json)}")
    
    if args.save_csv:
        print(f"\n{gen.save_to_csv(args.save_csv)}")

    # JSON output
    if args.json:
        print("\n" + gen.to_json())


if __name__ == '__main__':
    main()
