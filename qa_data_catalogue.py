#!/usr/bin/env python3
"""
QA Test Script for Data Catalogue Configuration Feature

This script performs comprehensive quality assurance testing for:
1. HTML structure and UI elements
2. JavaScript catalogue.js module
3. IndexedDB schema and operations
4. File validation logic
5. Backend integration
6. Gemini correlation analysis

Run this before opening the browser for manual testing.

Author: DSR
Date: 2025-11-12
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path


class DataCatalogueQA:
    def __init__(self):
        self.workspace_root = Path(__file__).parent
        self.results = {
            "test_suite": "Data Catalogue Configuration QA",
            "timestamp": datetime.now().isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "errors": [],
            "warnings": [],
            "recommendations": [],
        }

    def log_pass(self, test_name):
        """Log a passing test"""
        self.results["tests_run"] += 1
        self.results["tests_passed"] += 1
        print(f"✅ {test_name}")

    def log_fail(self, test_name, error):
        """Log a failing test"""
        self.results["tests_run"] += 1
        self.results["tests_failed"] += 1
        self.results["errors"].append({"test": test_name, "error": error})
        print(f"❌ {test_name}: {error}")

    def log_warning(self, message):
        """Log a warning"""
        self.results["warnings"].append(message)
        print(f"⚠️  {message}")

    def log_recommendation(self, message):
        """Log a recommendation"""
        self.results["recommendations"].append(message)
        print(f"💡 {message}")

    def test_html_structure(self):
        """Test 1: Validate HTML structure"""
        print("\n" + "=" * 80)
        print("TEST 1: HTML STRUCTURE VALIDATION")
        print("=" * 80)

        index_path = self.workspace_root / "src/web/templates/index.html"

        if not index_path.exists():
            self.log_fail("HTML file exists", f"File not found: {index_path}")
            return

        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Test 1.1: Check for Data Catalogue tab button
        if "📚 Data Catalogue Configuration" in html_content:
            self.log_pass("Data Catalogue tab button exists")
        else:
            self.log_fail(
                "Data Catalogue tab button", "Tab button text not found in HTML"
            )

        # Test 1.2: Check for 4 file browsers
        browsers = [
            "item-master-browser",
            "store-master-browser",
            "competition-master-browser",
            "marketing-plan-browser",
        ]
        for browser_id in browsers:
            if f'id="{browser_id}"' in html_content:
                self.log_pass(f"File browser '{browser_id}' exists")
            else:
                self.log_fail(
                    f"File browser '{browser_id}'", "Browser element not found"
                )

        # Test 1.3: Check for catalogue.js inclusion
        if (
            'src="/static/catalogue.js"' in html_content
            or "src='/static/catalogue.js'" in html_content
        ):
            self.log_pass("catalogue.js script tag exists")
        else:
            self.log_fail("catalogue.js script tag", "Script tag not found in HTML")

        # Test 1.4: Check for initCatalogueDB() call
        if "initCatalogueDB()" in html_content:
            self.log_pass("initCatalogueDB() initialization call exists")
        else:
            self.log_fail("initCatalogueDB() call", "DB initialization call not found")

        # Test 1.5: Check for event handlers
        handlers = [
            "handleMasterFileSelection",
            "updateMasterInfo",
            "loadCatalogueData",
            "showCatalogueStatus",
        ]
        for handler in handlers:
            if handler in html_content:
                self.log_pass(f"Event handler '{handler}' exists")
            else:
                self.log_fail(f"Event handler '{handler}'", "Handler not found in HTML")

        # Test 1.6: Check for getAllCatalogueDataForGemini call
        if "getAllCatalogueDataForGemini()" in html_content:
            self.log_pass("Gemini integration call exists")
        else:
            self.log_fail(
                "Gemini integration", "getAllCatalogueDataForGemini() not found"
            )

    def test_catalogue_js(self):
        """Test 2: Validate catalogue.js module"""
        print("\n" + "=" * 80)
        print("TEST 2: CATALOGUE.JS MODULE VALIDATION")
        print("=" * 80)

        catalogue_path = self.workspace_root / "src/web/static/catalogue.js"

        if not catalogue_path.exists():
            self.log_fail(
                "catalogue.js file exists", f"File not found: {catalogue_path}"
            )
            return

        with open(catalogue_path, "r", encoding="utf-8") as f:
            js_content = f.read()

        # Test 2.1: Check for IndexedDB constants
        if "const DB_NAME = 'VMartCatalogueDB'" in js_content:
            self.log_pass("IndexedDB name constant defined")
        else:
            self.log_fail("IndexedDB name", "DB_NAME constant not found")

        # Test 2.2: Check for object store names
        stores = ["itemMaster", "storeMaster", "competitionMaster", "marketingPlan"]
        for store in stores:
            if f'"{store}"' in js_content or f"'{store}'" in js_content:
                self.log_pass(f"Object store '{store}' referenced")
            else:
                self.log_fail(f"Object store '{store}'", "Store name not found")

        # Test 2.3: Check for key functions
        functions = [
            "initCatalogueDB",
            "validateMasterFileName",
            "parseCSV",
            "parseMasterFile",
            "storeMasterData",
            "getMasterData",
            "getMetadata",
            "clearMasterData",
            "getAllCatalogueDataForGemini",
            "formatCatalogueDataForPrompt",
        ]
        for func in functions:
            if (
                f"function {func}" in js_content
                or f"async function {func}" in js_content
            ):
                self.log_pass(f"Function '{func}' defined")
            else:
                self.log_fail(f"Function '{func}'", "Function definition not found")

        # Test 2.4: Check for validation patterns
        validation_patterns = [
            "item.*master",
            "store.*master",
            "competition.*master",
            "marketing.*plan",
        ]
        for pattern in validation_patterns:
            if pattern in js_content.lower():
                self.log_pass(f"Validation pattern '{pattern}' exists")
            else:
                self.log_warning(
                    f"Validation pattern '{pattern}' might be missing or different"
                )

    def test_sample_data(self):
        """Test 3: Validate sample CSV files"""
        print("\n" + "=" * 80)
        print("TEST 3: SAMPLE DATA FILES VALIDATION")
        print("=" * 80)

        test_data_dir = self.workspace_root / "test_data"
        sample_files = {
            "item_master_sample.csv": ["ItemCode", "ItemName", "Category"],
            "store_master_sample.csv": ["StoreCode", "StoreName", "City"],
            "competition_master_sample.csv": ["CompetitorID", "CompetitorName"],
            "marketing_plan_sample.csv": ["CampaignID", "CampaignName"],
        }

        for filename, required_columns in sample_files.items():
            file_path = test_data_dir / filename

            if not file_path.exists():
                self.log_fail(f"Sample file {filename}", f"File not found: {file_path}")
                continue

            self.log_pass(f"Sample file '{filename}' exists")

            # Check CSV structure
            with open(file_path, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                headers = [h.strip() for h in first_line.split(",")]

                for col in required_columns:
                    if col in headers:
                        self.log_pass(f"{filename}: Column '{col}' exists")
                    else:
                        self.log_fail(
                            f"{filename}: Column '{col}'", "Required column not found"
                        )

                # Count records
                record_count = sum(1 for _ in f)
                if record_count >= 5:
                    self.log_pass(
                        f"{filename}: Has {record_count} records (minimum 5 required)"
                    )
                else:
                    self.log_warning(
                        f"{filename}: Only {record_count} records (recommend at least 10)"
                    )

    def test_backend_integration(self):
        """Test 4: Validate backend integration"""
        print("\n" + "=" * 80)
        print("TEST 4: BACKEND INTEGRATION VALIDATION")
        print("=" * 80)

        app_path = self.workspace_root / "src/web/app.py"

        if not app_path.exists():
            self.log_fail("Backend file exists", f"File not found: {app_path}")
            return

        with open(app_path, "r", encoding="utf-8") as f:
            backend_content = f.read()

        # Test 4.1: Check for catalogue_context parameter
        if 'catalogue_context = data.get("catalogue_context")' in backend_content:
            self.log_pass("Backend accepts catalogue_context parameter")
        else:
            self.log_fail(
                "catalogue_context parameter", "Parameter not found in /ask endpoint"
            )

        # Test 4.2: Check for catalogue handling logic
        if "catalogue_context and catalogue_context.get" in backend_content:
            self.log_pass("Backend processes catalogue_context")
        else:
            self.log_fail(
                "Catalogue processing logic", "Processing logic not found in backend"
            )

        # Test 4.3: Check for correlation analysis prompt
        if "CORRELATION ANALYSIS" in backend_content:
            self.log_pass("Backend includes correlation analysis prompt")
        else:
            self.log_warning("Correlation analysis prompt might be missing")

        # Test 4.4: Check for master data sections
        masters = ["itemMaster", "storeMaster", "competitionMaster", "marketingPlan"]
        for master in masters:
            if f'catalogue_data.get("{master}")' in backend_content:
                self.log_pass(f"Backend handles {master} data")
            else:
                self.log_fail(f"{master} handling", f"{master} not found in backend")

    def test_integration_flow(self):
        """Test 5: Validate end-to-end integration flow"""
        print("\n" + "=" * 80)
        print("TEST 5: END-TO-END INTEGRATION FLOW")
        print("=" * 80)

        # Test 5.1: Frontend → IndexedDB flow
        html_path = self.workspace_root / "src/web/templates/index.html"
        catalogue_path = self.workspace_root / "src/web/static/catalogue.js"

        if html_path.exists() and catalogue_path.exists():
            with open(html_path, "r") as f:
                html = f.read()
            with open(catalogue_path, "r") as f:
                js = f.read()

            # Check file selection → validation flow
            if "handleMasterFileSelection" in html and "validateMasterFileName" in js:
                self.log_pass("File selection → validation flow connected")
            else:
                self.log_fail(
                    "File selection flow", "Validation connection might be broken"
                )

            # Check storage flow
            if "storeMasterData" in html and "storeMasterData" in js:
                self.log_pass("File upload → storage flow connected")
            else:
                self.log_fail("Storage flow", "Storage connection might be broken")

        # Test 5.2: IndexedDB → Gemini flow
        if html_path.exists():
            with open(html_path, "r") as f:
                html = f.read()

            if "getAllCatalogueDataForGemini()" in html and "catalogue_context" in html:
                self.log_pass("IndexedDB → Gemini flow connected")
            else:
                self.log_fail("Gemini flow", "Gemini connection might be broken")

        # Test 5.3: Frontend → Backend flow
        app_path = self.workspace_root / "src/web/app.py"
        if html_path.exists() and app_path.exists():
            with open(html_path, "r") as f:
                html = f.read()
            with open(app_path, "r") as f:
                backend = f.read()

            if "catalogue_context" in html and "catalogue_context" in backend:
                self.log_pass("Frontend → Backend catalogue data flow connected")
            else:
                self.log_fail(
                    "Frontend-Backend flow", "Catalogue context not passed to backend"
                )

    def generate_report(self):
        """Generate final QA report"""
        print("\n" + "=" * 80)
        print("QA TEST REPORT SUMMARY")
        print("=" * 80)

        print(f"\n📊 Test Statistics:")
        print(f"   Tests Run: {self.results['tests_run']}")
        print(f"   Tests Passed: {self.results['tests_passed']} ✅")
        print(f"   Tests Failed: {self.results['tests_failed']} ❌")

        pass_rate = (
            (self.results["tests_passed"] / self.results["tests_run"] * 100)
            if self.results["tests_run"] > 0
            else 0
        )
        print(f"   Pass Rate: {pass_rate:.1f}%")

        if self.results["errors"]:
            print(f"\n❌ Errors Found ({len(self.results['errors'])}):")
            for error in self.results["errors"]:
                print(f"   - {error['test']}: {error['error']}")

        if self.results["warnings"]:
            print(f"\n⚠️  Warnings ({len(self.results['warnings'])}):")
            for warning in self.results["warnings"]:
                print(f"   - {warning}")

        if self.results["recommendations"]:
            print(f"\n💡 Recommendations ({len(self.results['recommendations'])}):")
            for rec in self.results["recommendations"]:
                print(f"   - {rec}")

        # Overall verdict
        print("\n" + "=" * 80)
        if self.results["tests_failed"] == 0:
            print("✅ ALL TESTS PASSED - READY FOR MANUAL QA")
            self.log_recommendation(
                "Proceed with browser testing: http://localhost:8000"
            )
        elif self.results["tests_failed"] <= 3:
            print("⚠️  MINOR ISSUES FOUND - PROCEED WITH CAUTION")
            self.log_recommendation("Fix errors before proceeding to manual testing")
        else:
            print("❌ CRITICAL ISSUES FOUND - FIX REQUIRED")
            self.log_recommendation("Address all critical errors before testing")

        print("=" * 80)

        # Save report
        report_path = (
            self.workspace_root
            / f"QA_REPORT_DATA_CATALOGUE_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)

        print(f"\n📄 Full report saved: {report_path}")

        return pass_rate >= 80

    def run_all_tests(self):
        """Run all QA tests"""
        print("\n" + "=" * 80)
        print("DATA CATALOGUE CONFIGURATION - QA TEST SUITE")
        print("=" * 80)
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Workspace: {self.workspace_root}")
        print("=" * 80)

        self.test_html_structure()
        self.test_catalogue_js()
        self.test_sample_data()
        self.test_backend_integration()
        self.test_integration_flow()

        return self.generate_report()


if __name__ == "__main__":
    qa = DataCatalogueQA()
    success = qa.run_all_tests()

    if success:
        print("\n🎉 QA tests completed successfully!")
        print("\n📋 Next Steps for Manual Testing:")
        print("   1. Open browser: http://localhost:8000")
        print("   2. Navigate to 'Data Catalogue Configuration' tab")
        print("   3. Upload test_data/item_master_sample.csv to Item Master browser")
        print("   4. Upload test_data/store_master_sample.csv to Store Master browser")
        print(
            "   5. Upload test_data/competition_master_sample.csv to Competition Master browser"
        )
        print(
            "   6. Upload test_data/marketing_plan_sample.csv to Marketing Plan browser"
        )
        print("   7. Open DevTools → Application → IndexedDB → VMartCatalogueDB")
        print("   8. Verify all 4 object stores have data")
        print(
            "   9. Ask Gemini: 'Which stores should focus on ethnic wear during active campaigns?'"
        )
        print("   10. Verify response includes correlation analysis from all masters")
        exit(0)
    else:
        print("\n⚠️  QA tests found issues. Please review and fix.")
        exit(1)
