"""
Store Location Models and Database Schema
Handles V-Mart stores, competitor stores, geo-coordinates, and weather data
"""

import math
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class StoreChain(Enum):
    """Store chain types"""

    VMART = "V-Mart"
    V2_RETAIL = "V2 Retail"
    ZUDIO = "Zudio"
    STYLE_BAZAR = "Style Bazar"
    MAX_FASHION = "Max Fashion"
    RELIANCE_TRENDS = "Reliance Trends"
    PANTALOONS = "Pantaloons"
    SHOPPERS_STOP = "Shoppers Stop"
    LIFESTYLE = "Lifestyle"
    WESTSIDE = "Westside"
    OTHER = "Other"


class WeatherPeriod(Enum):
    """Time periods for weather data"""

    MORNING = "Morning"  # 6 AM - 12 PM
    AFTERNOON = "Afternoon"  # 12 PM - 6 PM
    EVENING = "Evening"  # 6 PM - 10 PM
    NIGHT = "Night"  # 10 PM - 6 AM


@dataclass
class GeoLocation:
    """Geographic coordinates with validation"""

    latitude: float
    longitude: float
    address: str
    city: str
    state: str
    pincode: str

    def __post_init__(self):
        """Validate coordinates"""
        if not (-90 <= self.latitude <= 90):
            raise ValueError(f"Invalid latitude: {self.latitude}")
        if not (-180 <= self.longitude <= 180):
            raise ValueError(f"Invalid longitude: {self.longitude}")

    def distance_to(self, other: "GeoLocation") -> float:
        """
        Calculate distance to another location using Haversine formula
        Returns distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers

        lat1_rad = math.radians(self.latitude)
        lat2_rad = math.radians(other.latitude)
        delta_lat = math.radians(other.latitude - self.latitude)
        delta_lon = math.radians(other.longitude - self.longitude)

        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "pincode": self.pincode,
        }


@dataclass
class WeatherData:
    """Weather information for a specific time period"""

    location: GeoLocation
    date: datetime
    period: WeatherPeriod
    temperature_celsius: float
    feels_like_celsius: float
    humidity: int  # percentage
    weather_condition: str  # e.g., "Clear", "Cloudy", "Rainy"
    weather_description: str
    wind_speed: float  # km/h
    visibility: float  # km
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "location": self.location.to_dict(),
            "date": self.date.isoformat(),
            "period": self.period.value,
            "temperature_celsius": self.temperature_celsius,
            "feels_like_celsius": self.feels_like_celsius,
            "humidity": self.humidity,
            "weather_condition": self.weather_condition,
            "weather_description": self.weather_description,
            "wind_speed": self.wind_speed,
            "visibility": self.visibility,
            "last_updated": self.last_updated.isoformat(),
        }


@dataclass
class Store:
    """Base store information"""

    store_id: str
    store_name: str
    chain: StoreChain
    location: GeoLocation
    phone: Optional[str] = None
    email: Optional[str] = None
    manager_name: Optional[str] = None
    opening_hours: Optional[str] = None
    store_size_sqft: Optional[int] = None
    is_active: bool = True
    opened_date: Optional[datetime] = None
    last_updated: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(
        cls,
        store_id: str,
        name: str,
        address: str,
        city: str,
        state: str,
        pincode: str,
        latitude: float,
        longitude: float,
        chain: StoreChain = StoreChain.VMART,
        phone: Optional[str] = None,
        manager_name: Optional[str] = None,
        manager_email: Optional[str] = None,
        **kwargs,
    ) -> "Store":
        """
        Factory method to create a Store from simplified parameters
        Used by bulk import tools for easier construction
        """
        location = GeoLocation(
            latitude=latitude,
            longitude=longitude,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
        )

        return cls(
            store_id=store_id,
            store_name=name,
            chain=chain,
            location=location,
            phone=phone,
            email=manager_email,
            manager_name=manager_name,
            **kwargs,
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "store_id": self.store_id,
            "store_name": self.store_name,
            "chain": self.chain.value,
            "location": self.location.to_dict(),
            "phone": self.phone,
            "email": self.email,
            "manager_name": self.manager_name,
            "opening_hours": self.opening_hours,
            "store_size_sqft": self.store_size_sqft,
            "is_active": self.is_active,
            "opened_date": self.opened_date.isoformat() if self.opened_date else None,
            "last_updated": self.last_updated.isoformat(),
        }


@dataclass
class CompetitorAnalysis:
    """Analysis of competitors near a V-Mart store"""

    vmart_store: Store
    nearby_competitors: List[Store]
    analysis_date: datetime = field(default_factory=datetime.now)
    search_radius_km: float = 5.0  # Default 5km radius

    def get_competitors_by_chain(self) -> Dict[str, List[Store]]:
        """Group competitors by chain"""
        by_chain = {}
        for competitor in self.nearby_competitors:
            chain_name = competitor.chain.value
            if chain_name not in by_chain:
                by_chain[chain_name] = []
            by_chain[chain_name].append(competitor)
        return by_chain

    def get_competitor_count(self) -> int:
        """Total number of nearby competitors"""
        return len(self.nearby_competitors)

    def get_closest_competitor(self) -> Optional[Store]:
        """Get the closest competitor"""
        if not self.nearby_competitors:
            return None

        closest = min(
            self.nearby_competitors,
            key=lambda c: self.vmart_store.location.distance_to(c.location),
        )
        return closest

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        by_chain = self.get_competitors_by_chain()
        closest = self.get_closest_competitor()

        return {
            "vmart_store": self.vmart_store.to_dict(),
            "total_competitors": self.get_competitor_count(),
            "search_radius_km": self.search_radius_km,
            "competitors_by_chain": {
                chain: [store.to_dict() for store in stores]
                for chain, stores in by_chain.items()
            },
            "closest_competitor": closest.to_dict() if closest else None,
            "analysis_date": self.analysis_date.isoformat(),
        }


# Database schema definitions for SQLite/PostgreSQL
DATABASE_SCHEMA = """
-- V-Mart Stores Table
CREATE TABLE IF NOT EXISTS vmart_stores (
    store_id VARCHAR(50) PRIMARY KEY,
    store_name VARCHAR(200) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    manager_name VARCHAR(100),
    opening_hours VARCHAR(100),
    store_size_sqft INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    opened_date TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_latitude CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT valid_longitude CHECK (longitude BETWEEN -180 AND 180)
);

