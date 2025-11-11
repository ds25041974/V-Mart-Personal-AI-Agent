"""
Analytics Engine for V-Mart Store Intelligence

This module provides comprehensive analytics combining store data, weather conditions,
competition analysis, sales trends, and inventory levels to generate actionable insights.
"""

import json
import random
import sqlite3
import uuid
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

from stores.database import StoreDatabase
from stores.models import Store, WeatherPeriod

from analytics.models import (
    ANALYTICS_DATABASE_SCHEMA,
    BusinessInsight,
    CompetitionImpact,
    DemandForecast,
    InsightCategory,
    InsightPriority,
    InventoryData,
    InventoryRecommendation,
    PerformanceMetrics,
    SalesData,
    SalesTrend,
    WeatherImpactAnalysis,
)


class AnalyticsEngine:
    """
    Main analytics engine that combines multiple data sources to generate insights
    """

    def __init__(self, db_path: str = "vmart_analytics.db"):
        self.db_path = db_path
        self.store_db = StoreDatabase()
        self.initialize_analytics_db()

    def initialize_analytics_db(self):
        """Initialize analytics database tables"""
        conn = sqlite3.connect(self.db_path)
        conn.executescript(ANALYTICS_DATABASE_SCHEMA)
        conn.commit()
        conn.close()

    # ==================== Sales Analytics ====================

    def analyze_sales_trends(self, store_id: str, days: int = 30) -> SalesTrend:
        """
        Analyze sales trends for a store over the specified period
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        # Get sales data (using mock data for now)
        sales_data = self._get_sales_data(store_id, start_date, end_date)

        if not sales_data:
            # Generate mock trend data
            return self._generate_mock_sales_trend(store_id, start_date, end_date)

        total_sales = sum(s.total_sales for s in sales_data)
        avg_daily_sales = total_sales / days

        # Calculate growth (comparing to previous period)
        previous_sales = self._get_previous_period_sales(store_id, start_date, days)
        growth = (
            ((total_sales - previous_sales) / previous_sales * 100)
            if previous_sales > 0
            else 0
        )

        # Find peak periods
        peak_day, peak_period = self._find_peak_sales_periods(sales_data)

        # Analyze category performance
        trending_cats, underperforming_cats = self._analyze_category_trends(sales_data)

        return SalesTrend(
            store_id=store_id,
            period_start=start_date,
            period_end=end_date,
            total_sales=total_sales,
            sales_growth=growth,
            average_daily_sales=avg_daily_sales,
            peak_sales_day=peak_day,
            peak_sales_period=peak_period,
            trending_categories=trending_cats,
            underperforming_categories=underperforming_cats,
        )

    def analyze_weather_impact(
        self, store_id: str, days: int = 30
    ) -> WeatherImpactAnalysis:
        """
        Analyze how weather conditions impact sales at a store
        """
        # Get store location
        store = self.store_db.get_vmart_store(store_id)
        if not store:
            raise ValueError(f"Store {store_id} not found")

        # Get weather data for the period
        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        weather_data = []
        for i in range(days):
            check_date = start_date + timedelta(days=i)
            for period in WeatherPeriod:
                weather = self.store_db.get_weather_data(
                    store.location.latitude,
                    store.location.longitude,
                    check_date,
                    period,
                )
                if weather:
                    weather_data.extend(weather)

        # Analyze patterns (using mock analysis)
        return self._analyze_weather_sales_correlation(store_id, weather_data)

    def analyze_competition_impact(
        self, store_id: str, radius_km: float = 10.0
    ) -> CompetitionImpact:
        """
        Analyze impact of nearby competitors on store performance
        """
        # Get proximity analysis
        analysis = self.store_db.get_proximity_analysis(store_id)

        if not analysis:
            # Run fresh analysis
            from stores.analyzer import StoreAnalyzer

            analyzer = StoreAnalyzer(self.store_db)
            analysis = analyzer.analyze_vmart_competition(store_id, radius_km)

        if not analysis:
            raise ValueError(f"Could not analyze competition for store {store_id}")

        competitor_count = analysis.get_competitor_count()
        closest = analysis.get_closest_competitor()
        nearest_distance = (
            closest.location.distance_to(analysis.vmart_store.location)
            if closest
            else float("inf")
        )

        # Estimate market impact based on competition density
        market_share = self._estimate_market_share(competitor_count, nearest_distance)
        sales_impact = self._estimate_sales_impact(competitor_count, nearest_distance)

        # Generate strategic recommendations
        advantages = self._identify_competitive_advantages(analysis)
        threats = self._identify_competitive_threats(analysis)
        strategies = self._recommend_competitive_strategies(analysis)

        return CompetitionImpact(
            store_id=store_id,
            competitor_count=competitor_count,
            nearest_competitor_distance=nearest_distance,
            estimated_market_share=market_share,
            sales_impact=sales_impact,
            competitive_advantages=advantages,
            competitive_threats=threats,
            recommended_strategies=strategies,
        )

    # ==================== Inventory Analytics ====================

    def generate_inventory_recommendations(
        self, store_id: str
    ) -> List[InventoryRecommendation]:
        """
        Generate inventory optimization recommendations based on sales, weather, and trends
        """
        recommendations = []

        # Get current inventory data
        inventory_data = self._get_inventory_data(store_id)

        # Get sales trends
        sales_trend = self.analyze_sales_trends(store_id, days=30)

        # Get weather forecast
        store = self.store_db.get_vmart_store(store_id)
        if not store:
            return recommendations

        # Analyze each category
        categories = [
            "Men's Wear",
            "Women's Wear",
            "Kids Wear",
            "Accessories",
            "Footwear",
            "Home Goods",
        ]

        for category in categories:
            inv_data = inventory_data.get(category)
            if not inv_data:
                # Generate mock data
                inv_data = self._generate_mock_inventory(store_id, category)

            # Calculate optimal stock level
            recommended_stock = self._calculate_optimal_stock(
                store_id, category, sales_trend, inv_data
            )

            reorder_qty = max(0, recommended_stock - inv_data.stock_level)
            urgency = self._determine_reorder_urgency(inv_data, reorder_qty)
            stockout_risk = self._calculate_stockout_risk(inv_data, sales_trend)
            overstock_cost = self._calculate_overstock_cost(inv_data, recommended_stock)

            reasoning = self._generate_inventory_reasoning(
                category, inv_data, recommended_stock, sales_trend
            )

            seasonal_factors = self._get_seasonal_factors(category, date.today())

            recommendations.append(
                InventoryRecommendation(
                    store_id=store_id,
                    category=category,
                    current_stock=inv_data.stock_level,
                    recommended_stock=recommended_stock,
                    reorder_quantity=reorder_qty,
                    reorder_urgency=urgency,
                    estimated_stockout_risk=stockout_risk,
                    estimated_overstock_cost=overstock_cost,
                    reasoning=reasoning,
                    seasonal_factors=seasonal_factors,
                )
            )

        return recommendations

    # ==================== Demand Forecasting ====================

    def forecast_demand(
        self, store_id: str, category: str, days_ahead: int = 7
    ) -> List[DemandForecast]:
        """
        Forecast demand for a specific category combining multiple factors
        """
        forecasts = []
        store = self.store_db.get_vmart_store(store_id)
        if not store:
            return forecasts

        # Get historical patterns
        sales_trend = self.analyze_sales_trends(store_id, days=30)
        competition = self.analyze_competition_impact(store_id)

        for day_offset in range(1, days_ahead + 1):
            forecast_date = date.today() + timedelta(days=day_offset)

            # Base demand from historical average
            base_demand = self._get_historical_average_demand(store_id, category)

            # Apply factors
            trend_factor = 1.0 + (sales_trend.sales_growth / 100)
            seasonal_factor = self._get_seasonal_multiplier(category, forecast_date)
            competition_factor = 1.0 + (competition.sales_impact / 100)

            # Weather prediction (simplified)
            weather_factor_name = self._predict_weather_impact(forecast_date)
            weather_multiplier = self._get_weather_multiplier(
                weather_factor_name, category
            )

            # Calculate predicted demand
            predicted_demand = (
                base_demand
                * trend_factor
                * seasonal_factor
                * competition_factor
                * weather_multiplier
            )

            # Calculate confidence based on data quality
            confidence = self._calculate_forecast_confidence(
                has_sales_data=True,
                has_weather_data=True,
                has_competition_data=True,
                days_ahead=day_offset,
            )

            influencing_factors = {
                "trend": trend_factor,
                "seasonal": seasonal_factor,
                "competition": competition_factor,
                "weather": weather_multiplier,
            }

            forecasts.append(
                DemandForecast(
                    store_id=store_id,
                    forecast_date=forecast_date,
                    category=category,
                    predicted_demand=predicted_demand,
                    confidence_level=confidence,
                    influencing_factors=influencing_factors,
                    weather_factor=weather_factor_name,
                    competition_factor=competition_factor,
                    seasonal_factor=seasonal_factor,
                    trend_factor=trend_factor,
                )
            )

        return forecasts

    # ==================== Insights Generation ====================

    def generate_insights(self, store_id: str) -> List[BusinessInsight]:
        """
        Generate comprehensive business insights from all data sources
        """
        insights = []

        # Analyze all dimensions
        sales_trend = self.analyze_sales_trends(store_id)
        weather_impact = self.analyze_weather_impact(store_id)
        competition = self.analyze_competition_impact(store_id)
        inventory_recs = self.generate_inventory_recommendations(store_id)

        # Generate insights from sales trends
        if sales_trend.sales_growth < -10:
            insights.append(
                self._create_insight(
                    store_id=store_id,
                    category=InsightCategory.SALES,
                    priority=InsightPriority.CRITICAL,
                    title="Significant Sales Decline Detected",
                    description=f"Sales have declined by {abs(sales_trend.sales_growth):.1f}% over the last 30 days. Immediate action required.",
                    impact=f"Estimated revenue loss: ₹{abs(sales_trend.sales_growth) * sales_trend.average_daily_sales * 30 / 100:.2f}",
                    actions=[
                        "Review pricing strategy and competitor prices",
                        "Launch promotional campaigns",
                        "Analyze customer feedback and satisfaction",
                        "Review product mix and inventory",
                        "Increase marketing and visibility",
                    ],
                    data_sources=["sales_data", "trend_analysis"],
                    confidence=85.0,
                )
            )

        # Generate insights from weather impact
        if abs(weather_impact.sales_variance) > 15:
            direction = "increase" if weather_impact.sales_variance > 0 else "decrease"
            insights.append(
                self._create_insight(
                    store_id=store_id,
                    category=InsightCategory.WEATHER,
                    priority=InsightPriority.MEDIUM,
                    title=f"Weather Causing {abs(weather_impact.sales_variance):.1f}% Sales {direction.capitalize()}",
                    description=f"Current weather conditions ({weather_impact.weather_condition}) are significantly impacting sales.",
                    impact=f"Sales variance: {weather_impact.sales_variance:+.1f}%",
                    actions=weather_impact.recommended_actions,
                    data_sources=["weather_data", "sales_data"],
                    confidence=72.0,
                )
            )

        # Generate insights from competition
        if competition.competitor_count > 5:
            insights.append(
                self._create_insight(
                    store_id=store_id,
                    category=InsightCategory.COMPETITION,
                    priority=InsightPriority.HIGH,
                    title=f"High Competition Density: {competition.competitor_count} Competitors Nearby",
                    description=f"Store faces intense competition with {competition.competitor_count} competitors within 10km radius.",
                    impact=f"Estimated market share: {competition.estimated_market_share:.1f}%, Sales impact: {competition.sales_impact:+.1f}%",
                    actions=competition.recommended_strategies,
                    data_sources=["competitor_data", "proximity_analysis"],
                    confidence=78.0,
                )
            )

        # Generate insights from inventory
        critical_inventory = [
            rec
            for rec in inventory_recs
            if rec.reorder_urgency == InsightPriority.CRITICAL
        ]
        if critical_inventory:
            categories = ", ".join([rec.category for rec in critical_inventory])
            insights.append(
                self._create_insight(
                    store_id=store_id,
                    category=InsightCategory.INVENTORY,
                    priority=InsightPriority.CRITICAL,
                    title=f"Critical Stock Shortage: {len(critical_inventory)} Categories",
                    description=f"The following categories need immediate restock: {categories}",
                    impact=f"High stockout risk (avg {sum(r.estimated_stockout_risk for r in critical_inventory) / len(critical_inventory):.1f}%)",
                    actions=[
                        f"Reorder {rec.reorder_quantity} units of {rec.category}"
                        for rec in critical_inventory
                    ],
                    data_sources=["inventory_data", "sales_forecast"],
                    confidence=90.0,
                )
            )

        return insights

    def get_performance_metrics(
        self, store_id: str, days: int = 30
    ) -> PerformanceMetrics:
        """
        Get comprehensive performance metrics for a store
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        # Gather all metrics
        sales_trend = self.analyze_sales_trends(store_id, days)
        competition = self.analyze_competition_impact(store_id)
        inventory_recs = self.generate_inventory_recommendations(store_id)
        weather_impact = self.analyze_weather_impact(store_id, days)

        # Calculate aggregated metrics (using mock data)
        total_revenue = sales_trend.total_sales
        transaction_count = int(total_revenue / 850)  # Mock avg transaction
        footfall = int(transaction_count / 0.35)  # Mock conversion rate

        avg_inventory_turnover = (
            sum(r.current_stock / max(1, r.recommended_stock) for r in inventory_recs)
            / len(inventory_recs)
            if inventory_recs
            else 2.5
        )

        stockout_count = sum(
            1 for r in inventory_recs if r.estimated_stockout_risk > 50
        )
        stockout_rate = (
            (stockout_count / len(inventory_recs) * 100) if inventory_recs else 0
        )

        overstock_cost = sum(r.estimated_overstock_cost for r in inventory_recs)

        # Determine competitive position
        if competition.estimated_market_share > 40:
            competitive_position = "Leading"
        elif competition.estimated_market_share > 30:
            competitive_position = "Strong"
        elif competition.estimated_market_share > 20:
            competitive_position = "Moderate"
        else:
            competitive_position = "Weak"

        return PerformanceMetrics(
            store_id=store_id,
            period_start=start_date,
            period_end=end_date,
            total_revenue=total_revenue,
            revenue_growth=sales_trend.sales_growth,
            average_transaction_value=total_revenue / transaction_count
            if transaction_count > 0
            else 0,
            transaction_count=transaction_count,
            inventory_turnover=avg_inventory_turnover,
            stockout_rate=stockout_rate,
            overstock_cost=overstock_cost,
            market_share_estimate=competition.estimated_market_share,
            competitive_position=competitive_position,
            footfall=footfall,
            conversion_rate=35.0,  # Mock
            weather_impact_score=weather_impact.sales_variance,
        )

    # ==================== Helper Methods ====================

    def _get_sales_data(
        self, store_id: str, start_date: date, end_date: date
    ) -> List[SalesData]:
        """Get sales data from database (returns mock data for now)"""
        # In production, query actual sales database
        return []  # Empty triggers mock data generation

    def _generate_mock_sales_trend(
        self, store_id: str, start_date: date, end_date: date
    ) -> SalesTrend:
        """Generate realistic mock sales trend"""
        days = (end_date - start_date).days

        # Simulate sales with some variance
        base_daily_sales = random.uniform(80000, 150000)
        total_sales = base_daily_sales * days
        growth = random.uniform(-15, 25)

        categories = [
            "Men's Wear",
            "Women's Wear",
            "Kids Wear",
            "Accessories",
            "Footwear",
        ]
        trending = [
            (cat, random.uniform(15, 40)) for cat in random.sample(categories, 2)
        ]
        underperforming = [
            (cat, random.uniform(-20, -5)) for cat in random.sample(categories, 2)
        ]

        return SalesTrend(
            store_id=store_id,
            period_start=start_date,
            period_end=end_date,
            total_sales=total_sales,
            sales_growth=growth,
            average_daily_sales=base_daily_sales,
            peak_sales_day=random.choice(["Saturday", "Sunday", "Friday"]),
            peak_sales_period=random.choice(["Evening", "Afternoon"]),
            trending_categories=trending,
            underperforming_categories=underperforming,
        )

    def _generate_mock_inventory(self, store_id: str, category: str) -> InventoryData:
        """Generate mock inventory data"""
        stock_level = random.randint(500, 3000)
        reorder_point = int(stock_level * 0.3)

        return InventoryData(
            store_id=store_id,
            date=date.today(),
            category=category,
            stock_level=stock_level,
            reorder_point=reorder_point,
            days_of_supply=random.uniform(15, 45),
            stockout_incidents=random.randint(0, 3),
            overstock_value=random.uniform(0, 50000),
            turnover_rate=random.uniform(2.0, 4.5),
        )

    def _get_previous_period_sales(
        self, store_id: str, start_date: date, days: int
    ) -> float:
        """Get sales from previous comparable period"""
        return random.uniform(2000000, 3500000)  # Mock

    def _find_peak_sales_periods(self, sales_data: List[SalesData]) -> Tuple[str, str]:
        """Find peak sales day and period"""
        return ("Saturday", "Evening")  # Mock

    def _analyze_category_trends(
        self, sales_data: List[SalesData]
    ) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
        """Analyze which categories are trending"""
        categories = [
            "Men's Wear",
            "Women's Wear",
            "Kids Wear",
            "Accessories",
            "Footwear",
        ]
        trending = [
            (cat, random.uniform(15, 40)) for cat in random.sample(categories, 2)
        ]
        underperforming = [
            (cat, random.uniform(-20, -5)) for cat in random.sample(categories, 2)
        ]
        return trending, underperforming

    def _analyze_weather_sales_correlation(
        self, store_id: str, weather_data: list
    ) -> WeatherImpactAnalysis:
        """Analyze correlation between weather and sales"""
        # Simplified mock analysis
        conditions = ["Clear", "Clouds", "Rain", "Haze"]
        condition = random.choice(conditions)

        temp_range = (random.uniform(15, 25), random.uniform(25, 35))
        avg_sales = random.uniform(90000, 140000)
        variance = random.uniform(-20, 20)

        actions = []
        if "Rain" in condition:
            actions = [
                "Stock more umbrellas and rainwear",
                "Promote indoor/home products",
                "Increase online delivery capacity",
            ]
        elif temp_range[1] > 30:
            actions = [
                "Promote summer wear and cooling products",
                "Ensure AC is optimal",
                "Stock cold beverages if applicable",
            ]
        else:
            actions = ["Monitor weather patterns", "Maintain balanced inventory"]

        affected_cats = [("Footwear", variance * 0.8), ("Accessories", variance * 0.6)]

        return WeatherImpactAnalysis(
            store_id=store_id,
            weather_condition=condition,
            temperature_range=temp_range,
            average_sales=avg_sales,
            sales_variance=variance,
            recommended_actions=actions,
            affected_categories=affected_cats,
        )

    def _estimate_market_share(
        self, competitor_count: int, nearest_distance: float
    ) -> float:
        """Estimate market share based on competition"""
        # Simplified estimation
        base_share = 50.0
        competition_penalty = competitor_count * 3.5
        distance_bonus = min(10, nearest_distance / 2)
        return max(10, base_share - competition_penalty + distance_bonus)

    def _estimate_sales_impact(
        self, competitor_count: int, nearest_distance: float
    ) -> float:
        """Estimate sales impact from competition"""
        if competitor_count == 0:
            return 0

        # Negative impact increases with competition
        base_impact = -5.0
        count_penalty = competitor_count * -2.5
        distance_mitigation = min(8, nearest_distance / 1.5)

        return base_impact + count_penalty + distance_mitigation

    def _identify_competitive_advantages(self, analysis) -> List[str]:
        """Identify competitive advantages"""
        advantages = []

        if analysis.get_competitor_count() < 3:
            advantages.append("Low competition density in area")

        advantages.extend(
            [
                "Established V-Mart brand recognition",
                "Wide product range across categories",
                "Competitive pricing strategy",
                "Strong customer service reputation",
            ]
        )

        return advantages

    def _identify_competitive_threats(self, analysis) -> List[str]:
        """Identify competitive threats"""
        threats = []

        competitor_count = analysis.get_competitor_count()
        if competitor_count > 5:
            threats.append(
                f"High competition density ({competitor_count} nearby competitors)"
            )

        chains = analysis.get_competitors_by_chain()
        if "Zudio" in [c.chain.value for c in chains.get("Zudio", [])]:
            threats.append("Zudio's aggressive pricing in local market")

        threats.extend(
            [
                "E-commerce competition affecting footfall",
                "Seasonal demand fluctuations",
            ]
        )

        return threats

    def _recommend_competitive_strategies(self, analysis) -> List[str]:
        """Recommend competitive strategies"""
        strategies = [
            "Strengthen loyalty programs and customer retention",
            "Differentiate with exclusive product lines",
            "Enhance in-store experience and customer service",
            "Leverage local marketing and community engagement",
        ]

        if analysis.get_competitor_count() > 5:
            strategies.insert(0, "Focus on price competitiveness for key categories")

        return strategies

    def _get_inventory_data(self, store_id: str) -> Dict[str, InventoryData]:
        """Get current inventory data"""
        return {}  # Empty triggers mock data

    def _calculate_optimal_stock(
        self,
        store_id: str,
        category: str,
        sales_trend: SalesTrend,
        inv_data: InventoryData,
    ) -> int:
        """Calculate optimal stock level"""
        # Simplified calculation
        daily_avg_demand = sales_trend.average_daily_sales / 6  # 6 categories
        safety_stock_days = 7
        reorder_lead_time = 3

        optimal = int(daily_avg_demand * (safety_stock_days + reorder_lead_time))
        return optimal

    def _determine_reorder_urgency(
        self, inv_data: InventoryData, reorder_qty: int
    ) -> InsightPriority:
        """Determine urgency of reorder"""
        if inv_data.stock_level < inv_data.reorder_point * 0.5:
            return InsightPriority.CRITICAL
        elif inv_data.stock_level < inv_data.reorder_point:
            return InsightPriority.HIGH
        elif reorder_qty > 0:
            return InsightPriority.MEDIUM
        return InsightPriority.LOW

    def _calculate_stockout_risk(
        self, inv_data: InventoryData, sales_trend: SalesTrend
    ) -> float:
        """Calculate risk of stockout"""
        if inv_data.days_of_supply < 7:
            return 80.0
        elif inv_data.days_of_supply < 14:
            return 50.0
        elif inv_data.days_of_supply < 21:
            return 20.0
        return 5.0

    def _calculate_overstock_cost(
        self, inv_data: InventoryData, recommended_stock: int
    ) -> float:
        """Calculate cost of overstocking"""
        if inv_data.stock_level > recommended_stock * 1.5:
            excess = inv_data.stock_level - recommended_stock
            return excess * 150  # Mock: ₹150 per unit holding cost
        return 0

    def _generate_inventory_reasoning(
        self,
        category: str,
        inv_data: InventoryData,
        recommended_stock: int,
        sales_trend: SalesTrend,
    ) -> str:
        """Generate reasoning for inventory recommendation"""
        if inv_data.stock_level < recommended_stock:
            return f"Current stock ({inv_data.stock_level}) below optimal level. Sales trending up {sales_trend.sales_growth:.1f}%. Restock recommended to avoid stockouts."
        elif inv_data.stock_level > recommended_stock * 1.3:
            return f"Current stock ({inv_data.stock_level}) exceeds optimal level. Consider reducing orders to minimize holding costs."
        return f"Stock level optimal. Monitor sales trends and adjust as needed."

    def _get_seasonal_factors(self, category: str, current_date: date) -> List[str]:
        """Get seasonal factors affecting inventory"""
        month = current_date.month
        factors = []

        # Festival seasons
        if month in [10, 11]:
            factors.append("Diwali festival season - high demand expected")
        elif month in [3, 4]:
            factors.append("Holi and spring season")
        elif month in [8, 9]:
            factors.append("Ganesh Chaturthi and festive season")

        # Weather seasons
        if month in [6, 7, 8, 9]:
            factors.append("Monsoon season")
        elif month in [11, 12, 1, 2]:
            factors.append("Winter season")
        elif month in [3, 4, 5]:
            factors.append("Summer season")

        return factors

    def _get_historical_average_demand(self, store_id: str, category: str) -> float:
        """Get historical average demand"""
        return random.uniform(100, 500)  # Mock units per day

    def _get_seasonal_multiplier(self, category: str, forecast_date: date) -> float:
        """Get seasonal demand multiplier"""
        month = forecast_date.month

        # Festival season boost
        if month in [10, 11]:
            return 1.5
        elif month in [8, 9]:
            return 1.3
        elif month in [3, 4]:
            return 1.2

        return 1.0

    def _predict_weather_impact(self, forecast_date: date) -> str:
        """Predict weather impact (simplified)"""
        return random.choice(["Clear", "Clouds", "Rain", "Hot"])

    def _get_weather_multiplier(self, weather: str, category: str) -> float:
        """Get weather impact multiplier"""
        if weather == "Rain":
            if category in ["Footwear", "Accessories"]:
                return 1.2
            return 0.9
        elif weather == "Hot":
            if category == "Men's Wear":
                return 1.1
            return 1.0
        return 1.0

    def _calculate_forecast_confidence(
        self,
        has_sales_data: bool,
        has_weather_data: bool,
        has_competition_data: bool,
        days_ahead: int,
    ) -> float:
        """Calculate confidence in forecast"""
        base_confidence = 50.0

        if has_sales_data:
            base_confidence += 20
        if has_weather_data:
            base_confidence += 15
        if has_competition_data:
            base_confidence += 10

        # Confidence decreases with forecast horizon
        time_penalty = days_ahead * 3

        return max(30, min(95, base_confidence - time_penalty))

    def _create_insight(
        self,
        store_id: str,
        category: InsightCategory,
        priority: InsightPriority,
        title: str,
        description: str,
        impact: str,
        actions: List[str],
        data_sources: List[str],
        confidence: float,
    ) -> BusinessInsight:
        """Create a business insight"""
        insight_id = f"INS_{store_id}_{uuid.uuid4().hex[:8].upper()}"

        # Insights expire based on priority
        expires_at = None
        if priority == InsightPriority.CRITICAL:
            expires_at = datetime.now() + timedelta(days=2)
        elif priority == InsightPriority.HIGH:
            expires_at = datetime.now() + timedelta(days=7)
        elif priority == InsightPriority.MEDIUM:
            expires_at = datetime.now() + timedelta(days=14)

        return BusinessInsight(
            insight_id=insight_id,
            store_id=store_id,
            category=category,
            priority=priority,
            title=title,
            description=description,
            impact=impact,
            recommended_actions=actions,
            data_sources=data_sources,
            confidence_score=confidence,
            created_at=datetime.now(),
            expires_at=expires_at,
        )
