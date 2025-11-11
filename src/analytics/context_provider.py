"""
Analytics Context Provider for Gemini AI Integration

This module provides relevant analytics data as context for AI responses,
enabling Gemini to give data-driven insights and recommendations.
"""

import logging
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Any

from analytics.engine import AnalyticsEngine
from stores.database import StoreDatabase

logger = logging.getLogger(__name__)


class AnalyticsContextProvider:
    """
    Provides analytics context for AI conversations
    """

    def __init__(self):
        self.analytics_engine = AnalyticsEngine()
        self.store_db = StoreDatabase()

    def get_context_for_prompt(
        self, prompt: str, store_id: Optional[str] = None, days: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze the prompt and return relevant analytics context
        
        Args:
            prompt: User's question/prompt
            store_id: Specific store ID (if None, will try to detect from prompt)
            days: Number of days of historical data to include
            
        Returns:
            Dict containing relevant analytics data
        """
        try:
            prompt_lower = prompt.lower()
            context = {
                "has_data": False,
                "store_info": None,
                "sales_data": None,
                "inventory_data": None,
                "weather_impact": None,
                "competition_data": None,
                "insights": None,
                "context_summary": "",
            }

            # Detect store from prompt if not provided
            if not store_id:
                store_id = self._detect_store_from_prompt(prompt)

            if not store_id:
                # No specific store, check if asking about network-wide data
                if self._is_network_query(prompt):
                    return self._get_network_context(prompt)
                return context

            # Get store information
            store = self.store_db.get_store(store_id)
            if not store:
                return context

            context["has_data"] = True
            context["store_info"] = {
                "store_id": store.store_id,
                "name": store.name,
                "city": store.city,
                "state": store.state,
            }

            # Determine what analytics to include based on prompt keywords
            include_sales = self._should_include_sales(prompt_lower)
            include_inventory = self._should_include_inventory(prompt_lower)
            include_weather = self._should_include_weather(prompt_lower)
            include_competition = self._should_include_competition(prompt_lower)
            include_insights = self._should_include_insights(prompt_lower)

            # If no specific category detected, include all for comprehensive analysis
            if not any(
                [
                    include_sales,
                    include_inventory,
                    include_weather,
                    include_competition,
                    include_insights,
                ]
            ):
                include_sales = True
                include_insights = True

            # Fetch relevant analytics data
            if include_sales:
                context["sales_data"] = self._get_sales_context(store_id, days)

            if include_inventory:
                context["inventory_data"] = self._get_inventory_context(store_id)

            if include_weather:
                context["weather_impact"] = self._get_weather_context(store_id, days)

            if include_competition:
                context["competition_data"] = self._get_competition_context(store_id)

            if include_insights:
                context["insights"] = self._get_insights_context(store_id)

            # Generate context summary
            context["context_summary"] = self._generate_context_summary(context)

            return context

        except Exception as e:
            logger.error(f"Error getting analytics context: {str(e)}")
            return {
                "has_data": False,
                "error": str(e),
                "context_summary": "Analytics data temporarily unavailable.",
            }

    def format_context_for_ai(self, context: Dict[str, Any]) -> str:
        """
        Format analytics context into a readable prompt section for the AI
        
        Args:
            context: Context dictionary from get_context_for_prompt
            
        Returns:
            Formatted string to append to AI prompt
        """
        if not context.get("has_data"):
            return ""

        sections = []

        # Store Information
        if context.get("store_info"):
            store_info = context["store_info"]
            sections.append(
                f"STORE INFORMATION:\n"
                f"- Store: {store_info['name']} ({store_info['store_id']})\n"
                f"- Location: {store_info['city']}, {store_info['state']}"
            )

        # Sales Data
        if context.get("sales_data"):
            sales = context["sales_data"]
            sections.append(
                f"\nSALES ANALYTICS (Last {sales.get('period_days', 30)} days):\n"
                f"- Total Sales: ₹{sales['total_sales']:,.2f}\n"
                f"- Sales Growth: {sales['sales_growth']:+.2f}%\n"
                f"- Average Daily Sales: ₹{sales['avg_daily_sales']:,.2f}\n"
                f"- Peak Period: {sales['peak_day']} {sales['peak_period']}\n"
                f"- Trending Categories: {', '.join(sales['trending_categories'])}\n"
                f"- Underperforming: {', '.join(sales['underperforming_categories'])}"
            )

        # Inventory Data
        if context.get("inventory_data"):
            inventory = context["inventory_data"]
            sections.append(
                f"\nINVENTORY STATUS:\n"
                f"- Categories Analyzed: {inventory['total_categories']}\n"
                f"- Critical Reorders: {inventory['critical_reorders']}\n"
                f"- High Priority: {inventory['high_priority_reorders']}\n"
                f"- Overstock Items: {inventory['overstock_count']}\n"
                f"- Top Recommendations: {', '.join(inventory['top_recommendations'])}"
            )

        # Weather Impact
        if context.get("weather_impact"):
            weather = context["weather_impact"]
            sections.append(
                f"\nWEATHER IMPACT ANALYSIS:\n"
                f"- Primary Condition: {weather['primary_condition']}\n"
                f"- Temperature Range: {weather['temp_range']}\n"
                f"- Sales Variance: {weather['sales_variance']:+.1f}%\n"
                f"- Affected Categories: {', '.join(weather['affected_categories'])}\n"
                f"- Recommendations: {weather['weather_recommendations']}"
            )

        # Competition Data
        if context.get("competition_data"):
            comp = context["competition_data"]
            sections.append(
                f"\nCOMPETITION ANALYSIS:\n"
                f"- Nearby Competitors: {comp['competitor_count']}\n"
                f"- Nearest Competitor: {comp['nearest_distance']:.1f} km\n"
                f"- Estimated Market Share: {comp['market_share']:.1f}%\n"
                f"- Sales Impact: {comp['sales_impact']:+.1f}%\n"
                f"- Competitive Advantages: {', '.join(comp['advantages'])}\n"
                f"- Threats: {', '.join(comp['threats'])}"
            )

        # Business Insights
        if context.get("insights"):
            insights_data = context["insights"]
            sections.append(
                f"\nBUSINESS INSIGHTS:\n"
                f"- Critical Insights: {insights_data['critical_count']}\n"
                f"- High Priority: {insights_data['high_priority_count']}\n"
                f"- Key Recommendations:\n"
            )
            for idx, rec in enumerate(insights_data["top_recommendations"][:3], 1):
                sections.append(f"  {idx}. [{rec['priority']}] {rec['title']}: {rec['description']}")

        return "\n".join(sections)

    def _detect_store_from_prompt(self, prompt: str) -> Optional[str]:
        """Detect store ID from prompt"""
        # Try to find store ID patterns (VM_XXX_XXX)
        import re

        pattern = r"VM_[A-Z]{2,3}_\d{3}"
        match = re.search(pattern, prompt.upper())
        if match:
            return match.group(0)

        # Try to detect city names
        all_stores = self.store_db.get_all_stores()
        prompt_lower = prompt.lower()

        for store in all_stores:
            if store.city.lower() in prompt_lower:
                return store.store_id
            if store.name.lower() in prompt_lower:
                return store.store_id

        # Default to Delhi store for demo
        return "VM_DL_001"

    def _is_network_query(self, prompt: str) -> bool:
        """Check if query is about network-wide data"""
        network_keywords = [
            "all stores",
            "network",
            "total",
            "overall",
            "across stores",
            "company-wide",
            "entire chain",
        ]
        prompt_lower = prompt.lower()
        return any(keyword in prompt_lower for keyword in network_keywords)

    def _should_include_sales(self, prompt_lower: str) -> bool:
        """Check if sales data should be included"""
        keywords = [
            "sales",
            "revenue",
            "income",
            "earnings",
            "growth",
            "trend",
            "performance",
            "footfall",
            "transaction",
        ]
        return any(keyword in prompt_lower for keyword in keywords)

    def _should_include_inventory(self, prompt_lower: str) -> bool:
        """Check if inventory data should be included"""
        keywords = [
            "inventory",
            "stock",
            "reorder",
            "shortage",
            "overstock",
            "out of stock",
            "stockout",
        ]
        return any(keyword in prompt_lower for keyword in keywords)

    def _should_include_weather(self, prompt_lower: str) -> bool:
        """Check if weather data should be included"""
        keywords = [
            "weather",
            "rain",
            "temperature",
            "climate",
            "seasonal",
            "summer",
            "winter",
            "monsoon",
        ]
        return any(keyword in prompt_lower for keyword in keywords)

    def _should_include_competition(self, prompt_lower: str) -> bool:
        """Check if competition data should be included"""
        keywords = [
            "competition",
            "competitor",
            "market share",
            "rival",
            "competitive",
        ]
        return any(keyword in prompt_lower for keyword in keywords)

    def _should_include_insights(self, prompt_lower: str) -> bool:
        """Check if insights should be included"""
        keywords = [
            "insight",
            "recommendation",
            "suggest",
            "advice",
            "should i",
            "what to do",
            "how to",
            "improve",
        ]
        return any(keyword in prompt_lower for keyword in keywords)

    def _get_sales_context(self, store_id: str, days: int) -> Dict[str, Any]:
        """Get sales analytics context"""
        try:
            trend = self.analytics_engine.analyze_sales_trends(store_id, days)
            return {
                "period_days": days,
                "total_sales": trend.total_sales,
                "sales_growth": trend.sales_growth,
                "avg_daily_sales": trend.average_daily_sales,
                "peak_day": trend.peak_sales_day,
                "peak_period": trend.peak_sales_period,
                "trending_categories": [
                    f"{cat['category']} (+{cat['growth']:.1f}%)"
                    for cat in trend.trending_categories[:3]
                ],
                "underperforming_categories": [
                    f"{cat['category']} ({cat['growth']:.1f}%)"
                    for cat in trend.underperforming_categories[:3]
                ],
            }
        except Exception as e:
            logger.error(f"Error getting sales context: {str(e)}")
            return {}

    def _get_inventory_context(self, store_id: str) -> Dict[str, Any]:
        """Get inventory analytics context"""
        try:
            recommendations = self.analytics_engine.generate_inventory_recommendations(
                store_id
            )
            
            critical = [r for r in recommendations if r.reorder_urgency == "CRITICAL"]
            high = [r for r in recommendations if r.reorder_urgency == "HIGH"]
            overstock = [r for r in recommendations if r.overstock_cost > 0]

            return {
                "total_categories": len(recommendations),
                "critical_reorders": len(critical),
                "high_priority_reorders": len(high),
                "overstock_count": len(overstock),
                "top_recommendations": [
                    f"{r.category}: Reorder {r.reorder_quantity} units"
                    for r in recommendations[:3]
                ],
            }
        except Exception as e:
            logger.error(f"Error getting inventory context: {str(e)}")
            return {}

    def _get_weather_context(self, store_id: str, days: int) -> Dict[str, Any]:
        """Get weather impact context"""
        try:
            weather_impact = self.analytics_engine.analyze_weather_impact(store_id, days)
            return {
                "primary_condition": weather_impact.weather_condition,
                "temp_range": weather_impact.temperature_range,
                "sales_variance": weather_impact.sales_variance,
                "affected_categories": weather_impact.affected_categories[:3],
                "weather_recommendations": "; ".join(
                    weather_impact.recommended_actions[:2]
                ),
            }
        except Exception as e:
            logger.error(f"Error getting weather context: {str(e)}")
            return {}

    def _get_competition_context(self, store_id: str) -> Dict[str, Any]:
        """Get competition analysis context"""
        try:
            comp_impact = self.analytics_engine.analyze_competition_impact(store_id)
            return {
                "competitor_count": comp_impact.competitor_count,
                "nearest_distance": comp_impact.nearest_competitor_distance,
                "market_share": comp_impact.estimated_market_share,
                "sales_impact": comp_impact.sales_impact,
                "advantages": comp_impact.competitive_advantages[:2],
                "threats": comp_impact.competitive_threats[:2],
            }
        except Exception as e:
            logger.error(f"Error getting competition context: {str(e)}")
            return {}

    def _get_insights_context(self, store_id: str) -> Dict[str, Any]:
        """Get business insights context"""
        try:
            insights = self.analytics_engine.generate_insights(store_id)
            
            critical = [i for i in insights if i.priority == InsightPriority.CRITICAL]
            high = [i for i in insights if i.priority == InsightPriority.HIGH]

            return {
                "critical_count": len(critical),
                "high_priority_count": len(high),
                "total_insights": len(insights),
                "top_recommendations": [
                    {
                        "priority": i.priority.name,
                        "title": i.title,
                        "description": i.description,
                        "actions": i.recommended_actions[:2],
                    }
                    for i in insights[:5]
                ],
            }
        except Exception as e:
            logger.error(f"Error getting insights context: {str(e)}")
            return {}

    def _get_network_context(self, prompt: str) -> Dict[str, Any]:
        """Get network-wide analytics context"""
        try:
            # This would call the network summary endpoint logic
            # For now, return basic structure
            return {
                "has_data": True,
                "is_network_query": True,
                "context_summary": "Network-wide analytics requested. Use /analytics/all-stores/summary endpoint for comprehensive data.",
            }
        except Exception as e:
            logger.error(f"Error getting network context: {str(e)}")
            return {"has_data": False, "error": str(e)}

    def _generate_context_summary(self, context: Dict[str, Any]) -> str:
        """Generate a brief summary of available context"""
        parts = []
        
        if context.get("store_info"):
            parts.append(f"Store: {context['store_info']['name']}")
        
        if context.get("sales_data"):
            sales = context["sales_data"]
            parts.append(
                f"Sales: ₹{sales['total_sales']:,.0f} ({sales['sales_growth']:+.1f}%)"
            )
        
        if context.get("insights"):
            insights = context["insights"]
            if insights["critical_count"] > 0:
                parts.append(f"{insights['critical_count']} critical insights")
        
        return " | ".join(parts) if parts else "Analytics data available"
