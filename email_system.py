import random
import string
import json
import os
from datetime import datetime

class PersistentMailSystem:
    def __init__(self, domain="local.test", data_file="mail_data.json"):
        self.domain = domain
        self.data_file = data_file
        self.users = self.load_data()

    def load_data(self):
        """File থেকে data load করবে"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_data(self):
        """Data file-এ save করবে"""
        with open(self.data_file, 'w') as f:
            json.dump(self.users, f, indent=2)

    def create_user(self, alias):
        """User/email create করবে"""
        alias = alias.strip().lower()
        email = f"{alias}@{self.domain}"
        
        if email not in self.users:
            self.users[email] = {
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "otp": None,
                "messages": []
            }
            self.save_data()
        
        return email

    def generate_random_email(self, pattern="user"):
        """Random email generate করবে"""
        alias = f"{pattern}{random.randint(1000, 9999)}"
        return self.create_user(alias)

    def generate_otp(self, email, length=6):
        """OTP generate করবে"""
        if email not in self.users:
            return None
        
        otp = "".join(random.choice(string.digits) for _ in range(length))
        self.users[email]["otp"] = otp
        self.users[email]["messages"].append({
            "from": "system@local",
            "subject": "Your OTP Code",
            "body": f"Your OTP is: {otp}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_data()
        return otp

    def send_message(self, to_email, sender, subject, body):
        """Message send করবে"""
        if to_email not in self.users:
            return False
        
        self.users[to_email]["messages"].append({
            "from": sender,
            "subject": subject,
            "body": body,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_data()
        return True

    def view_inbox(self, email):
        """Inbox দেখবে"""
        if email not in self.users:
            return None
        
        data = self.users[email]
        output = f"\n{'='*60}\n"
        output += f"Email: {email}\n"
        output += f"Created: {data['created_at']}\n"
        output += f"Current OTP: {data['otp'] or 'Not generated yet'}\n"
        output += f"Messages: {len(data['messages'])}\n"
        output += f"{'='*60}\n"

        if not data["messages"]:
            output += "\nNo messages yet.\n"
            return output

        for i, msg in enumerate(data["messages"], 1):
            output += f"\n{i}. From: {msg['from']}\n"
            output += f"   Subject: {msg['subject']}\n"
            output += f"   Time: {msg['timestamp']}\n"
            output += f"   Body: {msg['body']}\n"

        return output

    def list_all_emails(self):
        """সব email list করবে"""
        return list(self.users.keys())

    def dump_json(self):
        """সব data JSON-এ return করবে"""
        return json.dumps(self.users, indent=2)

    def clear_all(self):
        """সব data clear করবে"""
        self.users = {}
        self.save_data()
        return "All data cleared"
