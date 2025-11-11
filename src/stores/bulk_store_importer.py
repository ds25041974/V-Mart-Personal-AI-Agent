"""
Bulk Store Import Tool for V-Mart Store Locator
Handles importing 533+ V-Mart stores and 1300+ competitor stores
"""

import csv
import logging
from typing import Dict, List, Optional

from .database import StoreDatabase
from .google_maps_api import GoogleMapsService, StoreDataCollector
from .models import Store, StoreChain

logger = logging.getLogger(__name__)


class BulkStoreImporter:
    """
    Handles bulk import of store data from various sources
    """

    def __init__(self, db_path: str = "vmart_stores.db"):
        self.db = StoreDatabase(db_path)
        self.maps_service = GoogleMapsService()
        self.collector = StoreDataCollector(self.maps_service)
        self.import_stats = {
            "vmart_imported": 0,
            "vmart_failed": 0,
            "competitors_imported": 0,
            "competitors_failed": 0,
        }

    def import_vmart_stores_from_csv(self, csv_path: str) -> int:
        """
        Import V-Mart stores from CSV file

        CSV Format:
        store_id,store_name,address,city,state,pincode,phone,manager_name,manager_email

        Args:
            csv_path: Path to CSV file

        Returns:
            Number of stores imported
        """
        logger.info(f"Importing V-Mart stores from: {csv_path}")
        imported_count = 0

        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for idx, row in enumerate(reader, 1):
                    try:
                        # Build full address for geocoding
                        address_parts = [
                            row.get("address", ""),
                            row.get("city", ""),
                            row.get("state", ""),
                            row.get("pincode", ""),
                            "India",
                        ]
                        full_address = ", ".join(part for part in address_parts if part)

                        # Geocode address
                        geo_data = self.maps_service.geocode_address(full_address)

                        if not geo_data:
                            logger.warning(
                                f"Row {idx}: Failed to geocode {full_address}"
                            )
                            self.import_stats["vmart_failed"] += 1
                            continue

                        # Create store object using factory method
                        store = Store.create(
                            store_id=row.get("store_id", f"VM_AUTO_{idx:03d}"),
                            name=row.get("store_name", f"V-Mart Store {idx}"),
                            address=row.get("address", ""),
                            city=row.get("city", ""),
                            state=row.get("state", ""),
                            pincode=row.get("pincode", ""),
                            latitude=geo_data["latitude"],
                            longitude=geo_data["longitude"],
                            chain=StoreChain.VMART,
                            phone=row.get("phone", ""),
                            manager_name=row.get("manager_name", ""),
                            manager_email=row.get("manager_email", ""),
                        )

                        # Add to database
                        success = self.db.add_store(store)

                        if success:
                            imported_count += 1
                            self.import_stats["vmart_imported"] += 1
                            if imported_count % 50 == 0:
                                logger.info(
                                    f"✓ Imported {imported_count} V-Mart stores..."
                                )
                        else:
                            logger.warning(
                                f"Row {idx}: Failed to add store to database"
                            )
                            self.import_stats["vmart_failed"] += 1

                    except Exception as e:
                        logger.error(f"Row {idx}: Error importing store - {e}")
                        self.import_stats["vmart_failed"] += 1
                        continue

            logger.info(f"✓ Successfully imported {imported_count} V-Mart stores")
            return imported_count

        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return 0

    def import_competitor_stores_from_csv(self, csv_path: str, brand_name: str) -> int:
        """
        Import competitor stores from CSV

        CSV Format:
        store_name,address,city,state,pincode,phone

        Args:
            csv_path: Path to CSV file
            brand_name: Competitor brand ("V2", "Zudio", "Style Bazar")

        Returns:
            Number of stores imported
        """
        logger.info(f"Importing {brand_name} stores from: {csv_path}")
        imported_count = 0

        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for idx, row in enumerate(reader, 1):
                    try:
                        # Build full address
                        address_parts = [
                            row.get("address", ""),
                            row.get("city", ""),
                            row.get("state", ""),
                            row.get("pincode", ""),
                            "India",
                        ]
                        full_address = ", ".join(part for part in address_parts if part)

                        # Geocode address
                        geo_data = self.maps_service.geocode_address(full_address)

                        if not geo_data:
                            logger.warning(
                                f"Row {idx}: Failed to geocode {full_address}"
                            )
                            self.import_stats["competitors_failed"] += 1
                            continue

                        # Map brand name to StoreChain enum
                        chain_mapping = {
                            "V2": StoreChain.V2_RETAIL,
                            "Zudio": StoreChain.ZUDIO,
                            "Style Bazar": StoreChain.STYLE_BAZAR,
                        }
                        chain = chain_mapping.get(brand_name, StoreChain.OTHER)

                        # Create competitor store object
                        competitor = Store.create(
                            store_id=f"{brand_name.upper().replace(' ', '_')}_{idx:04d}",
                            name=row.get("store_name", f"{brand_name} Store {idx}"),
                            address=row.get("address", ""),
                            city=row.get("city", ""),
                            state=row.get("state", ""),
                            pincode=row.get("pincode", ""),
                            latitude=geo_data["latitude"],
                            longitude=geo_data["longitude"],
                            chain=chain,
                            phone=row.get("phone", ""),
                        )

                        # Add to database
                        success = self.db.add_competitor_store(competitor)

                        if success:
                            imported_count += 1
                            self.import_stats["competitors_imported"] += 1
                            if imported_count % 100 == 0:
                                logger.info(
                                    f"✓ Imported {imported_count} {brand_name} stores..."
                                )
                        else:
                            self.import_stats["competitors_failed"] += 1

                    except Exception as e:
                        logger.error(
                            f"Row {idx}: Error importing {brand_name} store - {e}"
                        )
                        self.import_stats["competitors_failed"] += 1
                        continue

            logger.info(f"✓ Successfully imported {imported_count} {brand_name} stores")
            return imported_count

        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return 0

    def generate_sample_vmart_data(self, output_path: str, count: int = 533):
        """
        Generate sample V-Mart store data template

        Args:
            output_path: Path to save CSV file
            count: Number of sample rows to generate
        """
        logger.info(f"Generating sample V-Mart data template: {output_path}")

        # Sample cities for distribution
        cities = [
            ("Delhi", "Delhi", "110001"),
            ("Mumbai", "Maharashtra", "400001"),
            ("Bangalore", "Karnataka", "560001"),
            ("Kolkata", "West Bengal", "700001"),
            ("Chennai", "Tamil Nadu", "600001"),
            ("Hyderabad", "Telangana", "500001"),
            ("Pune", "Maharashtra", "411001"),
            ("Ahmedabad", "Gujarat", "380001"),
            ("Jaipur", "Rajasthan", "302001"),
            ("Lucknow", "Uttar Pradesh", "226001"),
            ("Kanpur", "Uttar Pradesh", "208001"),
            ("Nagpur", "Maharashtra", "440001"),
            ("Indore", "Madhya Pradesh", "452001"),
            ("Bhopal", "Madhya Pradesh", "462001"),
            ("Patna", "Bihar", "800001"),
        ]

        try:
            with open(output_path, "w", encoding="utf-8", newline="") as f:
                fieldnames = [
                    "store_id",
                    "store_name",
                    "address",
                    "city",
                    "state",
                    "pincode",
                    "phone",
                    "manager_name",
                    "manager_email",
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for i in range(1, count + 1):
                    city, state, pincode = cities[i % len(cities)]

                    row = {
                        "store_id": f"VM_{city[:3].upper()}_{i:03d}",
                        "store_name": f"V-Mart {city} Store {i}",
                        "address": f"Shop No {i}, Market Area, {city}",
                        "city": city,
                        "state": state,
                        "pincode": pincode,
                        "phone": f"+91-{9000000000 + i}",
                        "manager_name": f"Manager {i}",
                        "manager_email": f"manager{i}@vmart.co.in",
                    }
                    writer.writerow(row)

            logger.info(f"✓ Generated {count} sample rows in {output_path}")
            logger.info("📝 Please update with actual V-Mart store data")

        except Exception as e:
            logger.error(f"Error generating sample data: {e}")

    def auto_discover_competitor_stores(
        self, brand_name: str, search_cities: Optional[List[str]] = None
    ) -> int:
        """
        Auto-discover competitor stores using Google Maps API

        Args:
            brand_name: Competitor brand name
            search_cities: List of cities to search (default: major cities)

        Returns:
            Number of stores discovered and imported
        """
        if not self.maps_service.client:
            logger.error("Google Maps API not configured. Cannot auto-discover stores.")
            return 0

        if search_cities is None:
            from stores.google_maps_api import MAJOR_INDIAN_CITIES

            search_cities = MAJOR_INDIAN_CITIES[:30]  # Top 30 cities

        logger.info(
            f"Auto-discovering {brand_name} stores in {len(search_cities)} cities..."
        )

        discovered_stores = self.collector.find_competitor_stores_nationwide(
            brand_name=brand_name, major_cities=search_cities
        )

        # Map brand name to StoreChain enum
        chain_mapping = {
            "V2": StoreChain.V2_RETAIL,
            "Zudio": StoreChain.ZUDIO,
            "Style Bazar": StoreChain.STYLE_BAZAR,
        }
        chain = chain_mapping.get(brand_name, StoreChain.OTHER)

        imported_count = 0
        for store_data in discovered_stores:
            try:
                competitor = Store.create(
                    store_id=f"{brand_name.upper().replace(' ', '_')}_{imported_count + 1:04d}",
                    name=store_data["name"],
                    address=store_data.get("address", ""),
                    city=store_data.get("city", ""),
                    state="",  # Would need reverse geocoding for state
                    pincode="",
                    latitude=store_data["latitude"],
                    longitude=store_data["longitude"],
                    chain=chain,
                    phone="",
                )

                if self.db.add_competitor_store(competitor):
                    imported_count += 1

            except Exception as e:
                logger.error(f"Error adding discovered store: {e}")
                continue

        logger.info(
            f"✓ Auto-discovered and imported {imported_count} {brand_name} stores"
        )
        return imported_count

    def get_import_summary(self) -> Dict:
        """
        Get summary of import statistics

        Returns:
            Dict with import statistics
        """
        total_vmart = self.db.get_store_count()
        total_competitors = self.db.get_competitor_count()

        return {
            "vmart_stores": {
                "total": total_vmart,
                "imported_this_session": self.import_stats["vmart_imported"],
                "failed_this_session": self.import_stats["vmart_failed"],
            },
            "competitor_stores": {
                "total": total_competitors,
                "imported_this_session": self.import_stats["competitors_imported"],
                "failed_this_session": self.import_stats["competitors_failed"],
            },
            "grand_total": total_vmart + total_competitors,
        }

    def print_summary(self):
        """Print import summary to console"""
        summary = self.get_import_summary()

        print("\n" + "=" * 60)
        print("STORE IMPORT SUMMARY")
        print("=" * 60)
        print("\n📍 V-MART STORES:")
        print(f"   Total in Database: {summary['vmart_stores']['total']}")
        print(
            f"   Imported (session): {summary['vmart_stores']['imported_this_session']}"
        )
        print(f"   Failed (session): {summary['vmart_stores']['failed_this_session']}")

        print("\n🏪 COMPETITOR STORES:")
        print(f"   Total in Database: {summary['competitor_stores']['total']}")
        print(
            f"   Imported (session): {summary['competitor_stores']['imported_this_session']}"
        )
        print(
            f"   Failed (session): {summary['competitor_stores']['failed_this_session']}"
        )

        print(f"\n📊 GRAND TOTAL: {summary['grand_total']} stores")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    import sys

    print("\n" + "=" * 60)
    print("V-MART BULK STORE IMPORTER")
    print("=" * 60)
    print("\nThis tool helps import:")
    print("• 533+ V-Mart stores")
    print("• 250+ V2 stores")
    print("• 806+ Zudio stores")
    print("• 250+ Style Bazar stores")
    print("\nTotal: 1,839+ stores with geo-location data")
    print("=" * 60 + "\n")

    importer = BulkStoreImporter()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "generate-template":
            # Generate sample CSV template
            importer.generate_sample_vmart_data("vmart_stores_template.csv", 533)
            print("\n✓ Template generated: vmart_stores_template.csv")
            print("📝 Please fill with actual V-Mart store data")

        elif command == "import-vmart":
            # Import V-Mart stores
            if len(sys.argv) < 3:
                print("Usage: python bulk_store_importer.py import-vmart <csv_file>")
                sys.exit(1)

            csv_file = sys.argv[2]
            count = importer.import_vmart_stores_from_csv(csv_file)
            importer.print_summary()

        elif command == "import-competitor":
            # Import competitor stores
            if len(sys.argv) < 4:
                print(
                    "Usage: python bulk_store_importer.py import-competitor <brand> <csv_file>"
                )
                print("Brands: 'V2', 'Zudio', 'Style Bazar'")
                sys.exit(1)

            brand = sys.argv[2]
            csv_file = sys.argv[3]
            count = importer.import_competitor_stores_from_csv(csv_file, brand)
            importer.print_summary()

        elif command == "auto-discover":
            # Auto-discover using Google Maps
            if len(sys.argv) < 3:
                print("Usage: python bulk_store_importer.py auto-discover <brand>")
                print("Brands: 'V2', 'Zudio', 'Style Bazar'")
                sys.exit(1)

            brand = sys.argv[2]
            count = importer.auto_discover_competitor_stores(brand)
            importer.print_summary()

        else:
            print(f"Unknown command: {command}")
            print("\nAvailable commands:")
            print("  generate-template    - Generate CSV template for V-Mart stores")
            print("  import-vmart <file>  - Import V-Mart stores from CSV")
            print("  import-competitor <brand> <file> - Import competitor stores")
            print("  auto-discover <brand> - Auto-discover stores via Google Maps")
    else:
        print("Usage: python bulk_store_importer.py <command> [options]")
        print("\nCommands:")
        print("  generate-template")
        print("  import-vmart <csv_file>")
        print("  import-competitor <brand> <csv_file>")
        print("  auto-discover <brand>")
        print("\nExample:")
        print("  python bulk_store_importer.py generate-template")
        print("  python bulk_store_importer.py import-vmart stores.csv")
        print(
            "  python bulk_store_importer.py import-competitor 'Zudio' zudio_stores.csv"
        )
        print("  python bulk_store_importer.py auto-discover 'V2'")
