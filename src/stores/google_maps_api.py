"""
Google Maps API Integration for Store Location Data
Fetches real geo-locations for V-Mart and competitor stores
"""

import logging
import os
import time
from typing import Dict, List, Optional

try:
    import googlemaps
    from googlemaps.exceptions import ApiError

    GOOGLE_MAPS_AVAILABLE = True
except ImportError:
    GOOGLE_MAPS_AVAILABLE = False
    print("⚠ Google Maps not available. Install: pip install googlemaps")

logger = logging.getLogger(__name__)


class GoogleMapsService:
    """
    Service for fetching store locations using Google Maps Geocoding API
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Google Maps service

        Args:
            api_key: Google Maps API key (or from environment)
        """
        self.api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
        self.client = None

        if GOOGLE_MAPS_AVAILABLE and self.api_key:
            try:
                self.client = googlemaps.Client(key=self.api_key)
                logger.info("✓ Google Maps API initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Google Maps: {e}")
        else:
            logger.warning("Google Maps API not configured")

    def geocode_address(
        self, address: str, retry_count: int = 3
    ) -> Optional[Dict[str, float]]:
        """
        Convert address to latitude/longitude coordinates

        Args:
            address: Full address string
            retry_count: Number of retries on failure

        Returns:
            Dict with 'latitude' and 'longitude' or None
        """
        if not self.client:
            logger.warning("Google Maps client not initialized")
            return None

        for attempt in range(retry_count):
            try:
                # Geocode the address
                result = self.client.geocode(address)

                if result and len(result) > 0:
                    location = result[0]["geometry"]["location"]
                    return {
                        "latitude": location["lat"],
                        "longitude": location["lng"],
                        "formatted_address": result[0]["formatted_address"],
                        "place_id": result[0].get("place_id"),
                    }
                else:
                    logger.warning(f"No results for address: {address}")
                    return None

            except ApiError as e:
                logger.error(f"Google Maps API error (attempt {attempt + 1}): {e}")
                if attempt < retry_count - 1:
                    time.sleep(2**attempt)  # Exponential backoff
                else:
                    return None

            except Exception as e:
                logger.error(f"Geocoding error: {e}")
                return None

        return None

    def find_stores_nearby(
        self,
        latitude: float,
        longitude: float,
        store_name: str,
        radius: int = 5000,
    ) -> List[Dict]:
        """
        Find stores of a specific brand near a location

        Args:
            latitude: Center latitude
            longitude: Center longitude
            store_name: Store brand name (e.g., "V2 Retail", "Zudio")
            radius: Search radius in meters (default 5km)

        Returns:
            List of nearby stores with details
        """
        if not self.client:
            return []

        try:
            # Use Places API to search for stores
            results = self.client.places_nearby(
                location=(latitude, longitude),
                radius=radius,
                keyword=store_name,
                type="clothing_store",
            )

            stores = []
            for place in results.get("results", []):
                store_info = {
                    "name": place.get("name"),
                    "latitude": place["geometry"]["location"]["lat"],
                    "longitude": place["geometry"]["location"]["lng"],
                    "address": place.get("vicinity"),
                    "place_id": place.get("place_id"),
                    "rating": place.get("rating"),
                    "user_ratings_total": place.get("user_ratings_total"),
                }
                stores.append(store_info)

            logger.info(f"Found {len(stores)} {store_name} stores nearby")
            return stores

        except Exception as e:
            logger.error(f"Error finding nearby stores: {e}")
            return []

    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """
        Get detailed information about a place

        Args:
            place_id: Google Maps Place ID

        Returns:
            Detailed place information
        """
        if not self.client:
            return None

        try:
            result = self.client.place(
                place_id=place_id,
                fields=[
                    "name",
                    "formatted_address",
                    "geometry",
                    "formatted_phone_number",
                    "opening_hours",
                    "rating",
                    "website",
                ],
            )

            if result.get("status") == "OK":
                place = result["result"]
                location = place["geometry"]["location"]

                return {
                    "name": place.get("name"),
                    "address": place.get("formatted_address"),
                    "latitude": location["lat"],
                    "longitude": location["lng"],
                    "phone": place.get("formatted_phone_number"),
                    "website": place.get("website"),
                    "rating": place.get("rating"),
                    "opening_hours": place.get("opening_hours"),
                }

        except Exception as e:
            logger.error(f"Error getting place details: {e}")
            return None

    def batch_geocode(
        self, addresses: List[str], delay: float = 0.2
    ) -> List[Optional[Dict]]:
        """
        Geocode multiple addresses with rate limiting

        Args:
            addresses: List of address strings
            delay: Delay between requests (seconds)

        Returns:
            List of geocoded results (same order as input)
        """
        results = []

        for idx, address in enumerate(addresses):
            logger.info(f"Geocoding {idx + 1}/{len(addresses)}: {address}")
            result = self.geocode_address(address)
            results.append(result)

            # Rate limiting
            if idx < len(addresses) - 1:
                time.sleep(delay)

        return results

    def validate_coordinates(self, latitude: float, longitude: float) -> bool:
        """
        Validate if coordinates are within India's bounds

        Args:
            latitude: Latitude value
            longitude: Longitude value

        Returns:
            True if valid coordinates in India
        """
        # India's approximate bounds
        # Latitude: 8.4° N to 37.6° N
        # Longitude: 68.7° E to 97.25° E

        if 8.4 <= latitude <= 37.6 and 68.7 <= longitude <= 97.25:
            return True

        logger.warning(f"Invalid coordinates for India: {latitude}, {longitude}")
        return False


