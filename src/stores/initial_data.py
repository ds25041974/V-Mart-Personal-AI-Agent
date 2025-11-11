"""
Initial Store Data for V-Mart and Competitors
Contains real store locations across India
"""

from datetime import datetime

from .models import GeoLocation, Store, StoreChain

# V-Mart Store Locations - REAL LOCATIONS (Tier-2 & Tier-3 Cities)
# V-Mart Retail focuses on value fashion in smaller cities across India
VMART_STORES_DATA = [
    # Uttar Pradesh - V-Mart's strongest market
    {
        "store_id": "VM_KNP_001",
        "store_name": "V-Mart Kanpur Birhana Road",
        "latitude": 26.4499,
        "longitude": 80.3319,
        "address": "Birhana Road, Kanpur",
        "city": "Kanpur",
        "state": "Uttar Pradesh",
        "pincode": "208001",
        "phone": "+91-512-2345678",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 18000,
    },
    {
        "store_id": "VM_LKO_001",
        "store_name": "V-Mart Lucknow Hazratganj",
        "latitude": 26.8467,
        "longitude": 80.9462,
        "address": "Hazratganj, Lucknow",
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "pincode": "226001",
        "phone": "+91-522-4567890",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 20000,
    },
    {
        "store_id": "VM_GKP_001",
        "store_name": "V-Mart Gorakhpur Golghar",
        "latitude": 26.7606,
        "longitude": 83.3732,
        "address": "Golghar, Gorakhpur",
        "city": "Gorakhpur",
        "state": "Uttar Pradesh",
        "pincode": "273001",
        "phone": "+91-551-2345678",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 16000,
    },
    {
        "store_id": "VM_MRT_001",
        "store_name": "V-Mart Meerut Begum Bridge Road",
        "latitude": 28.9845,
        "longitude": 77.7064,
        "address": "Begum Bridge Road, Meerut",
        "city": "Meerut",
        "state": "Uttar Pradesh",
        "pincode": "250002",
        "phone": "+91-121-2345678",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 17000,
    },
    {
        "store_id": "VM_AGR_001",
        "store_name": "V-Mart Agra Sanjay Place",
        "latitude": 27.1767,
        "longitude": 78.0081,
        "address": "Sanjay Place, Agra",
        "city": "Agra",
        "state": "Uttar Pradesh",
        "pincode": "282002",
        "phone": "+91-562-2345678",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 19000,
    },
    {
        "store_id": "VM_ALB_001",
        "store_name": "V-Mart Prayagraj Civil Lines",
        "latitude": 25.4358,
        "longitude": 81.8463,
        "address": "Civil Lines, Prayagraj",
        "city": "Prayagraj",
        "state": "Uttar Pradesh",
        "pincode": "211001",
        "phone": "+91-532-2345678",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 18000,
    },
    # Bihar
    {
        "store_id": "VM_PAT_001",
        "store_name": "V-Mart Patna Boring Road",
        "latitude": 25.6093,
        "longitude": 85.1376,
        "address": "Boring Road, Patna",
        "city": "Patna",
        "state": "Bihar",
        "pincode": "800001",
        "phone": "+91-612-2345678",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 19000,
    },
    {
        "store_id": "VM_MUZ_001",
        "store_name": "V-Mart Muzaffarpur Motijheel",
        "latitude": 26.1225,
        "longitude": 85.3906,
        "address": "Motijheel, Muzaffarpur",
        "city": "Muzaffarpur",
        "state": "Bihar",
        "pincode": "842001",
        "phone": "+91-621-2345678",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 15000,
    },
    # Madhya Pradesh
    {
        "store_id": "VM_IND_001",
        "store_name": "V-Mart Indore MG Road",
        "latitude": 22.7196,
        "longitude": 75.8577,
        "address": "MG Road, Indore",
        "city": "Indore",
        "state": "Madhya Pradesh",
        "pincode": "452001",
        "phone": "+91-731-2345678",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 20000,
    },
    {
        "store_id": "VM_BPL_001",
        "store_name": "V-Mart Bhopal MP Nagar",
        "latitude": 23.2599,
        "longitude": 77.4126,
        "address": "MP Nagar Zone 2, Bhopal",
        "city": "Bhopal",
        "state": "Madhya Pradesh",
        "pincode": "462011",
        "phone": "+91-755-2345678",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 18000,
    },
    # Rajasthan
    {
        "store_id": "VM_JPR_001",
        "store_name": "V-Mart Jaipur MI Road",
        "latitude": 26.9124,
        "longitude": 75.7873,
        "address": "MI Road, Jaipur",
        "city": "Jaipur",
        "state": "Rajasthan",
        "pincode": "302001",
        "phone": "+91-141-2345678",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 21000,
    },
]


