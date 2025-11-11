#!/usr/bin/env python3
"""
Enhanced AI Integration Test Suite
Tests all new features: ResponseFormatter, FileCrossReferencer, and integration
"""

import os
import sys

sys.path.insert(0, os.path.abspath("."))

from src.utils.file_cross_referencer import FileCrossReferencer
from src.utils.response_formatter import ResponseFormatter


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(test_name, passed, details=""):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"         {details}")


def test_response_formatter():
    """Test ResponseFormatter functionality"""
    print_section("TEST 1: Response Formatter")

    formatter = ResponseFormatter()

    # Test 1.1: Basic formatting
    sample_response = """
    Sales Analysis for Q4 2024:
    
    Total Revenue: ₹2,50,00,000 (15% growth YoY)
    Top Category: Electronics with 60% market share
    
    Key Insights:
    1. Delhi stores performing exceptionally well
    2. Electronics dominating with ₹1,50,00,000 revenue
    3. Customer retention rate improved by 12%
    
    Recommendations:
    - Consider expanding electronics inventory
    - Focus on tier-2 city expansion
    - Implement loyalty programs for high-value customers
    """

    result = formatter.format_curated_response(
        ai_response=sample_response,
        data_sources=[
            {"type": "store", "store_id": "VM_DL_001", "location": "Delhi"},
            {"type": "weather", "location": "Delhi"},
        ],
        analytics_data={"period": "Q4 2024", "source": "V-Mart Analytics"},
        include_citations=True,
    )

    # Verify structure
    test_response_formatter.passed = 0
    test_response_formatter.total = 0

    # Test insights extraction
    test_response_formatter.total += 1
    if len(result["insights"]) >= 3:
        print_result(
            "Insights Extraction", True, f"Found {len(result['insights'])} insights"
        )
        test_response_formatter.passed += 1
    else:
        print_result(
            "Insights Extraction",
            False,
            f"Only {len(result['insights'])} insights found",
        )

    # Test recommendations extraction
    test_response_formatter.total += 1
    if len(result["recommendations"]) >= 1:
        print_result(
            "Recommendations Extraction",
            True,
            f"Found {len(result['recommendations'])} recommendations",
        )
        test_response_formatter.passed += 1
    else:
        print_result("Recommendations Extraction", False, "No recommendations found")

    # Test citations generation
    test_response_formatter.total += 1
    if len(result["citations"]) >= 2:
        print_result(
            "Citations Generation",
            True,
            f"Generated {len(result['citations'])} citations",
        )
        test_response_formatter.passed += 1
    else:
        print_result(
            "Citations Generation", False, f"Only {len(result['citations'])} citations"
        )

    # Test data points extraction
    test_response_formatter.total += 1
    if len(result["data_points"]) >= 2:
        print_result(
            "Data Points Extraction",
            True,
            f"Found {len(result['data_points'])} data points",
        )
        test_response_formatter.passed += 1
    else:
        print_result("Data Points Extraction", False, "Insufficient data points")

    # Test INR formatting
    test_response_formatter.total += 1
    test_cases = [
        (25000000, "₹2.5 Cr"),
        (10200000, "₹10.2 L"),
        (1000000, "₹10 L"),
        (50000, "₹50,000.00"),
    ]

    inr_pass = True
    for amount, expected in test_cases:
        formatted = formatter._format_inr_currency(amount)
        # Allow flexibility in trailing zeros
        if not (formatted == expected or formatted.replace(".0 ", " ") == expected):
            inr_pass = False
            print(
                f"         INR Format Issue: {amount} -> {formatted} (expected ~{expected})"
            )

    if inr_pass:
        print_result("INR Currency Formatting", True, "All test cases passed")
        test_response_formatter.passed += 1
    else:
        print_result("INR Currency Formatting", False, "Some formatting issues")

    # Test metadata
    test_response_formatter.total += 1
    if "metadata" in result and result["metadata"]["sources_count"] == 2:
        print_result("Metadata Generation", True, "Correct source count")
        test_response_formatter.passed += 1
    else:
        print_result("Metadata Generation", False, "Incorrect metadata")

    print(
        f"\nResponse Formatter: {test_response_formatter.passed}/{test_response_formatter.total} tests passed"
    )
    return test_response_formatter.passed, test_response_formatter.total


