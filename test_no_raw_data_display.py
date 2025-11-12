#!/usr/bin/env python3
"""
Quick test to verify that raw file data is NOT displayed in chat responses
Only file names should be referenced
"""

import json

import requests

# Test data
test_csv = """Store_ID,Date,Revenue,Sales_Count,Location
101,2024-01-15,45678,234,Delhi
102,2024-01-15,38900,189,Mumbai
103,2024-01-15,52340,267,Bangalore"""


def test_no_raw_data():
    print("\n" + "=" * 80)
    print("TEST: Verify No Raw File Data in Response")
    print("=" * 80 + "\n")

    base_url = "http://localhost:8000"
    session = requests.Session()

    # Login
    print("Logging in...")
    login_resp = session.post(
        f"{base_url}/email-login",
        data={"email": "test@vmart.co.in", "name": "Test User"},
    )

    if login_resp.status_code not in [200, 302]:
        print(f"❌ Login failed: {login_resp.status_code}")
        return False

    print("✅ Login successful\n")

    # Prepare file context
    file_context = [
        {"filename": "sales_data.csv", "content": test_csv, "file_type": "csv"}
    ]

    question = "What is the total revenue from all stores?"

    params = {
        "question": question,
        "file_context": json.dumps(file_context),
        "use_paths": "false",
        "include_weather": "false",
    }

    print(f"Question: {question}")
    print("File uploaded: sales_data.csv\n")
    print("Sending request...\n")

    try:
        response = session.get(
            f"{base_url}/ai-chat/ask-stream", params=params, stream=True, timeout=120
        )

        if response.status_code != 200:
            print(f"❌ Request failed: {response.status_code}")
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

        print("Response received!\n")
        print("=" * 80)
        print("RESPONSE ANALYSIS")
        print("=" * 80 + "\n")

        # Check if raw CSV data appears in response
        csv_lines = test_csv.strip().split("\n")
        raw_data_found = False

        for csv_line in csv_lines:
            if csv_line in full_response:
                print(f"❌ FAIL: Raw CSV data found in response: '{csv_line}'")
                raw_data_found = True

        # Check if file name is referenced
        file_name_referenced = "sales_data.csv" in full_response.lower()

        # Check for actual insights (revenue numbers)
        has_insights = any(
            num in full_response for num in ["45678", "38900", "52340", "136918"]
        )

        print(f"\n{'=' * 80}")
        print("TEST RESULTS")
        print(f"{'=' * 80}\n")

        if not raw_data_found:
            print("✅ PASS: No raw CSV data displayed in response")
        else:
            print("❌ FAIL: Raw CSV data found in response")

        if file_name_referenced:
            print("✅ PASS: File name 'sales_data.csv' referenced")
        else:
            print("⚠️  WARNING: File name not referenced")

        if has_insights:
            print("✅ PASS: Actual insights and metrics present")
        else:
            print("⚠️  WARNING: Expected metrics not found")

        print(f"\n{'=' * 80}")
        print("RESPONSE PREVIEW (first 500 chars)")
        print(f"{'=' * 80}\n")
        print(full_response[:500] + "...\n")

        # Overall result
        success = not raw_data_found and file_name_referenced and has_insights

        if success:
            print("\n✅ TEST PASSED: Response contains insights only, no raw data")
            return True
        else:
            print("\n❌ TEST FAILED: Issues detected in response format")
            print("\nFull Response:")
            print(full_response)
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_no_raw_data()
    exit(0 if success else 1)