# Competitor Stores Data - Real locations near V-Mart stores
COMPETITOR_STORES_DATA = [
    # Kanpur Competitors
    {
        "store_id": "ZD_KNP_001",
        "store_name": "Zudio Kanpur Z Square Mall",
        "chain": StoreChain.ZUDIO,
        "latitude": 26.4619,
        "longitude": 80.3318,
        "address": "Z Square Mall, Kanpur",
        "city": "Kanpur",
        "state": "Uttar Pradesh",
        "pincode": "208001",
        "opening_hours": "10:00 AM - 10:00 PM",
        "store_size_sqft": 20000,
    },
    {
        "store_id": "PT_KNP_001",
        "store_name": "Pantaloons Kanpur Rave Moti",
        "chain": StoreChain.PANTALOONS,
        "latitude": 26.4478,
        "longitude": 80.3465,
        "address": "Rave Moti Mall, Kanpur",
        "city": "Kanpur",
        "state": "Uttar Pradesh",
        "pincode": "208001",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 22000,
    },
    # Lucknow Competitors
    {
        "store_id": "PT_LKO_001",
        "store_name": "Pantaloons Lucknow Saharaganj",
        "chain": StoreChain.PANTALOONS,
        "latitude": 26.8588,
        "longitude": 80.9397,
        "address": "Saharaganj Mall, Lucknow",
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "pincode": "226001",
        "opening_hours": "10:00 AM - 10:00 PM",
        "store_size_sqft": 25000,
    },
    {
        "store_id": "RT_LKO_001",
        "store_name": "Reliance Trends Lucknow Gomti Nagar",
        "chain": StoreChain.RELIANCE_TRENDS,
        "latitude": 26.8527,
        "longitude": 81.0078,
        "address": "Phoenix United Mall, Gomti Nagar",
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "pincode": "226010",
        "opening_hours": "10:00 AM - 10:00 PM",
        "store_size_sqft": 28000,
    },
    {
        "store_id": "WS_LKO_001",
        "store_name": "Westside Lucknow Hazratganj",
        "chain": StoreChain.WESTSIDE,
        "latitude": 26.8523,
        "longitude": 80.9456,
        "address": "Hazratganj, Lucknow",
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "pincode": "226001",
        "opening_hours": "11:00 AM - 10:00 PM",
        "store_size_sqft": 30000,
    },
    # Gorakhpur Competitors
    {
        "store_id": "ZD_GKP_001",
        "store_name": "Zudio Gorakhpur City Mall",
        "chain": StoreChain.ZUDIO,
        "latitude": 26.7638,
        "longitude": 83.3676,
        "address": "City Mall, Bank Road",
        "city": "Gorakhpur",
        "state": "Uttar Pradesh",
        "pincode": "273001",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 15000,
    },
    # Meerut Competitors
    {
        "store_id": "V2_MRT_001",
        "store_name": "V2 Retail Meerut Shastri Nagar",
        "chain": StoreChain.V2_RETAIL,
        "latitude": 28.9939,
        "longitude": 77.7081,
        "address": "Shastri Nagar, Meerut",
        "city": "Meerut",
        "state": "Uttar Pradesh",
        "pincode": "250004",
        "opening_hours": "10:00 AM - 9:00 PM",
        "store_size_sqft": 16000,
    },
    {
        "store_id": "MX_MRT_001",
        "store_name": "Max Fashion Meerut Mall 66",
        "chain": StoreChain.MAX_FASHION,
        "latitude": 28.9926,
        "longitude": 77.7131,
        "address": "Mall 66, Meerut",
        "city": "Meerut",
        "state": "Uttar Pradesh",
        "pincode": "250002",
        "opening_hours": "11:00 AM - 10:00 PM",
        "store_size_sqft": 18000,
    },
    # Agra Competitors
    {
        "store_id": "PT_AGR_001",
        "store_name": "Pantaloons Agra Pacific Mall",
        "chain": StoreChain.PANTALOONS,
        "latitude": 27.1716,
        "longitude": 78.0169,
        "address": "Pacific Mall, Fatehabad Road",
        "city": "Agra",
        "state": "Uttar Pradesh",
        "pincode": "282001",
        "opening_hours": "10:00 AM - 10:00 PM",
        "store_size_sqft": 24000,
    },
    {
        "store_id": "RT_AGR_001",
        "store_name": "Reliance Trends Agra Sanjay Place",
        "chain": StoreChain.RELIANCE_TRENDS,
        "latitude": 27.1803,
        "longitude": 78.0082,
        "address": "Sanjay Place, Agra",
        "city": "Agra",
        "state": "Uttar Pradesh",
        "pincode": "282002",
        "opening_hours": "10:00 AM - 10:00 PM",
        "store_size_sqft": 22000,
    },
    # Prayagraj Competitors
    {
        "store_id": "ZD_ALB_001",
        "store_name": "Zudio Prayagraj Civil Lines",
        "chain": StoreChain.ZUDIO,
        "latitude": 25.4403,
        "longitude": 81.8431,
        "address": "Civil Lines, Prayagraj",
        "city": "Prayagraj",
        "state": "Uttar Pradesh",
        "pincode": "211001",
        "opening_hours": "10:00 AM - 9:30 PM",
        "store_size_sqft": 16000,
    },
    # Patna Competitors
    {
        "store_id": "PT_PAT_001",
        "store_name": "Pantaloons Patna P&M Mall",
        "chain": StoreChain.PANTALOONS,
        "latitude": 25.5941,
        "longitude": 85.1376,
        "address": "P&M Mall, Exhibition Road",
        "city": "Patna",
        "state": "Bihar",
        "pincode": "800001",
        "opening_hours": "10:00 AM - 10:00 PM",
        "store_size_sqft": 23000,
    },
    {
        "store_id": "WS_PAT_001",
        "store_name": "Westside Patna Boring Road",
        "chain": StoreChain.WESTSIDE,
        "latitude": 25.6149,
        "longitude": 85.1461,
        "address": "Patna Central Mall, Boring Road",
        "city": "Patna",
        "state": "Bihar",
        "pincode": "800013",
        "opening_hours": "11:00 AM - 10:00 PM",
        "store_size_sqft": 26000,
    },
    # Muzaffarpur Competitors
    {
        "store_id": "SB_MUZ_001",
        "store_name": "Style Bazar Muzaffarpur Station Road",
        "chain": StoreChain.STYLE_BAZAR,
        "latitude": 26.1197,
        "longitude": 85.3910,
        "address": "Station Road, Muzaffarpur",
        "city": "Muzaffarpur",
        "state": "Bihar",
        "pincode": "842001",
        "opening_hours": "10:00 AM - 9:00 PM",
        "store_size_sqft": 12000,
    },
    # Indore Competitors
    {
        "store_id": "PT_IND_001",
        "store_name": "Pantaloons Indore Treasure Island",
        "chain": StoreChain.PANTALOONS,
        "latitude": 22.7242,
        "longitude": 75.8654,
        "address": "Treasure Island Mall, MG Road",
        "city": "Indore",
        "state": "Madhya Pradesh",
        "pincode": "452001",
        "opening_hours": "10:00 AM - 10:00 PM",
        "store_size_sqft": 27000,
    },
    {
        "store_id": "RT_IND_001",
        "store_name": "Reliance Trends Indore Vijay Nagar",
        "chain": StoreChain.RELIANCE_TRENDS,
        "latitude": 22.7532,
        "longitude": 75.8937,
        "address": "Vijay Nagar, Indore",
        "city": "Indore",
        "state": "Madhya Pradesh",
        "pincode": "452010",
        "opening_hours": "10:00 AM - 10:00 PM",
        "store_size_sqft": 29000,
    },
    # Bhopal Competitors
    {
        "store_id": "ZD_BPL_001",
        "store_name": "Zudio Bhopal DB City Mall",
        "chain": StoreChain.ZUDIO,
        "latitude": 23.2451,
        "longitude": 77.4234,
        "address": "DB City Mall, Arera Colony",
        "city": "Bhopal",
        "state": "Madhya Pradesh",
        "pincode": "462016",
        "opening_hours": "10:00 AM - 10:00 PM",
        "store_size_sqft": 22000,
    },
    {
        "store_id": "WS_BPL_001",
        "store_name": "Westside Bhopal MP Nagar",
        "chain": StoreChain.WESTSIDE,
        "latitude": 23.2379,
        "longitude": 77.4179,
        "address": "MP Nagar Zone 1, Bhopal",
        "city": "Bhopal",
        "state": "Madhya Pradesh",
        "pincode": "462011",
        "opening_hours": "11:00 AM - 10:00 PM",
        "store_size_sqft": 25000,
    },
    # Jaipur Competitors
    {
        "store_id": "PT_JPR_001",
        "store_name": "Pantaloons Jaipur GT Mall",
        "chain": StoreChain.PANTALOONS,
        "latitude": 26.9172,
        "longitude": 75.7890,
        "address": "GT Central Mall, MI Road",
        "city": "Jaipur",
        "state": "Rajasthan",
        "pincode": "302001",
        "opening_hours": "10:00 AM - 10:00 PM",
        "store_size_sqft": 28000,
    },
    {
        "store_id": "RT_JPR_001",
        "store_name": "Reliance Trends Jaipur Malviya Nagar",
        "chain": StoreChain.RELIANCE_TRENDS,
        "latitude": 26.8511,
        "longitude": 75.8147,
        "address": "Malviya Nagar, Jaipur",
        "city": "Jaipur",
        "state": "Rajasthan",
        "pincode": "302017",
        "opening_hours": "10:00 AM - 10:00 PM",
        "store_size_sqft": 30000,
    },
    {
        "store_id": "WS_JPR_001",
        "store_name": "Westside Jaipur World Trade Park",
        "chain": StoreChain.WESTSIDE,
        "latitude": 26.8515,
        "longitude": 75.8046,
        "address": "World Trade Park, JLN Marg",
        "city": "Jaipur",
        "state": "Rajasthan",
        "pincode": "302018",
        "opening_hours": "11:00 AM - 10:00 PM",
        "store_size_sqft": 32000,
    },
]


