#!/usr/bin/env python3
"""
Gemini AI Insights Analyzer Integration Test
Tests for: File correlation, Duplicate detection, Data curation, Comprehensive insights
"""

import json
import time
from datetime import datetime

import requests


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}\n")


def print_test_name(name):
    """Print test name"""
    print(f"{Colors.BOLD}{Colors.BLUE}🧪 TEST: {name}{Colors.RESET}")


def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")


def print_failure(message):
    """Print failure message"""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ {message}{Colors.RESET}")


def create_test_csv_data():
    """Create test CSV data with some duplicates"""
    return """Store_ID,Date,Revenue,Sales_Count,Location
101,2024-01-15,45678,234,Delhi
102,2024-01-15,38900,189,Mumbai
103,2024-01-15,52340,267,Bangalore
101,2024-01-15,45678,234,Delhi
104,2024-01-15,41200,198,Chennai"""


def create_test_excel_data():
    """Create test Excel-like data (simulated as CSV) with inventory"""
    return """Store_ID,Product_ID,Stock_Level,Reorder_Point,Category
101,P001,450,100,Electronics
101,P002,230,50,Clothing
102,P001,380,100,Electronics
103,P001,520,100,Electronics
104,P001,410,100,Electronics
101,P003,180,40,Home"""


def test_file_correlation_and_deduplication(base_url, session):
    """Test 1: Cross-file correlation and duplicate detection"""
    print_test_name("Cross-File Correlation + Duplicate Detection")

    # Create test files
    csv_data = create_test_csv_data()
    excel_data = create_test_excel_data()

    # Upload files and ask a question that requires correlation
    files = {
        "files": [
            ("file", ("sales_report.csv", csv_data, "text/csv")),
            ("file", ("inventory_data.csv", excel_data, "text/csv")),
        ]
    }

    question = "Analyze Store 101 performance by correlating sales with inventory. Are there any duplicate entries?"

    data = {
        "question": question,
        "use_paths": "false",
        "include_weather": "false",
        "include_competitors": "false",
    }

    try:
        print_info(f"Sending request with 2 files and question: '{question}'")
        response = session.post(
            f"{base_url}/ai-chat/ask-stream",
            files=files["files"],
            data=data,
            stream=True,
            timeout=120,
        )

        if response.status_code != 200:
            print_failure(f"Request failed: {response.status_code}")
            return False

        full_response = ""
        correlation_found = False
        duplicate_detected = False

        for line in response.iter_lines():
            if line:
                line_text = line.decode("utf-8")
                if line_text.startswith("data: "):
                    try:
                        event_data = json.loads(line_text[6:])
                        if event_data.get("type") == "response":
                            message = event_data.get("message", "")
                            full_response += message
                            print_info(f"Response received ({len(message)} chars)")
                    except json.JSONDecodeError:
                        continue

        # Check for correlation indicators
        correlation_keywords = [
            "correlat",
            "match",
            "store 101",
            "store_101",
            "merge",
            "cross-file",
        ]
        for keyword in correlation_keywords:
            if keyword.lower() in full_response.lower():
                correlation_found = True
                break

        # Check for duplicate detection
        duplicate_keywords = [
            "duplicate",
            "duplicated",
            "de-duplicate",
            "same entry",
            "repeated",
        ]
        for keyword in duplicate_keywords:
            if keyword.lower() in full_response.lower():
                duplicate_detected = True
                break

        # Verify response quality
        checks_passed = 0
        total_checks = 5

        if correlation_found:
            print_success("✓ Cross-file correlation detected in response")
            checks_passed += 1
        else:
            print_failure("✗ No cross-file correlation found")

        if duplicate_detected:
            print_success("✓ Duplicate detection mentioned in response")
            checks_passed += 1
        else:
            print_failure("✗ No duplicate detection mentioned")

        if "store 101" in full_response.lower() or "store_101" in full_response.lower():
            print_success("✓ Store 101 analysis present")
            checks_passed += 1
        else:
            print_failure("✗ Store 101 not analyzed")

        if "45678" in full_response or "45,678" in full_response:
            print_success("✓ Exact revenue value cited")
            checks_passed += 1
        else:
            print_failure("✗ Exact values not cited")

        if len(full_response) > 500:
            print_success(f"✓ Comprehensive response ({len(full_response)} chars)")
            checks_passed += 1
        else:
            print_failure(f"✗ Response too brief ({len(full_response)} chars)")

        success_rate = (checks_passed / total_checks) * 100

        if success_rate >= 80:
            print_success(
                f"TEST PASSED: {success_rate:.1f}% ({checks_passed}/{total_checks} checks)"
            )
            return True
        else:
            print_failure(
                f"TEST FAILED: {success_rate:.1f}% ({checks_passed}/{total_checks} checks)"
            )
            return False

    except Exception as e:
        print_failure(f"Test failed with error: {str(e)}")
        return False


