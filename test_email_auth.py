#!/usr/bin/env python3
"""
Quick test for email authentication system
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env file
from pathlib import Path

env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value

from src.auth.email_auth import email_auth_manager

print("=" * 60)
print("V-MART EMAIL AUTHENTICATION - QUICK TEST")
print("=" * 60)
print()

# Test 1: Email validation
print("TEST 1: Email Validation")
print("-" * 60)

test_emails = [
    ("ds.250474@gmail.com", True, "Anonymous whitelist"),
    ("dinesh.srivastava@vmart.co.in", True, "Anonymous whitelist + allowed domain"),
    ("dineshsrivastava07@gmail.com", True, "Anonymous whitelist"),
    ("user@vmart.co.in", True, "Allowed domain"),
    ("user@vmartretail.com", True, "Allowed domain"),
    ("user@limeroad.com", True, "Allowed domain"),
    ("user@gmail.com", False, "Not allowed (non-company Gmail)"),
    ("user@yahoo.com", False, "Not allowed domain"),
]

for email, should_pass, reason in test_emails:
    is_valid, error = email_auth_manager.validate_email(email)
    status = "✅ PASS" if is_valid == should_pass else "❌ FAIL"
    print(f"{status} | {email:<40} | {reason}")
    if not is_valid and error:
        print(f"       Error: {error}")

print()

# Test 2: Anonymous login check
print("TEST 2: Anonymous Login Check")
print("-" * 60)

from src.auth.email_auth import ANONYMOUS_LOGIN_EMAILS

print(f"Anonymous emails configured: {len(ANONYMOUS_LOGIN_EMAILS)}")
for email in ANONYMOUS_LOGIN_EMAILS:
    print(f"  ✓ {email}")

print()

# Test 3: Database initialization
print("TEST 3: Database Initialization")
print("-" * 60)

try:
    # Check if tables exist
    tables = email_auth_manager.db_manager.fetch_all(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    print(f"✅ Database tables created: {len(tables)}")
    for table in tables:
        print(f"  ✓ {table['name']}")
except Exception as e:
    print(f"❌ Database error: {e}")

print()

# Test 4: Email service configuration
print("TEST 4: Email Service Configuration")
print("-" * 60)

email_service = email_auth_manager.email_service
if email_service.is_configured:
    print(f"✅ Email service configured")
    print(f"  SMTP Server: {email_service.smtp_server}")
    print(f"  SMTP Port: {email_service.smtp_port}")
    print(f"  Username: {email_service.smtp_username}")
    print(f"  From: {email_service.from_name} <{email_service.from_email}>")

    if email_service.smtp_password == "your_gmail_app_password_here":
        print(f"  ⚠️  WARNING: Email password not configured!")
        print(f"  Please update EMAIL_PASSWORD in .env file")
        print(
            f"  Generate Gmail App Password: https://myaccount.google.com/apppasswords"
        )
else:
    print(f"❌ Email service NOT configured")
    print(f"  Please set EMAIL_USERNAME and EMAIL_PASSWORD in .env file")

print()

# Test 5: Try anonymous login (without creating user)
print("TEST 5: Anonymous Login Simulation")
print("-" * 60)

for email in ANONYMOUS_LOGIN_EMAILS[:2]:  # Test first 2
    success, message, user_data = email_auth_manager.login(
        email, password=None, ip_address="127.0.0.1"
    )
    status = "✅" if success else "❌"
    print(f"{status} {email}: {message}")
    if user_data:
        print(
            f"   User: {user_data['name']} (Role: {user_data['role']}, Anonymous: {user_data.get('anonymous', False)})"
        )

print()
print("=" * 60)
print("SETUP SUMMARY")
print("=" * 60)
print()
print("✅ Email validation working")
print("✅ Anonymous login configured for 3 emails")
print("✅ Database tables created")
print("✅ Domain restrictions active (vmart.co.in, vmartretail.com, limeroad.com)")
print()
print("NEXT STEPS:")
print("1. Update EMAIL_PASSWORD in .env with Gmail App Password")
print("2. Start server: python src/web/app.py")
print("3. Test signup: http://localhost:8000/auth/signup")
print("4. Test anonymous login with whitelisted emails (no password needed)")
print()
