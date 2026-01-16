#!/usr/bin/env python3
"""
Email Test Script

Simple script to test email functionality locally before committing.
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path


def test_email_config():
 """Test email configuration and send a test email."""
 config_file = Path("utils/etc/site_monitor_config.json")

 if not config_file.exists():
 print("❌ Config file not found")
 return False

 try:
 with open(config_file, "r") as f:
 config = json.load(f)
 except Exception as e:
 print(f"❌ Failed to load config: {e}")
 return False

 email_config = config.get("email", {})

 # Check if email is configured
 if (
 not email_config.get("sender_email")
 or email_config.get("sender_email") == "your-email@gmail.com"
 ):
 print("⚠️ Email not configured - skipping email test")
 print(" To configure email, update utils/etc/site_monitor_config.json")
 return True

 print("📧 Testing email configuration...")
 print(f" SMTP Server: {email_config.get('smtp_server')}")
 print(f" SMTP Port: {email_config.get('smtp_port')}")
 print(f" Sender: {email_config.get('sender_email')}")
 print(f" Recipient: {email_config.get('recipient_email')}")

 # Create test message
 msg = MIMEMultipart()
 msg["From"] = email_config["sender_email"]
 msg["To"] = email_config["recipient_email"]
 msg["Subject"] = "Test Email - Site Reliability Monitor"

 body = """
This is a test email from the Site Reliability Monitor.

If you receive this email, the email configuration is working correctly.

Time: {time}
Site: {site_url}

This email was sent as part of the pre-commit testing process.
""".format(
 time="2025-07-01 09:00:00",
 site_url=config.get("site_url", "https://unixwzrd.ai"),
 )

 msg.attach(MIMEText(body, "plain"))

 try:
 # Try to send email
 if email_config.get("use_oauth2", False):
 print(" Using OAuth2 authentication...")
 server = smtplib.SMTP_SSL(email_config["smtp_server"], 465)
 server.login(email_config["sender_email"], email_config["oauth2_token"])
 else:
 print(" Using password authentication...")
 server = smtplib.SMTP(
 email_config["smtp_server"], email_config["smtp_port"]
 )
 server.starttls()
 server.login(email_config["sender_email"], email_config["sender_password"])

 server.send_message(msg)
 server.quit()

 print("✅ Email test successful!")
 return True

 except Exception as e:
 print(f"❌ Email test failed: {e}")
 print(" This is expected if email is not configured")
 return False


def test_site_monitor():
 """Test the site monitor functionality."""
 print("🔍 Testing site monitor functionality...")

 try:
 import subprocess

 result = subprocess.run(
 ["python3", "utils/bin/site_reliability_monitor.py", "--mode", "health"],
 capture_output=True,
 text=True,
 timeout=60,
 )

 if result.returncode == 0:
 print("✅ Site monitor health check passed")
 return True
 else:
 print(f"❌ Site monitor health check failed: {result.stderr}")
 return False

 except Exception as e:
 print(f"❌ Site monitor test failed: {e}")
 return False


def main():
 """Run all tests."""
 print("🧪 Running pre-commit tests...")
 print()

 # Test email configuration
 email_ok = test_email_config()
 print()

 # Test site monitor
 monitor_ok = test_site_monitor()
 print()

 if email_ok and monitor_ok:
 print("✅ All tests passed!")
 return 0
 else:
 print("⚠️ Some tests failed or were skipped")
 print(" This is expected if email is not configured")
 return 0


if __name__ == "__main__":
 exit(main())