def test_file_cross_referencer():
    """Test FileCrossReferencer functionality"""
    print_section("TEST 2: File Cross Referencer")

    cross_ref = FileCrossReferencer()

    # Read test data files
    test_files = []
    test_data_dir = "tests/test_data"

    # Sales data
    with open(f"{test_data_dir}/sales_january.csv", "r") as f:
        test_files.append(
            {"name": "sales_january.csv", "content": f.read(), "format": "csv"}
        )

    # Inventory data
    with open(f"{test_data_dir}/inventory_january.csv", "r") as f:
        test_files.append(
            {"name": "inventory_january.csv", "content": f.read(), "format": "csv"}
        )

    # Performance report
    with open(f"{test_data_dir}/performance_report.txt", "r") as f:
        test_files.append(
            {"name": "performance_report.txt", "content": f.read(), "format": "txt"}
        )

    # Run analysis
    analysis = cross_ref.analyze_multiple_files(test_files)

    test_file_cross_referencer.passed = 0
    test_file_cross_referencer.total = 0

    # Test files analyzed
    test_file_cross_referencer.total += 1
    if analysis["files_analyzed"] == 3:
        print_result(
            "Files Analyzed Count", True, f"{analysis['files_analyzed']} files"
        )
        test_file_cross_referencer.passed += 1
    else:
        print_result(
            "Files Analyzed Count",
            False,
            f"Expected 3, got {analysis['files_analyzed']}",
        )

    # Test cross-references found
    test_file_cross_referencer.total += 1
    if len(analysis["cross_references"]) >= 5:
        print_result(
            "Cross-References Detection",
            True,
            f"Found {len(analysis['cross_references'])} cross-refs",
        )
        test_file_cross_referencer.passed += 1

        # Show sample cross-references
        print("\n   Sample Cross-References:")
        for ref in analysis["cross_references"][:3]:
            print(
                f"   • {ref['type'].upper()}: {ref['file1']} ↔ {ref['file2']} ({ref['count']} matches)"
            )
    else:
        print_result(
            "Cross-References Detection",
            False,
            f"Only {len(analysis['cross_references'])} found",
        )

    # Test insights generation
    test_file_cross_referencer.total += 1
    if len(analysis["insights"]) >= 2:
        print_result(
            "Insights Generation",
            True,
            f"Generated {len(analysis['insights'])} insights",
        )
        test_file_cross_referencer.passed += 1

        print("\n   Generated Insights:")
        for insight in analysis["insights"]:
            print(f"   • {insight}")
    else:
        print_result("Insights Generation", False, "Insufficient insights")

    # Test report formatting
    test_file_cross_referencer.total += 1
    report = cross_ref.format_cross_reference_report(analysis)
    if len(report) > 500 and "CROSS-REFERENCE ANALYSIS" in report:
        print_result(
            "Report Formatting", True, f"Report generated ({len(report)} chars)"
        )
        test_file_cross_referencer.passed += 1
    else:
        print_result("Report Formatting", False, "Report incomplete")

    # Test specific data search
    test_file_cross_referencer.total += 1
    search_results = cross_ref.find_data_in_files("PRD1234", test_files)
    if len(search_results) >= 2:
        print_result(
            "Data Search", True, f"Found 'PRD1234' in {len(search_results)} files"
        )
        test_file_cross_referencer.passed += 1
    else:
        print_result("Data Search", False, "Search failed")

    # Test pattern detection
    test_file_cross_referencer.total += 1
    patterns_found = set()
    for ref in analysis["cross_references"]:
        patterns_found.add(ref["type"])

    if len(patterns_found) >= 3:
        print_result(
            "Pattern Detection",
            True,
            f"Detected {len(patterns_found)} pattern types: {', '.join(patterns_found)}",
        )
        test_file_cross_referencer.passed += 1
    else:
        print_result(
            "Pattern Detection", False, f"Only {len(patterns_found)} patterns detected"
        )

    print(
        f"\nFile Cross Referencer: {test_file_cross_referencer.passed}/{test_file_cross_referencer.total} tests passed"
    )
    return test_file_cross_referencer.passed, test_file_cross_referencer.total


