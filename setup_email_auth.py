"""
Email Configuration Setup for V-Mart Personal AI Agent
Run this once to configure email settings for authentication
"""

from pathlib import Path


def setup_email_config():
    """Setup email configuration in .env file"""

    print("=" * 60)
    print("V-MART AI AGENT - EMAIL CONFIGURATION SETUP")
    print("=" * 60)
    print()

    # Check if .env exists
    env_path = Path(".env")

    if env_path.exists():
        with open(env_path, "r") as f:
            existing_content = f.read()
    else:
        existing_content = ""

    # Email configuration
    print("Email Service Configuration")
    print("-" * 60)
    print()
    print("Choose email service:")
    print("1. Gmail (recommended for testing)")
    print("2. Outlook/Office365")
    print("3. Custom SMTP")
    print()

    choice = input("Enter your choice (1-3): ").strip()

    if choice == "1":
        # Gmail
        print("\nGmail Configuration:")
        print("⚠️  You need to generate an App Password:")
        print("   1. Go to https://myaccount.google.com/security")
        print("   2. Enable 2-Step Verification")
        print("   3. Generate App Password")
        print()

        email = input("Enter your Gmail address: ").strip()
        password = input("Enter your App Password: ").strip()

        email_config = f"""
# Email Configuration (Gmail)
EMAIL_SERVICE=gmail
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_USERNAME={email}
EMAIL_PASSWORD={password}
EMAIL_FROM_NAME=V-Mart AI Agent
EMAIL_FROM_ADDRESS={email}
"""

    elif choice == "2":
        # Outlook
        email = input("Enter your Outlook email: ").strip()
        password = input("Enter your password: ").strip()

        email_config = f"""
# Email Configuration (Outlook)
EMAIL_SERVICE=outlook
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_USERNAME={email}
EMAIL_PASSWORD={password}
EMAIL_FROM_NAME=V-Mart AI Agent
EMAIL_FROM_ADDRESS={email}
"""

    else:
        # Custom SMTP
        print("\nCustom SMTP Configuration:")
        host = input("SMTP Host (e.g., smtp.example.com): ").strip()
        port = input("SMTP Port (usually 587 or 465): ").strip()
        use_tls = input("Use TLS? (yes/no): ").strip().lower() == "yes"
        username = input("SMTP Username: ").strip()
        password = input("SMTP Password: ").strip()
        from_address = input("From Email Address: ").strip()

        email_config = f"""
# Email Configuration (Custom SMTP)
EMAIL_SERVICE=custom
EMAIL_HOST={host}
EMAIL_PORT={port}
EMAIL_USE_TLS={"true" if use_tls else "false"}
EMAIL_USERNAME={username}
EMAIL_PASSWORD={password}
EMAIL_FROM_NAME=V-Mart AI Agent
EMAIL_FROM_ADDRESS={from_address}
"""

    # Application URL for verification links
    print("\nApplication URL Configuration:")
    print("This is used for email verification links")
    print("Examples:")
    print("  - Development: http://localhost:8000")
    print("  - Production: https://vmart-ai.example.com")
    print()

    app_url = input("Enter your application URL: ").strip()
    if not app_url.startswith(("http://", "https://")):
        app_url = "http://" + app_url

    email_config += f"\n# Application URL\nAPP_URL={app_url}\n"

    # Check if email config already exists
    if "EMAIL_SERVICE" in existing_content:
        print("\n⚠️  Email configuration already exists in .env")
        overwrite = input("Overwrite? (yes/no): ").strip().lower()
        if overwrite != "yes":
            print("Configuration cancelled.")
            return

        # Remove old email config
        lines = existing_content.split("\n")
        new_lines = []
        skip = False
        for line in lines:
            if "# Email Configuration" in line:
                skip = True
            elif skip and line.startswith("#") and "Email" not in line:
                skip = False
            elif skip and line.startswith(("EMAIL_", "APP_URL")):
                continue
            elif not skip:
                new_lines.append(line)

        existing_content = "\n".join(new_lines)

    # Write configuration
    with open(env_path, "w") as f:
        f.write(existing_content.rstrip() + "\n" + email_config)

    print("\n" + "=" * 60)
    print("✅ Email configuration saved to .env")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Restart your application server")
    print("2. Navigate to http://localhost:8000/auth/signup")
    print("3. Create an account and check your email for verification")
    print()
    print("Note: Make sure .env is in .gitignore to keep credentials secure!")
    print()


if __name__ == "__main__":
    setup_email_config()
