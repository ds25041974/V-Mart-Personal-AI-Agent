"""
Context Manager for Gemini AI Agent
Manages store location, weather, and competitor data context for AI insights

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import os
from datetime import datetime
from typing import Dict, List, Optional

from src.stores import StoreAnalyzer, StoreDatabase, WeatherService


class AIContextManager:
    """Manages contextual data for AI-powered insights"""

    def __init__(self):
        """Initialize context manager with store and weather services"""
        self.db = StoreDatabase("data/stores.db")
        self.weather_service = WeatherService(os.getenv("OPENWEATHER_API_KEY"))
        self.analyzer = StoreAnalyzer(self.db)

    def get_store_context(self, store_id: str) -> Optional[Dict]:
        """
        Get comprehensive context for a specific store including:
        - Store details
        - Current weather
        - Nearby competitors
        - Competition analysis

        Args:
            store_id: Store ID (e.g., 'VM_DL_001')

        Returns:
            Dictionary with complete store context
        """
        store = self.db.get_vmart_store(store_id)
        if not store:
            return None

        # Get current weather
        weather = self.weather_service.get_current_weather(store.location)

        # Get nearby competitors
        competitors = self.db.get_competitors_within_radius(store_id, radius_km=5.0)

        # Get competition analysis
        competition_analysis = self.analyzer.analyze_vmart_competition(store_id)

        return {
            "store": {
                "id": store.store_id,
                "name": store.store_name,
                "city": store.location.city,
                "state": store.location.state,
                "address": store.location.address,
                "coordinates": {
                    "latitude": store.location.latitude,
                    "longitude": store.location.longitude,
                },
            },
            "weather": {
                "temperature": weather.temperature_celsius if weather else None,
                "feels_like": weather.feels_like_celsius if weather else None,
                "condition": weather.weather_description if weather else None,
                "humidity": weather.humidity if weather else None,
                "period": weather.period.value if weather else None,
                "last_updated": (weather.last_updated.isoformat() if weather else None),
            }
            if weather
            else None,
            "competitors": {
                "total_nearby": len(competitors),
                "breakdown": (
                    {
                        chain: len(stores)
                        for chain, stores in competition_analysis.get_competitors_by_chain().items()
                    }
                    if competition_analysis
                    else {}
                ),
                "closest": (
                    {
                        "chain": competitors[0][0].chain.value,
                        "name": competitors[0][0].store_name,
                        "distance_km": round(competitors[0][1], 2),
                    }
                    if competitors
                    else None
                ),
                "list": [
                    {
                        "chain": comp[0].chain.value,
                        "name": comp[0].store_name,
                        "distance_km": round(comp[1], 2),
                        "city": comp[0].location.city,
                    }
                    for comp in competitors[:5]  # Top 5 closest
                ],
            },
            "analysis_timestamp": datetime.now().isoformat(),
        }

    def get_city_context(self, city: str) -> Dict:
        """
        Get context for all stores in a city

        Args:
            city: City name

        Returns:
            Dictionary with city-level context
        """
        vmart_stores = self.db.get_vmart_stores_by_city(city)
        competitor_stores = self.db.get_competitor_stores_by_city(city)

        # Get weather for first V-Mart store in city
        weather = None
        if vmart_stores:
            weather = self.weather_service.get_current_weather(vmart_stores[0].location)

        return {
            "city": city,
            "vmart_stores": {
                "count": len(vmart_stores),
                "stores": [
                    {
                        "id": store.store_id,
                        "name": store.store_name,
                        "address": store.location.address,
                    }
                    for store in vmart_stores
                ],
            },
            "competitors": {
                "total": len(competitor_stores),
                "by_chain": self._count_by_chain(competitor_stores),
            },
            "weather": {
                "temperature": weather.temperature_celsius if weather else None,
                "condition": weather.weather_description if weather else None,
                "period": weather.period.value if weather else None,
            }
            if weather
            else None,
            "analysis_timestamp": datetime.now().isoformat(),
        }

    def get_weather_context(
        self, store_id: str, include_forecast: bool = False
    ) -> Dict:
        """
        Get detailed weather context for a store

        Args:
            store_id: Store ID
            include_forecast: Whether to include 5-day forecast

        Returns:
            Dictionary with weather details
        """
        store = self.db.get_vmart_store(store_id)
        if not store:
            return None

        current_weather = self.weather_service.get_current_weather(store.location)

        context = {
            "store_id": store_id,
            "location": {
                "city": store.location.city,
                "state": store.location.state,
            },
            "current": (
                {
                    "date": current_weather.date.strftime("%Y-%m-%d"),
                    "time": current_weather.date.strftime("%H:%M"),
                    "period": current_weather.period.value,
                    "temperature": current_weather.temperature_celsius,
                    "feels_like": current_weather.feels_like_celsius,
                    "humidity": current_weather.humidity,
                    "condition": current_weather.weather_condition,
                    "description": current_weather.weather_description,
                    "wind_speed": current_weather.wind_speed,
                    "visibility": current_weather.visibility,
                }
                if current_weather
                else None
            ),
        }

        if include_forecast:
            forecast = self.weather_service.get_forecast_weather(store.location, days=5)
            context["forecast"] = [
                {
                    "date": w.date.strftime("%Y-%m-%d"),
                    "period": w.period.value,
                    "temperature": w.temperature_celsius,
                    "condition": w.weather_description,
                    "humidity": w.humidity,
                }
                for w in forecast[:12]  # Next 3 days (4 periods per day)
            ]

        return context

    def format_context_for_ai(
        self, store_id: Optional[str] = None, city: Optional[str] = None
    ) -> str:
        """
        Format context data as a readable string for AI prompt

        Args:
            store_id: Optional store ID for store-specific context
            city: Optional city name for city-level context

        Returns:
            Formatted context string
        """
        if store_id:
            context = self.get_store_context(store_id)
            if not context:
                return "⚠️ Store not found"

            parts = [
                "=== CURRENT STORE CONTEXT ===",
                f"\n📍 STORE: {context['store']['name']} ({context['store']['id']})",
                f"   Location: {context['store']['city']}, {context['store']['state']}",
                f"   Address: {context['store']['address']}",
            ]

            if context["weather"]:
                w = context["weather"]
                parts.extend(
                    [
                        f"\n🌤️ WEATHER ({w['period']}):",
                        f"   Temperature: {w['temperature']}°C (Feels like {w['feels_like']}°C)",
                        f"   Condition: {w['condition']}",
                        f"   Humidity: {w['humidity']}%",
                    ]
                )

            comp = context["competitors"]
            parts.extend(
                [
                    "\n🏪 COMPETITION:",
                    f"   Total Competitors within 5km: {comp['total_nearby']}",
                ]
            )

            if comp["breakdown"]:
                parts.append("   Breakdown:")
                for chain, count in comp["breakdown"].items():
                    parts.append(f"     - {chain}: {count} stores")

            if comp["closest"]:
                c = comp["closest"]
                parts.append(
                    f"   Closest: {c['chain']} - {c['name']} ({c['distance_km']} km away)"
                )

            parts.append(f"\n⏰ Analysis Time: {context['analysis_timestamp']}")
            parts.append("=== END CONTEXT ===\n")

            return "\n".join(parts)

        elif city:
            context = self.get_city_context(city)

            parts = [
                "=== CITY CONTEXT ===",
                f"\n📍 CITY: {context['city']}",
                f"\n🏢 V-MART STORES: {context['vmart_stores']['count']}",
            ]

            for store in context["vmart_stores"]["stores"]:
                parts.append(f"   - {store['name']} ({store['id']})")

            parts.append(f"\n🏪 COMPETITORS: {context['competitors']['total']} stores")
            if context["competitors"]["by_chain"]:
                for chain, count in context["competitors"]["by_chain"].items():
                    parts.append(f"   - {chain}: {count}")

            if context["weather"]:
                w = context["weather"]
                parts.extend(
                    [
                        f"\n🌤️ WEATHER ({w['period']}):",
                        f"   Temperature: {w['temperature']}°C",
                        f"   Condition: {w['condition']}",
                    ]
                )

            parts.append("=== END CONTEXT ===\n")
            return "\n".join(parts)

        return ""

    def _count_by_chain(self, stores: List) -> Dict[str, int]:
        """Count stores by chain"""
        counts = {}
        for store in stores:
            chain = store.chain.value
            counts[chain] = counts.get(chain, 0) + 1
        return counts
