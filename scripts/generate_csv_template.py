#!/usr/bin/env python3
"""
Generate CSV template for V-Mart store data import
Creates a template with sample cities for guidance
"""

import csv
from pathlib import Path

# Major Indian cities where V-Mart has presence
MAJOR_CITIES = [
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
    ("Chandigarh", "Chandigarh", "160001"),
]


def generate_template(
    output_path: str = "vmart_stores_template.csv", num_rows: int = 533
):
    """Generate CSV template for V-Mart stores"""

    headers = [
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

    print(f"📝 Generating template with {num_rows} rows...")

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for i in range(num_rows):
            city_idx = i % len(MAJOR_CITIES)
            city, state, pincode = MAJOR_CITIES[city_idx]

            # Generate sample data
            store_id = f"VM_{city[:3].upper()}_{i + 1:03d}"
            store_name = f"V-Mart {city} Store {i + 1}"
            address = f"Sample Address {i + 1}, {city}"
            phone = f"+91-{9000000000 + i}"
            manager_name = f"Manager {i + 1}"
            manager_email = f"manager{i + 1}@vmart.co.in"

            writer.writerow(
                [
                    store_id,
                    store_name,
                    address,
                    city,
                    state,
                    pincode,
                    phone,
                    manager_name,
                    manager_email,
                ]
            )

    print(f"✓ Template created: {output_path}")
    print(f"")
    print(f"Next steps:")
    print(f"1. Open {output_path} in Excel/Google Sheets")
    print(f"2. Replace sample data with actual V-Mart store information")
    print(f"3. Save the file")
    print(
        f"4. Run: python src/stores/bulk_store_importer.py import-vmart {output_path}"
    )
    print(f"")
    print(f"CSV Format:")
    print(f"  - store_id: Unique ID (e.g., VM_DEL_001)")
    print(f"  - store_name: Store name (e.g., V-Mart Delhi Central)")
    print(f"  - address: Full street address")
    print(f"  - city: City name")
    print(f"  - state: State name")
    print(f"  - pincode: PIN code")
    print(f"  - phone: Phone number with +91 prefix")
    print(f"  - manager_name: Store manager name")
    print(f"  - manager_email: Manager email")


if __name__ == "__main__":
    import sys

    output_file = sys.argv[1] if len(sys.argv) > 1 else "vmart_stores_template.csv"
    num_rows = int(sys.argv[2]) if len(sys.argv) > 2 else 533

    generate_template(output_file, num_rows)
