"""
Gemini AI Retail Insights Engine
Core AI system for V-Mart retail intelligence, forecasting, and recommendations
Powered by Google Gemini 2.0 Flash
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import google.generativeai as genai


class GeminiRetailInsights:
    """
    Core AI engine for V-Mart retail operations
    Provides insights, recommendations, predictions, and forecasting
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini AI engine"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=self.api_key)

        # Configure Gemini 2.0 Flash for retail insights
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                "temperature": 0.7,  # Balanced creativity for insights
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            },
        )

        # Start chat session
        self.chat = self.model.start_chat(history=[])

        # System context for V-Mart retail intelligence
        self.system_context = """
You are an AI-powered retail intelligence assistant for V-Mart, India's leading value fashion retail chain.

**Your Role:**
- Provide data-driven insights, recommendations, and forecasting for retail operations
- Analyze sales, inventory, customer behavior, and market trends
- Support planning for buying, merchandising, marketing, and operations
- Use Indian context (INR currency, Indian festivals, regional preferences)
- Communicate professionally yet conversationally

**V-Mart Context:**
- Value fashion retailer focused on tier-2 and tier-3 cities
- 11 stores across Uttar Pradesh, Bihar, Madhya Pradesh, Rajasthan
- Target customers: Middle-class families in smaller cities
- Product categories: Apparel, footwear, accessories for men, women, children
- Competitors: Pantaloons, Zudio, Reliance Trends, Westside, V2 Retail, Max Fashion

**Response Guidelines:**
1. For greetings (Hi, Hello, etc.): Respond warmly and professionally as a human assistant
2. For analysis questions: Provide detailed, data-driven insights with specific numbers
3. For forecasts: Use historical trends, seasonality, festivals, and market context
4. For recommendations: Provide actionable suggestions with reasoning
5. Always use INR (₹) for amounts and appropriate units for quantities
6. Consider Indian festivals, regional variations, and local customer preferences
7. Elaborate with proper detailing and summarizations

**Formatting:**
- Currency: ₹10,00,000 (INR lakhs format) or ₹1.5 Cr (crores)
- Quantities: 1,500 units, 25,000 pieces, 500 kg
- Percentages: 15.5% growth, 8.2% margin
- Dates: DD-MMM-YYYY (e.g., 15-Nov-2025)

**Key Focus Areas:**
- Sales Performance Analysis (hourly, daily, weekly, monthly, YoY)
- Inventory Planning & Forecasting
- Fashion & Trend Analysis (local and global)
- Festival Planning (Diwali, Holi, regional festivals)
- Customer Analytics & Footfall Analysis
- Marketing Performance & ROI
- Inter-Store Transfer (IST) Planning
- Logistics Optimization
- People Planning & Scheduling
- Buying & Merchandising Recommendations

Be insightful, actionable, and specific in your responses.
"""

    def get_insights(
        self,
        query: str,
        context_data: Optional[Dict[str, Any]] = None,
        analytics_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get AI-powered insights for any retail query

        Args:
            query: User's question or prompt
            context_data: Additional context (sales data, inventory, etc.)
            analytics_type: Type of analysis (sales, inventory, fashion, etc.)

        Returns:
            Dictionary with insights, recommendations, and metadata
        """
        # Build enhanced prompt with context
        enhanced_prompt = self._build_prompt(query, context_data, analytics_type)

        try:
            # Get response from Gemini
            response = self.chat.send_message(enhanced_prompt)

            return {
                "success": True,
                "query": query,
                "insights": response.text,
                "analytics_type": analytics_type,
                "timestamp": datetime.now().isoformat(),
                "model": "gemini-2.0-flash-exp",
            }

        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def _build_prompt(
        self,
        query: str,
        context_data: Optional[Dict[str, Any]],
        analytics_type: Optional[str],
    ) -> str:
        """Build enhanced prompt with system context and data"""
        prompt_parts = [self.system_context, "\n\n**Current Query:**", query]

        if analytics_type:
            prompt_parts.append(f"\n**Analysis Type:** {analytics_type}")

        if context_data:
            prompt_parts.append("\n**Available Data:**")
            for key, value in context_data.items():
                prompt_parts.append(f"- {key}: {value}")

        prompt_parts.append(
            "\n\nProvide detailed, actionable insights with specific recommendations and numbers in INR/quantities as applicable."
        )

        return "\n".join(prompt_parts)

    def analyze_sales_performance(self, sales_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sales performance with AI insights"""
        query = f"""
Analyze the following sales performance data and provide comprehensive insights:

**Sales Data:**
{self._format_data_for_prompt(sales_data)}

Please provide:
1. Overall Performance Assessment
2. Top Performing & Underperforming Areas
3. Trends & Patterns Identified
4. Growth Opportunities
5. Specific Recommendations for Improvement
6. Sales Forecasts for Next Period

Include specific numbers in INR and percentages.
"""
        return self.get_insights(query, sales_data, "sales_performance")

    def forecast_inventory(self, inventory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Forecast inventory needs with AI-powered planning"""
        query = f"""
Based on the inventory data and sales trends, provide inventory forecasting and planning recommendations:

**Inventory Data:**
{self._format_data_for_prompt(inventory_data)}

Please provide:
1. Current Inventory Health Assessment
2. Stock-out Risk Analysis
3. Overstock Identification
4. Procurement Recommendations (quantities and ₹ amounts)
5. Inter-Store Transfer (IST) Suggestions
6. Optimal Stock Levels by Category
7. Seasonal Inventory Planning

Use INR for amounts and units for quantities.
"""
        return self.get_insights(query, inventory_data, "inventory_forecasting")

    def analyze_fashion_trends(self, trend_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze fashion trends for buying and merchandising"""
        query = f"""
Analyze fashion and merchandising trends to guide buying decisions:

**Trend Data:**
{self._format_data_for_prompt(trend_data)}

Please provide:
1. Current Fashion Trends (Global & Indian Market)
2. Category-wise Trend Analysis
3. Color, Pattern, Style Preferences
4. Seasonal Recommendations
5. Buying Priorities & Quantities
6. Merchandising Strategy
7. Pricing Recommendations

Focus on value fashion segment for tier-2/3 cities.
"""
        return self.get_insights(query, trend_data, "fashion_trends")

    def plan_festival_inventory(
        self, festival_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Plan inventory for Indian festivals"""
        query = f"""
Provide festival-specific inventory planning and sales forecasting:

**Festival Planning Data:**
{self._format_data_for_prompt(festival_data)}

Please provide:
1. Festival Sales Forecast (₹ amounts)
2. Category-wise Inventory Requirements
3. Regional Preferences & Variations
4. Marketing & Promotional Strategies
5. Procurement Timeline & Quantities
6. Pricing Strategy for Festival Season
7. Post-Festival Clearance Planning

Consider major festivals: Diwali, Holi, Eid, Durga Puja, Onam, Pongal, and regional festivals.
"""
        return self.get_insights(query, festival_data, "festival_planning")

    def analyze_customer_behavior(
        self, customer_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze customer behavior and catchment area"""
        query = f"""
Analyze customer behavior, footfall, and catchment area dynamics:

**Customer Data:**
{self._format_data_for_prompt(customer_data)}

Please provide:
1. Customer Demographic Analysis
2. Footfall Trends & Patterns
3. Sales Conversion Analysis
4. Customer Lifetime Value Insights
5. Catchment Area Recommendations
6. Customer Retention Strategies
7. Upselling & Cross-selling Opportunities

Focus on tier-2/3 city customer preferences.
"""
        return self.get_insights(query, customer_data, "customer_analytics")

    def optimize_logistics(self, logistics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize logistics and operations"""
        query = f"""
Provide logistics optimization and operational planning recommendations:

**Logistics Data:**
{self._format_data_for_prompt(logistics_data)}

Please provide:
1. Best Route Planning for Deliveries
2. Inter-Store Transfer (IST) Optimization
3. Cost Reduction Opportunities
4. Warehouse Utilization Analysis
5. Transportation Efficiency Improvements
6. People Planning & Scheduling
7. Operational Bottleneck Identification

Include cost savings in INR.
"""
        return self.get_insights(query, logistics_data, "logistics_optimization")

    def analyze_marketing_performance(
        self, marketing_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze marketing campaigns and ROI"""
        query = f"""
Analyze marketing performance and provide recommendations:

**Marketing Data:**
{self._format_data_for_prompt(marketing_data)}

Please provide:
1. Campaign Performance Analysis
2. ROI Calculation (₹ spent vs ₹ revenue)
3. Channel Effectiveness (Online, Offline, Social)
4. Customer Acquisition Cost
5. Marketing Mix Optimization
6. Budget Allocation Recommendations
7. Future Campaign Strategies

Use INR for all financial metrics.
"""
        return self.get_insights(query, marketing_data, "marketing_analytics")

    def get_hourly_sales_insights(
        self, hourly_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze hourly sales patterns for peak hour identification"""
        query = f"""
Analyze hourly sales patterns to identify peak sales hours and optimize operations:

**Hourly Sales Data:**
{self._format_data_for_prompt(hourly_data)}

Please provide:
1. Peak Sales Hours Identification
2. Hourly Sales Patterns by Day of Week
3. Staff Scheduling Recommendations
4. Promotional Timing Optimization
5. Inventory Replenishment Schedule
6. Customer Flow Management
7. Revenue Maximization Strategies

Include hourly ₹ amounts and conversion rates.
"""
        return self.get_insights(query, hourly_data, "hourly_sales_analysis")

    def handle_greeting(self, greeting: str) -> Dict[str, Any]:
        """Handle conversational greetings naturally"""
        greetings_map = {
            "hi": "Hello! I'm your V-Mart retail intelligence assistant. How can I help you today with sales analysis, inventory planning, fashion trends, or any other retail insights?",
            "hello": "Hi there! I'm here to provide AI-powered insights for V-Mart's retail operations. What would you like to analyze or plan today?",
            "hey": "Hey! Ready to help you with retail intelligence, forecasting, and planning. What can I assist you with?",
            "good morning": "Good morning! Hope you're having a great day. I'm here to support your retail decisions with AI-powered insights. How can I help?",
            "good afternoon": "Good afternoon! Let me know how I can assist you with sales analysis, inventory planning, or any retail intelligence needs.",
            "good evening": "Good evening! I'm here to help optimize V-Mart's retail operations. What insights do you need?",
            "namaste": "Namaste! 🙏 I'm your V-Mart retail intelligence assistant. How can I help you grow your business today?",
        }

        greeting_lower = greeting.lower().strip()
        for key, response in greetings_map.items():
            if key in greeting_lower:
                return {
                    "success": True,
                    "query": greeting,
                    "insights": response,
                    "type": "greeting",
                    "timestamp": datetime.now().isoformat(),
                }

        # If not a standard greeting, use Gemini for natural response
        return self.get_insights(greeting, analytics_type="conversation")

    def _format_data_for_prompt(self, data: Dict[str, Any]) -> str:
        """Format data dictionary for prompt"""
        if not data:
            return "No additional data provided"

        formatted_lines = []
        for key, value in data.items():
            if isinstance(value, (int, float)):
                formatted_lines.append(f"  - {key}: {value:,}")
            elif isinstance(value, dict):
                formatted_lines.append(f"  - {key}:")
                for sub_key, sub_value in value.items():
                    formatted_lines.append(f"      * {sub_key}: {sub_value}")
            else:
                formatted_lines.append(f"  - {key}: {value}")

        return "\n".join(formatted_lines)

    def reset_conversation(self):
        """Reset chat history for fresh conversation"""
        self.chat = self.model.start_chat(history=[])
