#!/usr/bin/env python3
"""
Comprehensive QA Testing for File Upload & AI Analysis Integration
Tests: File upload, content extraction, AI file-only reference
Run with: python run_file_upload_qa.py
"""

import os
import time
from datetime import datetime

import requests

# Configuration
BASE_URL = "http://localhost:8000"
AI_CHAT_URL = f"{BASE_URL}/ai-chat"
UPLOAD_URL = f"{AI_CHAT_URL}/upload"
ASK_URL = f"{BASE_URL}/ask"
LOGIN_URL = f"{BASE_URL}/email-login"

# Test files
TEST_PDF = "/tmp/vmart_store_performance_report.pdf"
TEST_CSV = "/tmp/vmart_sales_data.csv"

# Create a session to maintain cookies
session = requests.Session()


def login():
    """Login to get session"""
    try:
        # Use demo login
        response = session.post(f"{BASE_URL}/demo-login", timeout=5)
        if response.status_code in [200, 302]:  # 302 is redirect after successful login
            print_info("✓ Logged in (demo user)")
            return True

        print_failure(f"Demo login failed with status: {response.status_code}")
        return False
    except Exception as e:
        print_failure(f"Login error: {e}")
        return False


def print_test_header(test_num, title):
    print(f"\n{'=' * 80}")
    print(f"TEST {test_num}: {title}")
    print(f"{'=' * 80}")


def print_success(message):
    print(f"  ✅ {message}")


def print_failure(message):
    print(f"  ❌ {message}")


def print_info(message):
    print(f"  ℹ️  {message}")


def main():
    print("\n" + "=" * 80)
    print("FILE UPLOAD & AI ANALYSIS - QA TESTS")
    print("=" * 80)
    print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Server: {BASE_URL}")
    print("=" * 80)

    results = {}

    # Run tests - currently empty, add tests as needed
    # results["Server Running"] = test_server_running()

    # Print summary
    print("\n" + "=" * 80)
    print("QA TEST SUMMARY")
    print("=" * 80)

    if not results:
        print("No tests defined yet.")
        print("\n" + "=" * 80)
        return 0

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} - {test_name}")

    print("\n" + "=" * 80)
    print(f"TOTAL: {passed}/{total} tests passed ({passed / total * 100:.1f}%)")
    print("=" * 80)

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
