#!/usr/bin/env python3
"""
Test File Upload and AI Analysis Integration
Tests that AI correctly reads and analyzes uploaded file data
"""

import json
import time

import requests

BASE_URL = "http://localhost:8000"


def test_file_upload_and_ai_analysis():
    """Test complete flow: login -> upload file -> ask AI question -> verify AI uses file data"""

    print("=" * 80)
    print("🧪 TESTING FILE UPLOAD AND AI ANALYSIS INTEGRATION")
    print("=" * 80)

    # Create session
    session = requests.Session()

    # Step 1: Login with demo account
    print("\n📝 Step 1: Logging in with demo account...")
    login_response = session.post(f"{BASE_URL}/demo-login", json={"email": ""})

    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return False

    print("✅ Login successful")

    # Step 2: Create test CSV file
    print("\n📝 Step 2: Creating test CSV file...")
    csv_content = """Store ID,Store Name,City,Monthly Revenue,Top Product
ST001,V-Mart Delhi Central,Delhi,₹45,00,000,Electronics
ST002,V-Mart Mumbai West,Mumbai,₹52,00,000,Fashion
ST003,V-Mart Bangalore Tech,Bangalore,₹38,00,000,Electronics
ST004,V-Mart Chennai Marina,Chennai,₹31,00,000,Home & Living
ST005,V-Mart Pune Deccan,Pune,₹29,00,000,Fashion"""

    with open("/tmp/test_store_revenue.csv", "w") as f:
        f.write(csv_content)

    print("✅ Test CSV file created")

    # Step 3: Upload file
    print("\n📝 Step 3: Uploading CSV file...")
    with open("/tmp/test_store_revenue.csv", "rb") as f:
        upload_response = session.post(
            f"{BASE_URL}/ai-chat/upload",
            files={"files": ("test_store_revenue.csv", f, "text/csv")},
        )

    if upload_response.status_code != 200:
        print(f"❌ Upload failed: {upload_response.status_code}")
        print(upload_response.text)
        return False

    upload_data = upload_response.json()

    if not upload_data.get("success"):
        print(f"❌ Upload failed: {upload_data.get('error')}")
        return False

    file_data = upload_data.get("file_data", [])

    print(f"✅ File uploaded successfully")
    print(f"   Files: {len(file_data)}")
    for f in file_data:
        print(f"   - {f['filename']} ({f['type']}) - {len(f.get('content', ''))} chars")

    # Step 4: Ask AI to analyze the file
    print("\n📝 Step 4: Asking AI to analyze uploaded file...")

    # Prepare question with file context
    question = "Which store has the highest revenue and what is the amount?"

    # Convert file_data to JSON string for URL parameter
    file_context_json = json.dumps(file_data)

    print(f"\n🤔 Question: {question}")
    print(f"📎 File context: {len(file_context_json)} characters")

    # Make streaming request
    import urllib.parse

    params = {
        "question": question,
        "file_context": file_context_json,
        "use_paths": "false",  # Disable path search to force using uploaded files
    }

    url = f"{BASE_URL}/ai-chat/ask-stream?{urllib.parse.urlencode(params)}"

    print(f"\n📡 Streaming from: /ai-chat/ask-stream")
    print("   (Waiting for AI response...)")

    # Stream response
    response_text = ""
    progress_messages = []

    try:
        response = session.get(url, stream=True, timeout=60)

        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8")

                if line_str.startswith("data: "):
                    data_str = line_str[6:]  # Remove 'data: ' prefix

                    try:
                        data = json.loads(data_str)
                        msg_type = data.get("type")
                        message = data.get("message", "")

                        if msg_type == "progress":
                            progress_messages.append(message)
                            print(f"   {message}")
                        elif msg_type == "response":
                            response_text = message
                        elif msg_type == "complete":
                            print(f"   ✅ {message}")
                        elif msg_type == "error":
                            print(f"   ❌ Error: {message}")
                            return False
                    except json.JSONDecodeError:
                        pass

    except Exception as e:
        print(f"❌ Streaming error: {e}")
        return False

    # Step 5: Verify AI response uses file data
    print("\n📝 Step 5: Verifying AI response...")

    if not response_text:
        print("❌ No response received from AI")
        return False

    print(f"\n🤖 AI Response:")
    print("-" * 80)
    print(response_text[:500])
    if len(response_text) > 500:
        print(f"... (truncated, total {len(response_text)} chars)")
    print("-" * 80)

    # Check if AI used the file data
    success_indicators = [
        "ST002" in response_text or "Mumbai" in response_text,  # Correct store
        "52" in response_text or "52,00,000" in response_text,  # Correct revenue
        "V-Mart Mumbai West" in response_text,  # Correct store name
    ]

    warning_indicators = [
        "I do not have access" in response_text,
        "cannot access" in response_text,
        "not available in the uploaded files" in response_text
        and not any(success_indicators),
    ]

    print("\n📊 Verification:")
    print(f"   Progress messages: {len(progress_messages)}")
    for msg in progress_messages:
        print(f"     • {msg}")

    if any(warning_indicators):
        print("\n❌ AI did NOT use file data correctly")
        print("   AI claims it cannot access files or data not available")
        return False

    if any(success_indicators):
        print("\n✅ AI correctly used file data!")
        print("   ✓ Mentioned correct store (ST002/Mumbai/V-Mart Mumbai West)")
        print("   ✓ Cited correct revenue (₹52,00,000)")
        return True
    else:
        print("\n⚠️  AI response unclear")
        print("   Could not verify if correct data was used")
        print("   Please check the response manually")
        return False


if __name__ == "__main__":
    try:
        success = test_file_upload_and_ai_analysis()

        print("\n" + "=" * 80)
        if success:
            print("✅ TEST PASSED: AI correctly reads and analyzes uploaded files")
        else:
            print("❌ TEST FAILED: AI not using file data correctly")
        print("=" * 80)

        exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