def test_integration():
    """Test integration of both components"""
    print_section("TEST 3: Integration Testing")

    formatter = ResponseFormatter()
    cross_ref = FileCrossReferencer()

    test_integration.passed = 0
    test_integration.total = 0

    # Test 3.1: Multi-file analysis with curated response
    test_data_dir = "tests/test_data"

    test_files = []
    with open(f"{test_data_dir}/sales_january.csv", "r") as f:
        test_files.append(
            {"name": "sales_january.csv", "content": f.read(), "format": "csv"}
        )

    with open(f"{test_data_dir}/inventory_january.csv", "r") as f:
        test_files.append(
            {"name": "inventory_january.csv", "content": f.read(), "format": "csv"}
        )

    # Perform cross-reference analysis
    cross_analysis = cross_ref.analyze_multiple_files(test_files)

    # Create mock AI response
    mock_ai_response = """
    Based on the analyzed files, here are the key findings:
    
    Sales Performance:
    - Total revenue across stores: ₹18,95,000
    - Best performing store: VM_DL_001 with ₹7,95,000
    - Top product: PRD1234 (Samsung Galaxy S24)
    
    Inventory Analysis:
    - Total stock value: ₹98,75,000
    - Stock levels are healthy for most products
    - PRD1234 has 655 units available across all stores
    
    Cross-File Insights:
    1. Sales and inventory data align perfectly for Store VM_DL_001
    2. Product PRD1234 appears in both sales and inventory consistently
    3. Strong correlation between stock availability and sales performance
    
    Recommendations:
    - Maintain current inventory levels for high-demand products
    - Consider promotional activities for slower-moving items
    - Monitor PRD5678 for potential stock increase based on growing demand
    """

    # Format response with citations
    curated = formatter.format_curated_response(
        ai_response=mock_ai_response,
        data_sources=[{"type": "files", "count": len(test_files)}],
        file_references=[
            {"name": f["name"], "format": f["format"]} for f in test_files
        ],
        include_citations=True,
    )

    # Test combined output
    test_integration.total += 1
    if (
        curated["insights"]
        and curated["citations"]
        and cross_analysis["cross_references"]
    ):
        print_result(
            "Multi-File Analysis Integration",
            True,
            f"{len(curated['insights'])} insights + {len(curated['citations'])} citations + {len(cross_analysis['cross_references'])} cross-refs",
        )
        test_integration.passed += 1
    else:
        print_result("Multi-File Analysis Integration", False, "Integration incomplete")

    # Test multi-file report formatting
    test_integration.total += 1
    multi_file_report = formatter.format_multi_file_analysis(
        test_files, cross_analysis["cross_references"]
    )

    if "MULTI-FILE ANALYSIS" in multi_file_report and len(multi_file_report) > 200:
        print_result(
            "Multi-File Report Generation",
            True,
            f"Report: {len(multi_file_report)} chars",
        )
        test_integration.passed += 1
    else:
        print_result("Multi-File Report Generation", False, "Report formatting issue")

    # Test data table creation
    test_integration.total += 1
    headers = ["Store", "Product", "Sales", "Stock"]
    rows = [
        ["VM_DL_001", "PRD1234", "₹2,50,000", "150 units"],
        ["VM_MH_001", "PRD1234", "₹3,00,000", "200 units"],
    ]

    table = formatter.create_data_table(headers, rows, "Sales vs Inventory")
    if "SALES VS INVENTORY" in table and "VM_DL_001" in table:
        print_result("Data Table Creation", True, "Table formatted correctly")
        test_integration.passed += 1
    else:
        print_result("Data Table Creation", False, "Table formatting issue")

    print(
        f"\nIntegration Tests: {test_integration.passed}/{test_integration.total} tests passed"
    )
    return test_integration.passed, test_integration.total


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  ENHANCED AI INTEGRATION - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print("\nTesting Date: November 11, 2025")
    print("Components: ResponseFormatter, FileCrossReferencer, Integration")

    # Run all tests
    rf_passed, rf_total = test_response_formatter()
    fc_passed, fc_total = test_file_cross_referencer()
    int_passed, int_total = test_integration()

    # Summary
    print_section("FINAL SUMMARY")

    total_passed = rf_passed + fc_passed + int_passed
    total_tests = rf_total + fc_total + int_total

    success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

    print(
        f"\nResponse Formatter:     {rf_passed}/{rf_total} ({rf_passed / rf_total * 100:.1f}%)"
    )
    print(
        f"File Cross Referencer:  {fc_passed}/{fc_total} ({fc_passed / fc_total * 100:.1f}%)"
    )
    print(
        f"Integration Tests:      {int_passed}/{int_total} ({int_passed / int_total * 100:.1f}%)"
    )
    print(f"\n{'=' * 70}")
    print(
        f"OVERALL RESULT: {total_passed}/{total_tests} tests passed ({success_rate:.1f}%)"
    )
    print(f"{'=' * 70}")

    if success_rate >= 90:
        print("\n✅ EXCELLENT - System ready for production!")
    elif success_rate >= 75:
        print("\n⚠️  GOOD - Minor issues need attention")
    else:
        print("\n❌ NEEDS WORK - Significant issues detected")

    print("\nNext Steps:")
    print("1. Start server: python main.py")
    print("2. Upload test files from tests/test_data/")
    print("3. Test multi-file analysis in UI")
    print("4. Verify curated responses with insights/citations")
    print("5. Test with live store/weather data integration")

    return 0 if success_rate >= 90 else 1


if __name__ == "__main__":
    sys.exit(main())