class StoreDataCollector:
    """
    Collects and validates store data from various sources
    """

    def __init__(self, maps_service: GoogleMapsService):
        self.maps_service = maps_service

    def import_from_csv(self, csv_path: str) -> List[Dict]:
        """
        Import store data from CSV file

        Expected CSV columns:
        - store_name
        - address
        - city
        - state
        - pincode
        - phone (optional)

        Returns:
            List of store records with geocoded coordinates
        """
        import csv

        stores = []

        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
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

                    if geo_data:
                        store_record = {
                            "name": row.get("store_name"),
                            "address": row.get("address"),
                            "city": row.get("city"),
                            "state": row.get("state"),
                            "pincode": row.get("pincode"),
                            "phone": row.get("phone"),
                            "latitude": geo_data["latitude"],
                            "longitude": geo_data["longitude"],
                            "formatted_address": geo_data["formatted_address"],
                        }
                        stores.append(store_record)
                        logger.info(
                            f"✓ Imported: {store_record['name']} - {store_record['city']}"
                        )
                    else:
                        logger.warning(f"⚠ Failed to geocode: {full_address}")

                    # Rate limiting
                    time.sleep(0.2)

            logger.info(f"✓ Imported {len(stores)} stores from CSV")
            return stores

        except Exception as e:
            logger.error(f"Error importing CSV: {e}")
            return []

    def scrape_vmart_stores(self) -> List[Dict]:
        """
        Scrape V-Mart store locations from official website

        Note: This is a placeholder. Actual implementation would use
        BeautifulSoup or Selenium to scrape from vmart.co.in

        Returns:
            List of V-Mart store records
        """
        logger.info("Store scraping would be implemented here")
        logger.info("Source: https://www.vmart.co.in/store-locator")

        # Placeholder - would need actual scraping implementation
        return []

    def find_competitor_stores_nationwide(
        self, brand_name: str, major_cities: List[str]
    ) -> List[Dict]:
        """
        Find competitor stores across major cities

        Args:
            brand_name: Competitor brand (e.g., "Zudio", "V2", "Style Bazar")
            major_cities: List of city names to search

        Returns:
            List of competitor store records
        """
        all_stores = []

        for city in major_cities:
            logger.info(f"Searching for {brand_name} stores in {city}")

            # Geocode city center
            city_geo = self.maps_service.geocode_address(f"{city}, India")

            if city_geo:
                # Search for stores nearby
                stores = self.maps_service.find_stores_nearby(
                    latitude=city_geo["latitude"],
                    longitude=city_geo["longitude"],
                    store_name=brand_name,
                    radius=15000,  # 15km radius
                )

                for store in stores:
                    store["city"] = city
                    store["brand"] = brand_name
                    all_stores.append(store)

                # Rate limiting
                time.sleep(1)

        logger.info(f"✓ Found {len(all_stores)} {brand_name} stores")
        return all_stores


# Major Indian cities for competitor store search
MAJOR_INDIAN_CITIES = [
    # Metro cities
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Kolkata",
    "Chennai",
    "Hyderabad",
    # Tier 1 cities
    "Pune",
    "Ahmedabad",
    "Jaipur",
    "Surat",
    "Lucknow",
    "Kanpur",
    "Nagpur",
    "Indore",
    "Thane",
    "Bhopal",
    "Visakhapatnam",
    "Patna",
    "Vadodara",
    "Ghaziabad",
    "Ludhiana",
    "Agra",
    "Nashik",
    "Faridabad",
    "Meerut",
    "Rajkot",
    "Kalyan-Dombivali",
    "Vasai-Virar",
    "Varanasi",
    "Srinagar",
    "Aurangabad",
    "Dhanbad",
    "Amritsar",
    "Navi Mumbai",
    # Tier 2 cities
    "Allahabad",
    "Ranchi",
    "Howrah",
    "Coimbatore",
    "Jabalpur",
    "Gwalior",
    "Vijayawada",
    "Jodhpur",
    "Madurai",
    "Raipur",
    "Kota",
    "Chandigarh",
    "Guwahati",
    "Solapur",
    "Hubli-Dharwad",
    "Bareilly",
    "Moradabad",
    "Mysore",
    "Gurgaon",
    "Aligarh",
    "Jalandhar",
    "Tiruchirappalli",
    "Bhubaneswar",
    "Salem",
    "Warangal",
    "Mira-Bhayandar",
    "Thiruvananthapuram",
    "Bhiwandi",
    "Saharanpur",
    "Gorakhpur",
    "Guntur",
    "Bikaner",
    "Amravati",
    "Noida",
    "Jamshedpur",
    "Bhilai",
    "Cuttack",
    "Firozabad",
    "Kochi",
]


if __name__ == "__main__":
    # Example usage
    print("Google Maps Store Locator Service")
    print("=" * 50)

    # Initialize service
    maps_service = GoogleMapsService()

    if maps_service.client:
        print("✓ Google Maps API initialized")

        # Test geocoding
        test_address = "Connaught Place, New Delhi, India"
        print(f"\nTesting geocoding: {test_address}")
        result = maps_service.geocode_address(test_address)

        if result:
            print(f"✓ Latitude: {result['latitude']}")
            print(f"✓ Longitude: {result['longitude']}")
            print(f"✓ Formatted: {result['formatted_address']}")
        else:
            print("✗ Geocoding failed")
    else:
        print("✗ Google Maps API not configured")
        print("\nTo use this service:")
        print("1. Get API key from: https://console.cloud.google.com/")
        print("2. Enable: Geocoding API, Places API, Maps JavaScript API")
        print("3. Set environment variable: GOOGLE_MAPS_API_KEY")
        print("4. Install package: pip install googlemaps")