def test_data_curation_and_insights(base_url, session):
    """Test 2: Data curation and comprehensive insights"""
    print_test_name("Data Curation + Comprehensive Insights")

    # Create data with quality issues
    messy_data = """Store_ID,Date,Revenue,Sales_Count,Location
105,2024-01-15,38500,192,Pune
106,2024-01-15,,178,Hyderabad
107,2024-01-15,99999,5,Kolkata
108,2024-01-15,42300,205,Ahmedabad"""

    files = {"files": [("file", ("messy_sales.csv", messy_data, "text/csv"))]}

    question = "Analyze this sales data. Identify any data quality issues and provide curated insights with strategic recommendations."

    data = {
        "question": question,
        "use_paths": "false",
        "include_weather": "false",
        "include_competitors": "false",
    }

    try:
        print_info(f"Sending request with messy data")
        response = session.post(
            f"{base_url}/ai-chat/ask-stream",
            files=files["files"],
            data=data,
            stream=True,
            timeout=120,
        )

        if response.status_code != 200:
            print_failure(f"Request failed: {response.status_code}")
            return False

        full_response = ""

        for line in response.iter_lines():
            if line:
                line_text = line.decode("utf-8")
                if line_text.startswith("data: "):
                    try:
                        event_data = json.loads(line_text[6:])
                        if event_data.get("type") == "response":
                            message = event_data.get("message", "")
                            full_response += message
                    except json.JSONDecodeError:
                        continue

        # Check for required sections
        checks_passed = 0
        total_checks = 8

        required_sections = [
            ("crisp insights", "Crisp Insights section"),
            ("recommendation", "Recommendations section"),
            ("actionable", "Strategic Actionables"),
            ("summary", "Summary section"),
            ("file", "File citations"),
            ("missing", "Data quality issues identified"),
            ("store", "Store analysis"),
            ("106", "Specific store mention"),
        ]

        for keyword, description in required_sections:
            if keyword.lower() in full_response.lower():
                print_success(f"✓ {description} present")
                checks_passed += 1
            else:
                print_failure(f"✗ {description} missing")

        success_rate = (checks_passed / total_checks) * 100

        if success_rate >= 75:
            print_success(
                f"TEST PASSED: {success_rate:.1f}% ({checks_passed}/{total_checks} checks)"
            )
            return True
        else:
            print_failure(
                f"TEST FAILED: {success_rate:.1f}% ({checks_passed}/{total_checks} checks)"
            )
            return False

    except Exception as e:
        print_failure(f"Test failed with error: {str(e)}")
        return False


