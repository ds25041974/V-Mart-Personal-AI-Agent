#!/usr/bin/env python3
"""
Quick QA Test for Gemini AI Insights Analyzer
Tests the enhanced features: correlation, deduplication, curation, insights
"""

import json
from urllib.parse import urlencode

import requests


# Colors for output
class C:
    G = "\033[92m"  # Green
    R = "\033[91m"  # Red
    Y = "\033[93m"  # Yellow
    B = "\033[94m"  # Blue
    C = "\033[96m"  # Cyan
    X = "\033[0m"  # Reset
    BOLD = "\033[1m"


def print_header(text):
    print(f"\n{C.BOLD}{C.C}{'=' * 80}{C.X}")
    print(f"{C.BOLD}{C.C}{text}{C.X}")
    print(f"{C.BOLD}{C.C}{'=' * 80}{C.X}\n")


def print_pass(msg):
    print(f"{C.G}✓ PASS: {msg}{C.X}")


def print_fail(msg):
    print(f"{C.R}✗ FAIL: {msg}{C.X}")


def print_info(msg):
    print(f"{C.Y}ℹ INFO: {msg}{C.X}")


# Test Data
csv_sales = """Store_ID,Date,Revenue,Sales_Count,Location
101,2024-01-15,45678,234,Delhi
102,2024-01-15,38900,189,Mumbai
103,2024-01-15,52340,267,Bangalore
101,2024-01-15,45678,234,Delhi
104,2024-01-15,41200,198,Chennai"""

csv_inventory = """Store_ID,Product_ID,Stock_Level,Reorder_Point,Category
101,P001,450,100,Electronics
101,P002,230,50,Clothing
102,P001,380,100,Electronics
103,P001,520,100,Electronics
104,P001,410,100,Electronics"""


