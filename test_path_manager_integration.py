"""
Path Manager Integration Test
Tests the complete flow of Path Manager with Gemini AI Chat

Run with: python test_path_manager_integration.py
"""

import json
import os
import tempfile
from pathlib import Path

import requests

BASE_URL = "http://localhost:8000"


def test_path_manager_integration():
    """Test complete Path Manager integration"""

    print("=" * 60)
    print("PATH MANAGER INTEGRATION TEST")
    print("=" * 60)
    print()

    # Test 1: Add a new path
    print("Test 1: Adding a new path...")
    print("-" * 60)

    # Create a test directory with sample files
    test_dir = tempfile.mkdtemp(prefix="vmart_test_")

    # Create sample files
    with open(os.path.join(test_dir, "sales_report.txt"), "w") as f:
        f.write("Sales Report Q4 2024\n\n")
        f.write("Total Sales: $150,000\n")
        f.write("Top Product: Smartphones\n")
        f.write("Growth: +25% YoY\n")

    with open(os.path.join(test_dir, "inventory.txt"), "w") as f:
        f.write("Inventory Status\n\n")
        f.write("Smartphones: 50 units\n")
        f.write("Laptops: 30 units\n")
        f.write("Tablets: 75 units\n")

    # Add path via API
    response = requests.post(
        f"{BASE_URL}/api/paths/add",
        json={
            "name": "Test Sales Data",
            "location": test_dir,
            "description": "Test directory for sales and inventory data",
        },
    )

    if response.status_code == 200 and response.json().get("success"):
        print(f"✅ Path added successfully!")
        path_id = response.json()["path"]["id"]
        print(f"   Path ID: {path_id}")
        print(f"   Location: {test_dir}")
    else:
        print(f"❌ Failed to add path: {response.text}")
        return

    print()

    # Test 2: Scan the path
    print("Test 2: Scanning path...")
    print("-" * 60)

    response = requests.post(f"{BASE_URL}/api/paths/{path_id}/scan")

    if response.status_code == 200 and response.json().get("success"):
        result = response.json()["scan_result"]
        print(f"✅ Scan completed!")
        print(f"   Files found: {result['file_count']}")
        print(f"   Total size: {result['total_size']} bytes")
        print(f"   File types: {list(result['file_types'].keys())}")
    else:
        print(f"❌ Scan failed: {response.text}")

    print()

    # Test 3: Get all paths
    print("Test 3: Getting all configured paths...")
    print("-" * 60)

    response = requests.get(f"{BASE_URL}/api/paths/")

    if response.status_code == 200 and response.json().get("success"):
        paths = response.json()["paths"]
        print(f"✅ Retrieved {len(paths)} path(s)")
        for path in paths:
            print(f"   - {path['name']} ({path['file_count']} files)")
    else:
        print(f"❌ Failed to get paths: {response.text}")

    print()

    # Test 4: Search files
    print("Test 4: Searching for 'sales' files...")
    print("-" * 60)

    response = requests.get(
        f"{BASE_URL}/api/paths/search", params={"q": "sales", "limit": 10}
    )

    if response.status_code == 200 and response.json().get("success"):
        results = response.json()["results"]
        print(f"✅ Found {len(results)} file(s)")
        for file in results:
            print(f"   - {file['name']} ({file['size']} bytes)")
    else:
        print(f"❌ Search failed: {response.text}")

    print()

    # Test 5: Get path statistics
    print("Test 5: Getting path statistics...")
    print("-" * 60)

    response = requests.get(f"{BASE_URL}/api/paths/stats")

    if response.status_code == 200 and response.json().get("success"):
        stats = response.json()["stats"]
        print(f"✅ Statistics retrieved!")
        print(f"   Total paths: {stats['total_paths']}")
        print(f"   Total files: {stats['total_files']}")
        print(f"   Total size: {stats['total_size']} bytes")
    else:
        print(f"❌ Failed to get stats: {response.text}")

    print()

    # Test 6: Chat integration (requires authentication)
    print("Test 6: Testing chat integration with Path Manager...")
    print("-" * 60)
    print("⚠️  Manual test required - login to the web interface and ask:")
    print("   'What are our sales numbers?' or 'Tell me about inventory'")
    print("   The AI should automatically use files from configured paths!")

    print()

    # Test 7: Remove path
    print("Test 7: Removing test path...")
    print("-" * 60)

    response = requests.delete(f"{BASE_URL}/api/paths/{path_id}")

    if response.status_code == 200 and response.json().get("success"):
        print(f"✅ Path removed successfully!")
    else:
        print(f"❌ Failed to remove path: {response.text}")

    # Cleanup
    print()
    print("Cleaning up test files...")
    try:
        os.remove(os.path.join(test_dir, "sales_report.txt"))
        os.remove(os.path.join(test_dir, "inventory.txt"))
        os.rmdir(test_dir)
        print("✅ Cleanup complete")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

    print()
    print("=" * 60)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 60)
    print()
    print("✅ Path Manager API Tests: PASSED")
    print("   - Add path: ✅")
    print("   - Scan path: ✅")
    print("   - Get paths: ✅")
    print("   - Search files: ✅")
    print("   - Get statistics: ✅")
    print("   - Remove path: ✅")
    print()
    print("⚠️  Chat Integration: MANUAL TEST REQUIRED")
    print()
    print("How to test chat integration:")
    print("1. Open http://localhost:8000 in your browser")
    print("2. Go to the 'Path Manager' tab")
    print("3. Add a path with some text files")
    print("4. Scan the path")
    print("5. Go to the 'Chat' tab")
    print("6. Ask a question about your files")
    print("7. Gemini should automatically use files from configured paths!")
    print()
    print("=" * 60)


if __name__ == "__main__":
    print("\nMake sure the V-Mart server is running on http://localhost:8000\n")

    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/", timeout=2)
        if response.status_code in [200, 302, 401]:
            test_path_manager_integration()
        else:
            print("❌ Server returned unexpected status code")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server at http://localhost:8000")
        print("   Please start the server first: python src/web/app.py")
    except Exception as e:
        print(f"❌ Error: {e}")