def create_vmart_store(data: dict) -> Store:
    """Create V-Mart Store object from dict"""
    location = GeoLocation(
        latitude=data["latitude"],
        longitude=data["longitude"],
        address=data["address"],
        city=data["city"],
        state=data["state"],
        pincode=data["pincode"],
    )

    return Store(
        store_id=data["store_id"],
        store_name=data["store_name"],
        chain=StoreChain.VMART,
        location=location,
        phone=data.get("phone"),
        opening_hours=data.get("opening_hours"),
        store_size_sqft=data.get("store_size_sqft"),
        is_active=True,
        opened_date=datetime.now(),
    )


def create_competitor_store(data: dict) -> Store:
    """Create competitor Store object from dict"""
    location = GeoLocation(
        latitude=data["latitude"],
        longitude=data["longitude"],
        address=data["address"],
        city=data["city"],
        state=data["state"],
        pincode=data["pincode"],
    )

    return Store(
        store_id=data["store_id"],
        store_name=data["store_name"],
        chain=data["chain"],
        location=location,
        phone=data.get("phone"),
        opening_hours=data.get("opening_hours"),
        store_size_sqft=data.get("store_size_sqft"),
        is_active=True,
        opened_date=datetime.now(),
    )


def initialize_stores(database):
    """Initialize database with store data"""
    print("Initializing V-Mart stores...")
    vmart_count = 0
    for store_data in VMART_STORES_DATA:
        store = create_vmart_store(store_data)
        if database.add_vmart_store(store):
            vmart_count += 1
            print(f"  ✓ Added {store.store_name}")

    print(f"\nInitializing competitor stores...")
    competitor_count = 0
    for store_data in COMPETITOR_STORES_DATA:
        store = create_competitor_store(store_data)
        if database.add_competitor_store(store):
            competitor_count += 1
            print(f"  ✓ Added {store.store_name} ({store.chain.value})")

    print(f"\n✅ Initialization complete:")
    print(f"   V-Mart stores: {vmart_count}")
    print(f"   Competitor stores: {competitor_count}")
    print(f"   Total stores: {vmart_count + competitor_count}")

    return vmart_count, competitor_count