def test_tight_integration(base_url, session):
    """Test 3: Tight integration - response quality and structure"""
    print_test_name("Tight Integration - Response Quality")

    csv_data = """Store_ID,Month,Revenue,Target,Achievement
201,January,125000,120000,104.2%
202,January,98000,100000,98.0%
203,January,142000,130000,109.2%"""

    files = {"files": [("file", ("monthly_performance.csv", csv_data, "text/csv"))]}

    question = "Which stores exceeded targets? Provide detailed analysis with actionable recommendations."

    data = {
        "question": question,
        "use_paths": "false",
        "include_weather": "false",
        "include_competitors": "false",
    }

    try:
        print_info(f"Testing response structure and quality")
        response = session.post(
            f"{base_url}/ai-chat/ask-stream",
            files=files["files"],
            data=data,
            stream=True,
            timeout=120,
        )

        if response.status_code != 200:
            print_failure(f"Request failed: {response.status_code}")
            return False

        full_response = ""
        response_sections = []

        for line in response.iter_lines():
            if line:
                line_text = line.decode("utf-8")
                if line_text.startswith("data: "):
                    try:
                        event_data = json.loads(line_text[6:])
                        event_type = event_data.get("type")
                        if event_type == "response":
                            message = event_data.get("message", "")
                            full_response += message
                        if event_type:
                            response_sections.append(event_type)
                    except json.JSONDecodeError:
                        continue

        checks_passed = 0
        total_checks = 7

        # Check for numbered sections (1-9)
        if any(str(i) in full_response for i in range(1, 10)):
            print_success("✓ Structured response with numbered sections")
            checks_passed += 1
        else:
            print_failure("✗ Missing numbered section structure")

        # Check for specific stores
        if "201" in full_response and "203" in full_response:
            print_success("✓ Both target-exceeding stores mentioned")
            checks_passed += 1
        else:
            print_failure("✗ Not all relevant stores analyzed")

        # Check for exact values
        if "125000" in full_response or "125,000" in full_response:
            print_success("✓ Exact revenue values cited")
            checks_passed += 1
        else:
            print_failure("✗ Missing exact values")

        # Check response depth
        if len(full_response) > 800:
            print_success(f"✓ Detailed response ({len(full_response)} chars)")
            checks_passed += 1
        else:
            print_failure(f"✗ Response lacks detail ({len(full_response)} chars)")

        # Check for actionable recommendations
        action_keywords = ["recommend", "should", "action", "strategy", "implement"]
        if any(keyword in full_response.lower() for keyword in action_keywords):
            print_success("✓ Actionable recommendations present")
            checks_passed += 1
        else:
            print_failure("✗ Missing actionable recommendations")

        # Check for file citation
        if (
            "monthly_performance.csv" in full_response.lower()
            or "file" in full_response.lower()
        ):
            print_success("✓ File citations present")
            checks_passed += 1
        else:
            print_failure("✗ Missing file citations")

        # Check streaming worked
        if "complete" in response_sections:
            print_success("✓ Streaming completed successfully")
            checks_passed += 1
        else:
            print_failure("✗ Streaming may not have completed")

        success_rate = (checks_passed / total_checks) * 100

        if success_rate >= 85:
            print_success(
                f"TEST PASSED: {success_rate:.1f}% ({checks_passed}/{total_checks} checks)"
            )
            return True
        else:
            print_failure(
                f"TEST FAILED: {success_rate:.1f}% ({checks_passed}/{total_checks} checks)"
            )
            return False

    except Exception as e:
        print_failure(f"Test failed with error: {str(e)}")
        return False


def main():
    """Run all Gemini integration tests"""
    print_header("GEMINI AI INSIGHTS ANALYZER - INTEGRATION TEST SUITE")

    base_url = "http://localhost:8000"
    session = requests.Session()

    # Login
    print_info("Logging in...")
    try:
        login_response = session.post(
            f"{base_url}/email-login",
            data={"email": "test@vmart.co.in", "name": "Test User"},
        )
        if login_response.status_code not in [200, 302]:
            print_failure(
                "Login failed - make sure server is running and test account exists"
            )
            return
        print_success("Login successful")
    except Exception as e:
        print_failure(f"Could not connect to server: {str(e)}")
        return

    # Run tests
    results = {}

    print_header("TEST 1: CROSS-FILE CORRELATION & DUPLICATE DETECTION")
    results["correlation_dedup"] = test_file_correlation_and_deduplication(
        base_url, session
    )
    time.sleep(2)

    print_header("TEST 2: DATA CURATION & COMPREHENSIVE INSIGHTS")
    results["curation_insights"] = test_data_curation_and_insights(base_url, session)
    time.sleep(2)

    print_header("TEST 3: TIGHT INTEGRATION - RESPONSE QUALITY")
    results["tight_integration"] = test_tight_integration(base_url, session)

    # Summary
    print_header("TEST SUMMARY")

    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests

    print(f"\n{Colors.BOLD}Total Tests: {total_tests}{Colors.RESET}")
    print(f"{Colors.GREEN}Passed: {passed_tests}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {failed_tests}{Colors.RESET}")
    print(
        f"{Colors.CYAN}Success Rate: {(passed_tests / total_tests) * 100:.1f}%{Colors.RESET}\n"
    )

    # Detailed results
    for test_name, result in results.items():
        status = (
            f"{Colors.GREEN}✓ PASS{Colors.RESET}"
            if result
            else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        )
        print(f"{test_name}: {status}")

    print()


if __name__ == "__main__":
    main()