-- Competitor Stores Table
CREATE TABLE IF NOT EXISTS competitor_stores (
    store_id VARCHAR(50) PRIMARY KEY,
    store_name VARCHAR(200) NOT NULL,
    chain VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    opening_hours VARCHAR(100),
    store_size_sqft INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    opened_date TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_latitude CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT valid_longitude CHECK (longitude BETWEEN -180 AND 180)
);

-- Weather Data Table
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    weather_date DATE NOT NULL,
    period VARCHAR(20) NOT NULL,
    temperature_celsius DECIMAL(5, 2) NOT NULL,
    feels_like_celsius DECIMAL(5, 2) NOT NULL,
    humidity INTEGER NOT NULL,
    weather_condition VARCHAR(50) NOT NULL,
    weather_description TEXT,
    wind_speed DECIMAL(5, 2),
    visibility DECIMAL(5, 2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_period CHECK (period IN ('Morning', 'Afternoon', 'Evening', 'Night')),
    CONSTRAINT valid_humidity CHECK (humidity BETWEEN 0 AND 100)
);

-- Competitor Proximity Analysis Table
CREATE TABLE IF NOT EXISTS competitor_proximity (
    id SERIAL PRIMARY KEY,
    vmart_store_id VARCHAR(50) NOT NULL,
    competitor_store_id VARCHAR(50) NOT NULL,
    distance_km DECIMAL(10, 2) NOT NULL,
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vmart_store_id) REFERENCES vmart_stores(store_id),
    FOREIGN KEY (competitor_store_id) REFERENCES competitor_stores(store_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_vmart_city ON vmart_stores(city);
CREATE INDEX IF NOT EXISTS idx_vmart_state ON vmart_stores(state);
CREATE INDEX IF NOT EXISTS idx_vmart_active ON vmart_stores(is_active);
CREATE INDEX IF NOT EXISTS idx_vmart_location ON vmart_stores(latitude, longitude);

CREATE INDEX IF NOT EXISTS idx_competitor_chain ON competitor_stores(chain);
CREATE INDEX IF NOT EXISTS idx_competitor_city ON competitor_stores(city);
CREATE INDEX IF NOT EXISTS idx_competitor_state ON competitor_stores(state);
CREATE INDEX IF NOT EXISTS idx_competitor_active ON competitor_stores(is_active);
CREATE INDEX IF NOT EXISTS idx_competitor_location ON competitor_stores(latitude, longitude);

CREATE INDEX IF NOT EXISTS idx_weather_location ON weather_data(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_weather_date ON weather_data(weather_date);
CREATE INDEX IF NOT EXISTS idx_weather_period ON weather_data(period);

CREATE INDEX IF NOT EXISTS idx_proximity_vmart ON competitor_proximity(vmart_store_id);
CREATE INDEX IF NOT EXISTS idx_proximity_competitor ON competitor_proximity(competitor_store_id);
CREATE INDEX IF NOT EXISTS idx_proximity_distance ON competitor_proximity(distance_km);
"""