def test_correlation_and_dedup():
    """Test 1: Cross-file correlation and duplicate detection"""
    print_header("TEST 1: CROSS-FILE CORRELATION & DUPLICATE DETECTION")

    base_url = "http://localhost:8000"
    session = requests.Session()

    # Login
    print_info("Logging in...")
    login_resp = session.post(
        f"{base_url}/email-login",
        data={"email": "test@vmart.co.in", "name": "Test User"},
    )
    if login_resp.status_code not in [200, 302]:
        print_fail(f"Login failed: {login_resp.status_code}")
        return False
    print_pass("Login successful")

    # Prepare file context
    file_context = [
        {"filename": "sales_report.csv", "content": csv_sales, "file_type": "csv"},
        {
            "filename": "inventory_data.csv",
            "content": csv_inventory,
            "file_type": "csv",
        },
    ]

    question = "Analyze Store 101 performance by correlating sales with inventory. Are there any duplicate entries?"

    # Build query parameters
    params = {
        "question": question,
        "file_context": json.dumps(file_context),
        "use_paths": "false",
        "include_weather": "false",
        "include_competitors": "false",
    }

    print_info(f"Sending request with 2 files...")
    print_info(f"Question: {question}")

    try:
        response = session.get(
            f"{base_url}/ai-chat/ask-stream", params=params, stream=True, timeout=180
        )

        if response.status_code != 200:
            print_fail(f"Request failed: {response.status_code}")
            return False

        print_pass("Request accepted, processing response...")

        full_response = ""
        progress_count = 0

        for line in response.iter_lines():
            if line:
                line_text = line.decode("utf-8")
                if line_text.startswith("data: "):
                    try:
                        event_data = json.loads(line_text[6:])
                        event_type = event_data.get("type")
                        message = event_data.get("message", "")

                        if event_type == "progress":
                            progress_count += 1
                            print(f"  {C.C}[Progress {progress_count}] {message}{C.X}")
                        elif event_type == "response":
                            full_response += message
                            print(
                                f"  {C.G}[Response] Received {len(message)} chars{C.X}"
                            )
                        elif event_type == "complete":
                            print_pass("Stream completed")
                        elif event_type == "error":
                            print_fail(f"Error: {message}")
                            return False
                    except json.JSONDecodeError:
                        continue

        print(
            f"\n{C.BOLD}Total Response Length: {len(full_response)} characters{C.X}\n"
        )

        # Analyze response for key features
        checks = {
            "correlation": [
                "correlat",
                "match",
                "store 101",
                "store_101",
                "merge",
                "cross-file",
            ],
            "duplicate": [
                "duplicate",
                "duplicated",
                "de-duplicate",
                "same entry",
                "repeated",
            ],
            "crisp_insights": ["crisp insights", "insights:", "💡"],
            "recommendations": ["recommend", "curated", "🎯"],
            "actionables": ["actionable", "strategic", "✅"],
            "summary": ["summary", "detailed", "📝"],
            "citations": ["sales_report.csv", "inventory_data.csv", "file", "from"],
            "exact_values": ["45678", "45,678", "234"],
        }

        results = {}
        for category, keywords in checks.items():
            found = any(kw.lower() in full_response.lower() for kw in keywords)
            results[category] = found
            if found:
                print_pass(f"{category.upper().replace('_', ' ')}: Detected")
            else:
                print_fail(f"{category.upper().replace('_', ' ')}: Not found")

        # Calculate score
        score = sum(results.values()) / len(results) * 100

        print(
            f"\n{C.BOLD}Overall Score: {score:.1f}% ({sum(results.values())}/{len(results)} checks){C.X}"
        )

        if score >= 75:
            print_pass(f"Test PASSED with {score:.1f}%")

            # Show sample of response
            print(f"\n{C.BOLD}Response Preview (first 500 chars):{C.X}")
            print(f"{C.Y}{full_response[:500]}...{C.X}\n")
            return True
        else:
            print_fail(f"Test FAILED with {score:.1f}%")
            print(f"\n{C.BOLD}Full Response:{C.X}")
            print(full_response)
            return False

    except Exception as e:
        print_fail(f"Test failed with error: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_data_curation():
    """Test 2: Data curation with messy data"""
    print_header("TEST 2: DATA CURATION & VALIDATION")

    base_url = "http://localhost:8000"
    session = requests.Session()

    # Login
    print_info("Logging in...")
    login_resp = session.post(
        f"{base_url}/email-login",
        data={"email": "test@vmart.co.in", "name": "Test User"},
    )
    if login_resp.status_code not in [200, 302]:
        print_fail(f"Login failed")
        return False

    # Messy data
    messy_data = """Store_ID,Date,Revenue,Sales_Count,Location
105,2024-01-15,38500,192,Pune
106,2024-01-15,,178,Hyderabad
107,2024-01-15,99999,5,Kolkata
108,2024-01-15,42300,205,Ahmedabad"""

    file_context = [
        {"filename": "messy_sales.csv", "content": messy_data, "file_type": "csv"}
    ]

    question = "Analyze this sales data. Identify any data quality issues and provide curated insights."

    params = {
        "question": question,
        "file_context": json.dumps(file_context),
        "use_paths": "false",
        "include_weather": "false",
    }

    print_info("Sending request with messy data...")

    try:
        response = session.get(
            f"{base_url}/ai-chat/ask-stream", params=params, stream=True, timeout=180
        )

        if response.status_code != 200:
            print_fail(f"Request failed: {response.status_code}")
            return False

        full_response = ""
        for line in response.iter_lines():
            if line:
                line_text = line.decode("utf-8")
                if line_text.startswith("data: "):
                    try:
                        event_data = json.loads(line_text[6:])
                        if event_data.get("type") == "response":
                            full_response += event_data.get("message", "")
                    except:
                        continue

        # Check for data quality detection
        quality_checks = {
            "missing_value": ["missing", "106", "revenue"],
            "outlier": ["outlier", "99999", "unusual"],
            "validation": ["validat", "quality", "integrity"],
            "curated": ["curat", "clean", "standardiz"],
        }

        results = {}
        for check, keywords in quality_checks.items():
            found = any(kw.lower() in full_response.lower() for kw in keywords)
            results[check] = found
            if found:
                print_pass(f"{check.upper().replace('_', ' ')}: Detected")
            else:
                print_fail(f"{check.upper().replace('_', ' ')}: Not found")

        score = sum(results.values()) / len(results) * 100
        print(f"\n{C.BOLD}Score: {score:.1f}%{C.X}")

        return score >= 50

    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False


def main():
    print_header("GEMINI AI INSIGHTS ANALYZER - QA TEST SUITE")

    results = {}

    # Test 1
    results["correlation_dedup"] = test_correlation_and_dedup()

    # Test 2
    results["data_curation"] = test_data_curation()

    # Summary
    print_header("QA TEST SUMMARY")

    passed = sum(results.values())
    total = len(results)

    print(f"\n{C.BOLD}Total Tests: {total}{C.X}")
    print(f"{C.G}Passed: {passed}{C.X}")
    print(f"{C.R}Failed: {total - passed}{C.X}")
    print(f"{C.C}Success Rate: {(passed / total) * 100:.1f}%{C.X}\n")

    for test_name, result in results.items():
        status = f"{C.G}✓ PASS{C.X}" if result else f"{C.R}✗ FAIL{C.X}"
        print(f"{test_name}: {status}")

    print()


if __name__ == "__main__":
    main()
