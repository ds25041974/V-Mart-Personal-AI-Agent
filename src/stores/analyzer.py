"""
Store Analyzer - Competitor Proximity and Analysis
"""

from datetime import datetime
from typing import List, Optional

from .database import StoreDatabase
from .models import CompetitorAnalysis, GeoLocation, Store, StoreChain


class StoreAnalyzer:
    """Analyze store locations and competitor proximity"""

    def __init__(self, database: StoreDatabase):
        """Initialize analyzer with database"""
        self.db = database

    def find_nearby_competitors(
        self, vmart_store: Store, radius_km: float = 5.0
    ) -> List[Store]:
        """
        Find all competitor stores within radius of a V-Mart store

        Args:
            vmart_store: V-Mart Store object
            radius_km: Search radius in kilometers (default 5km)

        Returns:
            List of competitor stores within radius
        """
        all_competitors = self.db.get_competitor_stores()
        nearby = []

        for competitor in all_competitors:
            distance = vmart_store.location.distance_to(competitor.location)
            if distance <= radius_km:
                nearby.append(competitor)

        return nearby

    def analyze_vmart_competition(
        self, vmart_store_id: str, radius_km: float = 5.0
    ) -> Optional[CompetitorAnalysis]:
        """
        Perform full competition analysis for a V-Mart store

        Args:
            vmart_store_id: V-Mart store ID
            radius_km: Search radius

        Returns:
            CompetitorAnalysis object or None if store not found
        """
        vmart_store = self.db.get_vmart_store(vmart_store_id)
        if not vmart_store:
            return None

        nearby_competitors = self.find_nearby_competitors(vmart_store, radius_km)

        analysis = CompetitorAnalysis(
            vmart_store=vmart_store,
            nearby_competitors=nearby_competitors,
            analysis_date=datetime.now(),
            search_radius_km=radius_km,
        )

        # Save analysis to database
        self.db.save_proximity_analysis(analysis)

        return analysis

    def analyze_all_vmart_stores(
        self, radius_km: float = 5.0
    ) -> List[CompetitorAnalysis]:
        """
        Analyze competition for all V-Mart stores

        Args:
            radius_km: Search radius

        Returns:
            List of CompetitorAnalysis objects
        """
        vmart_stores = self.db.get_all_vmart_stores()
        analyses = []

        for store in vmart_stores:
            analysis = self.analyze_vmart_competition(store.store_id, radius_km)
            if analysis:
                analyses.append(analysis)

        return analyses

    def get_stores_by_city(self, city: str) -> dict:
        """
        Get all stores (V-Mart and competitors) in a city

        Args:
            city: City name

        Returns:
            Dictionary with vmart_stores and competitor_stores
        """
        vmart_stores = self.db.get_vmart_stores_by_city(city)
        competitor_stores = self.db.get_competitor_stores_by_city(city)

        return {
            "city": city,
            "vmart_stores": [s.to_dict() for s in vmart_stores],
            "competitor_stores": [s.to_dict() for s in competitor_stores],
            "vmart_count": len(vmart_stores),
            "competitor_count": len(competitor_stores),
        }

    def get_competition_summary(self) -> dict:
        """
        Get overall competition summary

        Returns:
            Dictionary with statistics
        """
        vmart_stores = self.db.get_all_vmart_stores()
        all_competitors = self.db.get_competitor_stores()

        # Count competitors by chain
        competitors_by_chain = {}
        for competitor in all_competitors:
            chain = competitor.chain.value
            competitors_by_chain[chain] = competitors_by_chain.get(chain, 0) + 1

        # Get cities with most V-Marts
        cities = {}
        for store in vmart_stores:
            city = store.location.city
            cities[city] = cities.get(city, 0) + 1

        top_cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "total_vmart_stores": len(vmart_stores),
            "total_competitor_stores": len(all_competitors),
            "competitors_by_chain": competitors_by_chain,
            "top_10_cities": [
                {"city": city, "store_count": count} for city, count in top_cities
            ],
            "unique_cities": len(cities),
        }
