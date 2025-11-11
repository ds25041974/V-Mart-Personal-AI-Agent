"""
Database Manager for Store Locations
Handles CRUD operations for V-Mart stores, competitors, and weather data
"""

import json
import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .models import (
    DATABASE_SCHEMA,
    CompetitorAnalysis,
    GeoLocation,
    Store,
    StoreChain,
    WeatherData,
    WeatherPeriod,
)


class StoreDatabase:
    """SQLite database manager for store data"""

    def __init__(self, db_path: str = "data/stores.db"):
        """Initialize database connection"""
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.initialize_database()

    def initialize_database(self):
        """Create tables if they don't exist"""
        cursor = self.conn.cursor()
        cursor.executescript(DATABASE_SCHEMA)
        self.conn.commit()

    # V-Mart Store Operations

    def add_vmart_store(self, store: Store) -> bool:
        """Add a V-Mart store to the database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO vmart_stores (
                    store_id, store_name, latitude, longitude,
                    address, city, state, pincode, phone, email,
                    manager_name, opening_hours, store_size_sqft,
                    is_active, opened_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    store.store_id,
                    store.store_name,
                    store.location.latitude,
                    store.location.longitude,
                    store.location.address,
                    store.location.city,
                    store.location.state,
                    store.location.pincode,
                    store.phone,
                    store.email,
                    store.manager_name,
                    store.opening_hours,
                    store.store_size_sqft,
                    store.is_active,
                    store.opened_date,
                    store.last_updated,
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_vmart_store(self, store_id: str) -> Optional[Store]:
        """Get a V-Mart store by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vmart_stores WHERE store_id = ?", (store_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_store(row, StoreChain.VMART)
        return None

    def get_all_vmart_stores(self, active_only: bool = True) -> List[Store]:
        """Get all V-Mart stores"""
        cursor = self.conn.cursor()
        query = "SELECT * FROM vmart_stores"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY city, store_name"

        cursor.execute(query)
        return [self._row_to_store(row, StoreChain.VMART) for row in cursor.fetchall()]

    def get_vmart_stores_by_city(self, city: str) -> List[Store]:
        """Get V-Mart stores in a specific city"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM vmart_stores WHERE city = ? AND is_active = 1", (city,)
        )
        return [self._row_to_store(row, StoreChain.VMART) for row in cursor.fetchall()]

    def get_vmart_stores_by_state(self, state: str) -> List[Store]:
        """Get V-Mart stores in a specific state"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM vmart_stores WHERE state = ? AND is_active = 1", (state,)
        )
        return [self._row_to_store(row, StoreChain.VMART) for row in cursor.fetchall()]

    # Competitor Store Operations

    def add_competitor_store(self, store: Store) -> bool:
        """Add a competitor store to the database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO competitor_stores (
                    store_id, store_name, chain, latitude, longitude,
                    address, city, state, pincode, phone, email,
                    opening_hours, store_size_sqft, is_active,
                    opened_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    store.store_id,
                    store.store_name,
                    store.chain.value,
                    store.location.latitude,
                    store.location.longitude,
                    store.location.address,
                    store.location.city,
                    store.location.state,
                    store.location.pincode,
                    store.phone,
                    store.email,
                    store.opening_hours,
                    store.store_size_sqft,
                    store.is_active,
                    store.opened_date,
                    store.last_updated,
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_competitor_stores(self, chain: Optional[StoreChain] = None) -> List[Store]:
        """Get competitor stores, optionally filtered by chain"""
        cursor = self.conn.cursor()
        if chain:
            cursor.execute(
                "SELECT * FROM competitor_stores WHERE chain = ? AND is_active = 1",
                (chain.value,),
            )
        else:
            cursor.execute("SELECT * FROM competitor_stores WHERE is_active = 1")

        return [self._row_to_competitor_store(row) for row in cursor.fetchall()]

    def get_competitor_stores_by_city(self, city: str) -> List[Store]:
        """Get competitor stores in a specific city"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM competitor_stores WHERE city = ? AND is_active = 1", (city,)
        )
        return [self._row_to_competitor_store(row) for row in cursor.fetchall()]

    # Weather Data Operations

    def add_weather_data(self, weather: WeatherData) -> bool:
        """Add weather data to the database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO weather_data (
                    latitude, longitude, city, state, weather_date,
                    period, temperature_celsius, feels_like_celsius,
                    humidity, weather_condition, weather_description,
                    wind_speed, visibility, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    weather.location.latitude,
                    weather.location.longitude,
                    weather.location.city,
                    weather.location.state,
                    weather.date.date(),
                    weather.period.value,
                    weather.temperature_celsius,
                    weather.feels_like_celsius,
                    weather.humidity,
                    weather.weather_condition,
                    weather.weather_description,
                    weather.wind_speed,
                    weather.visibility,
                    weather.last_updated,
                ),
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding weather data: {e}")
            return False

    def get_weather_data(
        self,
        latitude: float,
        longitude: float,
        target_date: date,
        period: Optional[WeatherPeriod] = None,
    ) -> List[WeatherData]:
        """Get weather data for a location and date"""
        cursor = self.conn.cursor()

        if period:
            cursor.execute(
                """
                SELECT * FROM weather_data 
                WHERE latitude = ? AND longitude = ? 
                AND weather_date = ? AND period = ?
                ORDER BY last_updated DESC LIMIT 1
            """,
                (latitude, longitude, target_date, period.value),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM weather_data 
                WHERE latitude = ? AND longitude = ? 
                AND weather_date = ?
                ORDER BY period
            """,
                (latitude, longitude, target_date),
            )

        return [self._row_to_weather(row) for row in cursor.fetchall()]

    # Proximity Analysis Operations

    def save_proximity_analysis(self, analysis: CompetitorAnalysis) -> bool:
        """Save competitor proximity analysis"""
        try:
            cursor = self.conn.cursor()
            # Delete old analysis for this store
            cursor.execute(
                "DELETE FROM competitor_proximity WHERE vmart_store_id = ?",
                (analysis.vmart_store.store_id,),
            )

            # Insert new analysis
            for competitor in analysis.nearby_competitors:
                distance = analysis.vmart_store.location.distance_to(
                    competitor.location
                )
                cursor.execute(
                    """
                    INSERT INTO competitor_proximity (
                        vmart_store_id, competitor_store_id, distance_km, analysis_date
                    ) VALUES (?, ?, ?, ?)
                """,
                    (
                        analysis.vmart_store.store_id,
                        competitor.store_id,
                        distance,
                        analysis.analysis_date,
                    ),
                )

            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving proximity analysis: {e}")
            return False

    def get_proximity_analysis(
        self, vmart_store_id: str
    ) -> Optional[CompetitorAnalysis]:
        """Get proximity analysis for a V-Mart store"""
        vmart_store = self.get_vmart_store(vmart_store_id)
        if not vmart_store:
            return None

        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT cs.*, cp.distance_km
            FROM competitor_proximity cp
            JOIN competitor_stores cs ON cp.competitor_store_id = cs.store_id
            WHERE cp.vmart_store_id = ?
            ORDER BY cp.distance_km
        """,
            (vmart_store_id,),
        )

        competitors = []
        for row in cursor.fetchall():
            store = self._row_to_competitor_store(row)
            competitors.append(store)

        return CompetitorAnalysis(
            vmart_store=vmart_store,
            nearby_competitors=competitors,
            analysis_date=datetime.now(),
        )

    # Helper Methods

    def _row_to_store(self, row: sqlite3.Row, chain: StoreChain) -> Store:
        """Convert database row to Store object"""
        location = GeoLocation(
            latitude=row["latitude"],
            longitude=row["longitude"],
            address=row["address"],
            city=row["city"],
            state=row["state"],
            pincode=row["pincode"],
        )

        # Safely get optional fields
        manager_name = (
            row["manager_name"]
            if "manager_name" in row.keys() and row["manager_name"]
            else None
        )

        return Store(
            store_id=row["store_id"],
            store_name=row["store_name"],
            chain=chain,
            location=location,
            phone=row["phone"],
            email=row["email"],
            manager_name=manager_name,
            opening_hours=row["opening_hours"],
            store_size_sqft=row["store_size_sqft"],
            is_active=bool(row["is_active"]),
            opened_date=datetime.fromisoformat(row["opened_date"])
            if row["opened_date"]
            else None,
            last_updated=datetime.fromisoformat(row["last_updated"])
            if row["last_updated"]
            else datetime.now(),
        )

    def _row_to_competitor_store(self, row: sqlite3.Row) -> Store:
        """Convert competitor row to Store object"""
        location = GeoLocation(
            latitude=row["latitude"],
            longitude=row["longitude"],
            address=row["address"],
            city=row["city"],
            state=row["state"],
            pincode=row["pincode"],
        )

        # Safely get optional fields
        email = row["email"] if "email" in row.keys() and row["email"] else None
        phone = row["phone"] if "phone" in row.keys() and row["phone"] else None
        manager_name = (
            row["manager_name"]
            if "manager_name" in row.keys() and row["manager_name"]
            else None
        )

        return Store(
            store_id=row["store_id"],
            store_name=row["store_name"],
            chain=StoreChain(row["chain"]),
            location=location,
            phone=phone,
            email=email,
            manager_name=manager_name,
            opening_hours=row["opening_hours"],
            store_size_sqft=row["store_size_sqft"],
            is_active=bool(row["is_active"]),
            opened_date=datetime.fromisoformat(row["opened_date"])
            if row["opened_date"]
            else None,
            last_updated=datetime.fromisoformat(row["last_updated"])
            if row["last_updated"]
            else datetime.now(),
        )

    def _row_to_weather(self, row: sqlite3.Row) -> WeatherData:
        """Convert database row to WeatherData object"""
        location = GeoLocation(
            latitude=row["latitude"],
            longitude=row["longitude"],
            address="",
            city=row["city"],
            state=row["state"],
            pincode="",
        )

        return WeatherData(
            location=location,
            date=datetime.fromisoformat(row["weather_date"]),
            period=WeatherPeriod(row["period"]),
            temperature_celsius=row["temperature_celsius"],
            feels_like_celsius=row["feels_like_celsius"],
            humidity=row["humidity"],
            weather_condition=row["weather_condition"],
            weather_description=row["weather_description"],
            wind_speed=row["wind_speed"],
            visibility=row["visibility"],
            last_updated=datetime.fromisoformat(row["last_updated"])
            if row["last_updated"]
            else datetime.now(),
        )

    # Additional helper methods for bulk operations

    def add_store(self, store: Store) -> bool:
        """
        Add a store to the database (alias for add_vmart_store)
        Automatically detects if it's a V-Mart or competitor store
        """
        if store.chain == StoreChain.VMART:
            return self.add_vmart_store(store)
        else:
            return self.add_competitor_store(store)

    def get_store_count(self, active_only: bool = True) -> int:
        """Get total count of V-Mart stores"""
        cursor = self.conn.cursor()
        if active_only:
            cursor.execute("SELECT COUNT(*) FROM vmart_stores WHERE is_active = 1")
        else:
            cursor.execute("SELECT COUNT(*) FROM vmart_stores")
        return cursor.fetchone()[0]

    def get_competitor_count(
        self, chain: Optional[StoreChain] = None, active_only: bool = True
    ) -> int:
        """Get total count of competitor stores"""
        cursor = self.conn.cursor()
        if chain:
            if active_only:
                cursor.execute(
                    "SELECT COUNT(*) FROM competitor_stores WHERE chain = ? AND is_active = 1",
                    (chain.value,),
                )
            else:
                cursor.execute(
                    "SELECT COUNT(*) FROM competitor_stores WHERE chain = ?",
                    (chain.value,),
                )
        else:
            if active_only:
                cursor.execute(
                    "SELECT COUNT(*) FROM competitor_stores WHERE is_active = 1"
                )
            else:
                cursor.execute("SELECT COUNT(*) FROM competitor_stores")
        return cursor.fetchone()[0]

    def get_all_stores(self, active_only: bool = True) -> List[Store]:
        """Get all V-Mart stores (alias for get_all_vmart_stores)"""
        return self.get_all_vmart_stores(active_only)

    def get_store(self, store_id: str) -> Optional[Store]:
        """Get a store by ID (checks both V-Mart and competitor tables)"""
        # Try V-Mart first
        store = self.get_vmart_store(store_id)
        if store:
            return store

        # Try competitor stores
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM competitor_stores WHERE store_id = ?", (store_id,)
        )
        row = cursor.fetchone()
        if row:
            return self._row_to_competitor_store(row)

        return None

    def get_competitors_within_radius(
        self, store_id: str, radius_km: float = 5.0
    ) -> List[Tuple[Store, float]]:
        """
        Get competitor stores within specified radius of a V-Mart store
        Returns list of (competitor_store, distance_km) tuples
        """
        vmart_store = self.get_vmart_store(store_id)
        if not vmart_store:
            return []

        all_competitors = self.get_competitor_stores()
        nearby = []

        for competitor in all_competitors:
            distance = vmart_store.location.distance_to(competitor.location)
            if distance <= radius_km:
                nearby.append((competitor, distance))

        # Sort by distance
        nearby.sort(key=lambda x: x[1])
        return nearby

    def close(self):
        """Close database connection"""
        self.conn.close()
