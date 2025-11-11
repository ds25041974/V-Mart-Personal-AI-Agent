"""
Sales Analytics Module
Comprehensive sales performance analysis, forecasting, and insights
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from .formatters import format_inr, format_quantity, format_percentage, format_growth


class SalesAnalyzer:
    """
    Sales performance analysis and forecasting
    Covers: Daily/hourly sales, salesperson performance, target tracking
    """

    def __init__(self, gemini_engine=None):
        """Initialize Sales Analyzer with optional Gemini AI engine"""
        self.gemini_engine = gemini_engine

    def analyze_sales_data(
        self, sales_data: Dict[str, Any], period: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze sales data - generic entry point for sales analysis
        
        Args:
            sales_data: Sales data dict with period, amounts, categories
            period: Optional period override
            
        Returns:
            Dict with sales analysis results
        """
        try:
            analysis_period = period or sales_data.get('period', 'monthly')
            sales_by_category = sales_data.get('sales_by_category', {})
            total_sales = sum(sales_by_category.values())
            
            result = {
                'success': True,
                'period': analysis_period,
                'total_sales': format_inr(total_sales),
                'total_sales_raw': total_sales,
                'categories_analyzed': len(sales_by_category),
                'category_breakdown': {
                    cat: {
                        'sales': format_inr(amt),
                        'percentage': format_percentage(amt / total_sales if total_sales > 0 else 0)
                    }
                    for cat, amt in sorted(sales_by_category.items(), key=lambda x: x[1], reverse=True)
                },
                'top_category': max(sales_by_category.items(), key=lambda x: x[1])[0] if sales_by_category else None,
                'summary': {
                    'total_revenue': format_inr(total_sales),
                    'category_count': len(sales_by_category),
                    'avg_per_category': format_inr(total_sales / len(sales_by_category) if sales_by_category else 0)
                }
            }
            
            # Get AI insights if engine available
            if self.gemini_engine:
                ai_insights = self.gemini_engine.get_insights(
                    query=f"Analyze sales performance for {analysis_period} period",
                    context_data=result,
                    analytics_type='sales'
                )
                result['ai_recommendations'] = ai_insights
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to analyze sales data'
            }

    def analyze_daily_sales(
        self, sales_data: List[Dict[str, Any]], store_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze daily sales performance

        Args:
            sales_data: List of daily sales records
            store_id: Optional store ID filter

        Returns:
            Comprehensive sales analysis
        """
        total_sales = sum(day["amount"] for day in sales_data)
        total_transactions = sum(day.get("transactions", 0) for day in sales_data)
        avg_daily_sales = total_sales / len(sales_data) if sales_data else 0

        analysis = {
            "period": {
                "start_date": sales_data[0]["date"] if sales_data else None,
                "end_date": sales_data[-1]["date"] if sales_data else None,
                "days_count": len(sales_data),
            },
            "summary": {
                "total_sales": format_inr(total_sales),
                "total_sales_raw": total_sales,
                "avg_daily_sales": format_inr(avg_daily_sales),
                "total_transactions": format_quantity(total_transactions, "transactions"),
                "avg_transaction_value": format_inr(
                    total_sales / total_transactions if total_transactions > 0 else 0
                ),
            },
            "daily_breakdown": [
                {
                    "date": day["date"],
                    "sales": format_inr(day["amount"]),
                    "transactions": day.get("transactions", 0),
                    "avg_bill": format_inr(
                        day["amount"] / day.get("transactions", 1)
                        if day.get("transactions", 0) > 0
                        else 0
                    ),
                }
                for day in sales_data
            ],
        }

        # Get AI insights if engine available
        if self.gemini_engine:
            ai_insights = self.gemini_engine.analyze_sales_performance(
                {
                    "total_sales_inr": total_sales,
                    "days": len(sales_data),
                    "avg_daily_sales_inr": avg_daily_sales,
                    "total_transactions": total_transactions,
                    "store_id": store_id,
                }
            )
            analysis["ai_insights"] = ai_insights.get("insights", "")

        return analysis

    def analyze_hourly_sales(
        self, hourly_data: List[Dict[str, Any]], date: str
    ) -> Dict[str, Any]:
        """
        Analyze hourly sales patterns for peak hour identification

        Args:
            hourly_data: List of hourly sales records
            date: Date for analysis

        Returns:
            Hourly analysis with peak hours
        """
        total_sales = sum(hour["amount"] for hour in hourly_data)
        peak_hour = max(hourly_data, key=lambda x: x["amount"])
        slowest_hour = min(hourly_data, key=lambda x: x["amount"])

        hourly_breakdown = []
        for hour_data in hourly_data:
            hour = hour_data["hour"]
            amount = hour_data["amount"]
            transactions = hour_data.get("transactions", 0)

            hourly_breakdown.append(
                {
                    "hour": f"{hour:02d}:00",
                    "sales": format_inr(amount),
                    "sales_raw": amount,
                    "transactions": transactions,
                    "avg_bill": format_inr(amount / transactions if transactions > 0 else 0),
                    "percentage_of_day": format_percentage(
                        (amount / total_sales * 100) if total_sales > 0 else 0
                    ),
                    "is_peak": hour == peak_hour["hour"],
                }
            )

        analysis = {
            "date": date,
            "total_sales": format_inr(total_sales),
            "peak_hour": {
                "time": f"{peak_hour['hour']:02d}:00",
                "sales": format_inr(peak_hour["amount"]),
                "percentage": format_percentage(
                    (peak_hour["amount"] / total_sales * 100) if total_sales > 0 else 0
                ),
            },
            "slowest_hour": {
                "time": f"{slowest_hour['hour']:02d}:00",
                "sales": format_inr(slowest_hour["amount"]),
            },
            "hourly_breakdown": hourly_breakdown,
        }

        # Get AI insights
        if self.gemini_engine:
            ai_insights = self.gemini_engine.get_hourly_sales_insights(
                {
                    "date": date,
                    "total_sales_inr": total_sales,
                    "peak_hour": peak_hour["hour"],
                    "peak_sales_inr": peak_hour["amount"],
                    "hourly_data": hourly_breakdown,
                }
            )
            analysis["ai_insights"] = ai_insights.get("insights", "")
            analysis["recommendations"] = {
                "staffing": "Optimize staff during peak hours",
                "promotions": f"Run promotions during {slowest_hour['hour']:02d}:00 to boost sales",
                "inventory": "Ensure adequate stock before peak hours",
            }

        return analysis

    def analyze_salesperson_performance(
        self, salesperson_data: List[Dict[str, Any]], period: str = "month"
    ) -> Dict[str, Any]:
        """
        Analyze individual salesperson performance

        Args:
            salesperson_data: List of salesperson sales records
            period: Analysis period (day, week, month)

        Returns:
            Salesperson performance analysis
        """
        total_sales = sum(sp["sales_amount"] for sp in salesperson_data)
        total_transactions = sum(sp.get("transactions", 0) for sp in salesperson_data)

        performance_list = []
        for sp in salesperson_data:
            sales = sp["sales_amount"]
            target = sp.get("target", 0)
            achievement = (sales / target * 100) if target > 0 else 0

            performance_list.append(
                {
                    "name": sp["name"],
                    "id": sp.get("id", ""),
                    "sales": format_inr(sales),
                    "sales_raw": sales,
                    "target": format_inr(target),
                    "achievement": format_percentage(achievement),
                    "transactions": sp.get("transactions", 0),
                    "avg_bill": format_inr(
                        sales / sp.get("transactions", 1)
                        if sp.get("transactions", 0) > 0
                        else 0
                    ),
                    "percentage_contribution": format_percentage(
                        (sales / total_sales * 100) if total_sales > 0 else 0
                    ),
                    "rank": 0,  # Will be set after sorting
                }
            )

        # Sort by sales and assign ranks
        performance_list.sort(key=lambda x: x["sales_raw"], reverse=True)
        for i, sp in enumerate(performance_list, 1):
            sp["rank"] = i

        top_performer = performance_list[0] if performance_list else None
        low_performer = performance_list[-1] if performance_list else None

        analysis = {
            "period": period,
            "summary": {
                "total_sales": format_inr(total_sales),
                "total_salespersons": len(salesperson_data),
                "avg_sales_per_person": format_inr(
                    total_sales / len(salesperson_data) if salesperson_data else 0
                ),
                "total_transactions": total_transactions,
            },
            "top_performer": top_performer,
            "needs_improvement": low_performer,
            "performance_list": performance_list,
        }

        # AI insights
        if self.gemini_engine:
            ai_insights = self.gemini_engine.get_insights(
                f"Analyze salesperson performance for {period}. "
                f"Top performer: {top_performer['name']} with {top_performer['sales']}. "
                f"Provide training and improvement recommendations.",
                context_data={
                    "total_sales_inr": total_sales,
                    "salesperson_count": len(salesperson_data),
                    "top_sales_inr": top_performer["sales_raw"] if top_performer else 0,
                },
                analytics_type="salesperson_performance",
            )
            analysis["ai_insights"] = ai_insights.get("insights", "")

        return analysis

    def analyze_target_achievement(
        self, target_data: Dict[str, Any], actual_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze sales target vs actual achievement

        Args:
            target_data: Target sales data by category/period
            actual_data: Actual sales data

        Returns:
            Target achievement analysis
        """
        analysis = {
            "summary": {
                "target_total": format_inr(target_data.get("total", 0)),
                "actual_total": format_inr(actual_data.get("total", 0)),
                "achievement": format_percentage(
                    (actual_data.get("total", 0) / target_data.get("total", 1) * 100)
                ),
                "variance": format_inr(
                    actual_data.get("total", 0) - target_data.get("total", 0)
                ),
            },
            "category_wise": [],
        }

        # Category-wise analysis
        for category in target_data.get("categories", {}):
            target = target_data["categories"][category]
            actual = actual_data.get("categories", {}).get(category, 0)
            achievement_pct = (actual / target * 100) if target > 0 else 0

            analysis["category_wise"].append(
                {
                    "category": category,
                    "target": format_inr(target),
                    "actual": format_inr(actual),
                    "achievement": format_percentage(achievement_pct),
                    "variance": format_inr(actual - target),
                    "status": (
                        "✅ Achieved"
                        if achievement_pct >= 100
                        else "⚠️  Below Target"
                        if achievement_pct >= 80
                        else "❌ Critical"
                    ),
                }
            )

        return analysis

    def forecast_sales(
        self, historical_data: List[Dict[str, Any]], forecast_days: int = 30
    ) -> Dict[str, Any]:
        """
        Forecast future sales using AI and trend analysis

        Args:
            historical_data: Historical sales data
            forecast_days: Number of days to forecast

        Returns:
            Sales forecast
        """
        if not historical_data:
            return {"error": "No historical data provided"}

        # Calculate basic trend
        total_sales = sum(day["amount"] for day in historical_data)
        avg_daily = total_sales / len(historical_data)

        # Simple growth calculation
        if len(historical_data) >= 7:
            recent_week = sum(day["amount"] for day in historical_data[-7:]) / 7
            older_week = sum(day["amount"] for day in historical_data[-14:-7]) / 7
            growth_rate = ((recent_week - older_week) / older_week * 100) if older_week > 0 else 0
        else:
            growth_rate = 0

        forecast = {
            "period": f"Next {forecast_days} days",
            "based_on_days": len(historical_data),
            "avg_daily_sales": format_inr(avg_daily),
            "growth_trend": format_percentage(growth_rate),
            "forecast_total": format_inr(avg_daily * forecast_days * (1 + growth_rate / 100)),
        }

        # AI-powered forecast
        if self.gemini_engine:
            ai_forecast = self.gemini_engine.get_insights(
                f"Forecast sales for next {forecast_days} days based on historical data. "
                f"Average daily sales: {format_inr(avg_daily)}, "
                f"Recent growth trend: {format_percentage(growth_rate)}",
                context_data={
                    "historical_days": len(historical_data),
                    "avg_daily_inr": avg_daily,
                    "growth_rate": growth_rate,
                    "forecast_days": forecast_days,
                },
                analytics_type="sales_forecasting",
            )
            forecast["ai_forecast"] = ai_forecast.get("insights", "")

        return forecast
