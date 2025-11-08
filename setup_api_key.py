#!/usr/bin/env python3
"""
Setup script to configure Gemini API key
"""

import os
import sys


def setup_api_key():
    """Interactive setup for Gemini API key"""

    print("=" * 70)
    print("🔑 V-Mart AI Agent - API Key Setup")
    print("=" * 70)
    print()

    print("You have the project: gen-lang-client-0157247224")
    print()
    print("To get your API key:")
    print("1. Go to: https://aistudio.google.com/app/apikey")
    print("2. Select project: gen-lang-client-0157247224")
    print("3. Click 'Create API Key'")
    print("4. Copy the key (starts with AIza...)")
    print()
    print("=" * 70)
    print()

    api_key = input("Paste your Gemini API key here: ").strip()

    if not api_key:
        print("❌ No API key provided. Exiting.")
        sys.exit(1)

    if not api_key.startswith("AIza"):
        print("⚠️  Warning: API key should start with 'AIza'")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != "y":
            print("❌ Setup cancelled.")
            sys.exit(1)

    # Read current .env
    env_path = os.path.join(os.path.dirname(__file__), ".env")

    try:
        with open(env_path, "r") as f:
            lines = f.readlines()

        # Update the GEMINI_API_KEY line
        updated = False
        for i, line in enumerate(lines):
            if line.startswith("GEMINI_API_KEY="):
                lines[i] = f"GEMINI_API_KEY={api_key}\n"
                updated = True
                break

        if not updated:
            print("❌ Could not find GEMINI_API_KEY in .env file")
            sys.exit(1)

        # Write back
        with open(env_path, "w") as f:
            f.writelines(lines)

        print()
        print("=" * 70)
        print("✅ API Key successfully configured!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("1. Restart the server: python3 main.py")
        print("2. Open browser: http://localhost:8000")
        print("3. Click 'Enter Demo Mode'")
        print("4. Start chatting!")
        print()
        print("The API key is now available for all users accessing your server.")
        print("=" * 70)

    except FileNotFoundError:
        print(f"❌ .env file not found at: {env_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_api_key()
