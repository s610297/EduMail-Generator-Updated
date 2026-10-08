import random
import string
import sys
import argparse
import json
from datetime import datetime

class EmailGenerator:
    def __init__(self, domain="local.test"):
        self.domain = domain
        self.emails = []

    def generate_alias(self, length=10):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_custom_alias(self, pattern="user"):
        return f"{pattern}{random.randint(1000, 9999)}"

    def generate_email(self, alias=None, count=1):
        emails = []
        for _ in range(count):
            if alias is None:
                alias = self.generate_alias()
            email = f"{alias}@{self.domain}"
            emails.append(email)
            self.emails.append(email)
        return emails

    def generate_bulk(self, count=10, pattern="user"):
        emails = []
        for _ in range(count):
            alias = self.generate_custom_alias(pattern)
            email = f"{alias}@{self.domain}"
            emails.append(email)
            self.emails.append(email)
        return emails

    def save_to_file(self, filename="emails.txt"):
        with open(filename, 'w') as f:
            for email in self.emails:
                f.write(email + '\n')
        return f"Saved {len(self.emails)} emails to {filename}"

    def get_all_emails(self):
        return self.emails

    def clear(self):
        self.emails = []

    def to_json(self):
        return json.dumps({
            "domain": self.domain,
            "count": len(self.emails),
            "emails": self.emails,
            "generated_at": datetime.utcnow().isoformat()
        }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Custom Email Generator"
    )
    parser.add_argument('domain', nargs='?', default='local.test', help='Domain (e.g., ku.ac.bd)')
    parser.add_argument('--count', type=int, default=1, help='How many emails to generate')
    parser.add_argument('--pattern', default='user', help='Alias pattern (e.g., user, student, admin)')
    parser.add_argument('--save', help='Save generated emails to a file')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    parser.add_argument('--list', action='store_true', help='Output as plain list')

    args = parser.parse_args()

    gen = EmailGenerator(domain=args.domain)
    emails = gen.generate_bulk(count=args.count, pattern=args.pattern)

    if args.json:
        print(gen.to_json())
    elif args.list:
        for email in emails:
            print(email)
    else:
        for i, email in enumerate(emails, 1):
            print(f"{i}. {email}")

    if args.save:
        print(f"\n{gen.save_to_file(args.save)}")


if __name__ == '__main__':
    main()
