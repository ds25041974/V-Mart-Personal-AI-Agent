"""
Customer Analytics Module for V-Mart Retail Intelligence
Analyzes footfall, conversion, demographics, catchment area
"""

from typing import Dict, List, Optional, Any
from .formatters import format_inr, format_quantity, format_percentage, format_growth
from datetime import datetime, timedelta
import math


class CustomerAnalyzer:
    """AI-powered customer behavior and footfall analysis"""
    
    def __init__(self, gemini_engine=None):
        """
        Initialize CustomerAnalyzer
        
        Args:
            gemini_engine: GeminiRetailInsights instance for AI insights
        """
        self.gemini_engine = gemini_engine
    
    def analyze_footfall(
        self,
        footfall_data: Any,
        period: str = "weekly"
    ) -> Dict[str, Any]:
        """
        Analyze footfall patterns and trends
        
        Args:
            footfall_data: Footfall data - can be list or dict format
            period: Analysis period ('daily', 'weekly', 'monthly')
            
        Returns:
            Dict with footfall analysis, peak times, trends
        """
        try:
            # Handle list format (timestamp + count entries)
            if isinstance(footfall_data, list):
                from collections import defaultdict
                hourly_counts = defaultdict(int)
                total_count = 0
                
                for entry in footfall_data:
                    count = entry.get('count', 0)
                    total_count += count
                    
                    # Try to extract hour from timestamp
                    timestamp = entry.get('timestamp', '')
                    if timestamp and ':' in timestamp:
                        hour = int(timestamp.split()[1].split(':')[0])
                        hourly_counts[hour] += count
                
                if not hourly_counts:
                    hourly_counts[10] = total_count  # Default to 10 AM if no time data
                
                # Convert to standard format
                footfall_data = {
                    'hourly_footfall': dict(hourly_counts),
                    'store_id': 'default'
                }
            
            # Now process as dict format
            # Extract footfall metrics
            hourly_footfall = footfall_data.get('hourly_footfall', {})
            daily_footfall = footfall_data.get('daily_footfall', {})
            store_id = footfall_data.get('store_id', 'Unknown')
            
            # Calculate totals and averages
            if hourly_footfall:
                total_footfall = sum(hourly_footfall.values())
                avg_hourly = total_footfall / len(hourly_footfall) if hourly_footfall else 0
                
                # Find peak hours
                peak_hours = sorted(
                    hourly_footfall.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]
                
                # Find slowest hours
                slowest_hours = sorted(
                    hourly_footfall.items(),
                    key=lambda x: x[1]
                )[:3]
                
                hourly_analysis = {
                    'total_footfall': format_quantity(total_footfall, 'visitors'),
                    'avg_per_hour': format_quantity(avg_hourly, 'visitors', 1),
                    'peak_hours': [
                        {
                            'hour': f"{hour}:00",
                            'footfall': format_quantity(count, 'visitors'),
                            'percentage': format_percentage(count / total_footfall * 100) if total_footfall > 0 else '0%'
                        }
                        for hour, count in peak_hours
                    ],
                    'slowest_hours': [
                        {
                            'hour': f"{hour}:00",
                            'footfall': format_quantity(count, 'visitors'),
                            'percentage': format_percentage(count / total_footfall * 100) if total_footfall > 0 else '0%'
                        }
                        for hour, count in slowest_hours
                    ]
                }
            else:
                hourly_analysis = {}
            
            # Initialize variables
            wow_growth = 0
            peak_hours = []
            slowest_hours = []
            
            # Daily footfall analysis
            if daily_footfall:
                total_daily = sum(daily_footfall.values())
                avg_daily = total_daily / len(daily_footfall) if daily_footfall else 0
                
                # Calculate week-over-week growth
                if len(daily_footfall) >= 14:
                    recent_week = sum(list(daily_footfall.values())[-7:])
                    previous_week = sum(list(daily_footfall.values())[-14:-7])
                    wow_growth = ((recent_week - previous_week) / previous_week * 100) if previous_week > 0 else 0
                else:
                    wow_growth = 0
                
                daily_analysis = {
                    'total_footfall': format_quantity(total_daily, 'visitors'),
                    'avg_per_day': format_quantity(avg_daily, 'visitors', 1),
                    'week_over_week_growth': format_growth(recent_week if 'recent_week' in locals() else avg_daily,
                                                          previous_week if 'previous_week' in locals() else avg_daily)
                }
            else:
                daily_analysis = {}
            
            result = {
                'success': True,
                'store_id': store_id,
                'period': period,
                'analysis_date': datetime.now().strftime('%d-%b-%Y'),
                'hourly_analysis': hourly_analysis,
                'daily_analysis': daily_analysis,
                'summary': {
                    'peak_time': peak_hours[0][0] if hourly_footfall and peak_hours else 'N/A',
                    'slowest_time': slowest_hours[0][0] if hourly_footfall and slowest_hours else 'N/A',
                    'trend': 'Growing' if wow_growth > 0 else ('Declining' if wow_growth < 0 else 'Stable') if 'wow_growth' in locals() else 'Unknown'
                }
            }
            
            # Get AI insights on footfall patterns
            if self.gemini_engine:
                query = f"""
                Analyze footfall patterns for store {store_id}.
                
                Provide insights on:
                1. **Peak Hour Strategy**: How to maximize conversions during peak hours
                2. **Slow Hour Optimization**: Activities to attract customers during slow hours
                3. **Staffing Recommendations**: Optimal staffing based on footfall patterns
                4. **Marketing Timing**: Best times for promotions and marketing activities
                5. **Customer Behavior**: What footfall patterns reveal about customer habits
                6. **Action Plan**: Specific actions to improve overall footfall
                
                Footfall Summary:
                - Peak Hours: {', '.join([f"{p['hour']} ({p['footfall']})" for p in (hourly_analysis.get('peak_hours', [])[:3])])}
                - Daily Average: {daily_analysis.get('avg_per_day', 'N/A')}
                - Trend: {result['summary']['trend']}
                """
                
                ai_insights = self.gemini_engine.analyze_customer_behavior({
                    'analysis_type': 'footfall',
                    'data': result
                })
                result['ai_insights'] = ai_insights
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to analyze footfall data'
            }
    
    def analyze_conversion(
        self,
        footfall: int,
        transactions: int,
        sales_inr: int,
        period: str = "monthly"
    ) -> Dict[str, Any]:
        """
        Analyze sales conversion metrics
        
        Args:
            footfall: Total footfall count
            transactions: Number of transactions
            sales_inr: Total sales amount in INR
            period: Analysis period
            
        Returns:
            Dict with conversion rate, avg bill value, insights
        """
        try:
            # Calculate conversion metrics
            conversion_rate = (transactions / footfall * 100) if footfall > 0 else 0
            avg_bill_value = sales_inr / transactions if transactions > 0 else 0
            revenue_per_visitor = sales_inr / footfall if footfall > 0 else 0
            
            # Determine conversion quality
            if conversion_rate >= 25:
                conversion_grade = 'Excellent'
                grade_color = '🟢'
            elif conversion_rate >= 20:
                conversion_grade = 'Good'
                grade_color = '🟡'
            elif conversion_rate >= 15:
                conversion_grade = 'Average'
                grade_color = '🟠'
            else:
                conversion_grade = 'Needs Improvement'
                grade_color = '🔴'
            
            # Calculate potential revenue (if conversion improved to 25%)
            target_conversion = 0.25
            potential_transactions = int(footfall * target_conversion)
            potential_revenue = potential_transactions * avg_bill_value
            revenue_opportunity = potential_revenue - sales_inr
            
            result = {
                'success': True,
                'period': period,
                'analysis_date': datetime.now().strftime('%d-%b-%Y'),
                'metrics': {
                    'total_footfall': format_quantity(footfall, 'visitors'),
                    'total_transactions': format_quantity(transactions, 'transactions'),
                    'total_sales': format_inr(sales_inr),
                    'conversion_rate': format_percentage(conversion_rate, 2),
                    'avg_bill_value': format_inr(avg_bill_value),
                    'revenue_per_visitor': format_inr(revenue_per_visitor)
                },
                'performance': {
                    'conversion_grade': f"{grade_color} {conversion_grade}",
                    'benchmark_conversion': '25%',
                    'gap_to_benchmark': format_percentage(25 - conversion_rate, 2)
                },
                'opportunity': {
                    'potential_transactions': format_quantity(potential_transactions - transactions, 'additional'),
                    'potential_revenue': format_inr(revenue_opportunity),
                    'description': f'If conversion improves to 25%, additional {format_inr(revenue_opportunity)} revenue'
                },
                'summary': {
                    'conversion_rate_raw': conversion_rate,
                    'avg_bill_raw': avg_bill_value,
                    'grade': conversion_grade
                }
            }
            
            # Get AI recommendations for improving conversion
            if self.gemini_engine:
                query = f"""
                Analyze sales conversion performance and provide actionable recommendations.
                
                Current Metrics:
                - Footfall: {format_quantity(footfall, 'visitors')}
                - Transactions: {format_quantity(transactions, 'transactions')}
                - Sales: {format_inr(sales_inr)}
                - Conversion Rate: {format_percentage(conversion_rate, 2)}
                - Average Bill: {format_inr(avg_bill_value)}
                - Grade: {conversion_grade}
                
                Provide:
                1. **Root Cause Analysis**: Why is conversion at current level?
                2. **Conversion Improvement Strategies**: Specific tactics to increase conversion
                3. **Average Bill Enhancement**: How to increase ticket size
                4. **Customer Journey Optimization**: Improve path from entry to purchase
                5. **Staff Training**: What skills staff need to improve conversion
                6. **Visual Merchandising**: How to arrange store for better conversion
                7. **Promotional Strategies**: Offers that drive purchases
                8. **KPIs to Track**: What metrics to monitor for improvement
                9. **Implementation Phases**: Step-by-step action plan
                10. **Expected Impact**: Projected improvement with recommended actions
                
                Target: Improve conversion to 25% and increase average bill by 15%
                """
                
                ai_recommendations = self.gemini_engine.get_insights(
                    query=query,
                    context_data=result,
                    analytics_type='conversion_analysis'
                )
                result['ai_recommendations'] = ai_recommendations
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to analyze conversion metrics'
            }
    
    def analyze_catchment_area(
        self,
        store_location: List[float],
        customer_data: Optional[Dict[str, Any]] = None,
        radius_km: int = 5
    ) -> Dict[str, Any]:
        """
        Analyze customer catchment area around store
        
        Args:
            store_location: [latitude, longitude] of store
            customer_data: Optional customer location/demographic data
            radius_km: Catchment radius in kilometers
            
        Returns:
            Dict with catchment analysis, demographics, penetration
        """
        try:
            latitude, longitude = store_location
            
            # If customer data provided, analyze distribution
            if customer_data and 'customer_locations' in customer_data:
                customer_locations = customer_data['customer_locations']
                
                # Calculate distances and categorize
                distance_buckets = {
                    '0-2 km': 0,
                    '2-5 km': 0,
                    '5-10 km': 0,
                    '10+ km': 0
                }
                
                for cust_loc in customer_locations:
                    try:
                        cust_lat, cust_lon = cust_loc['latitude'], cust_loc['longitude']
                        distance = self._calculate_distance(latitude, longitude, cust_lat, cust_lon)
                        
                        if distance <= 2:
                            distance_buckets['0-2 km'] += 1
                        elif distance <= 5:
                            distance_buckets['2-5 km'] += 1
                        elif distance <= 10:
                            distance_buckets['5-10 km'] += 1
                        else:
                            distance_buckets['10+ km'] += 1
                    except:
                        continue
                
                total_customers = sum(distance_buckets.values())
                distance_distribution = {
                    bucket: {
                        'count': format_quantity(count, 'customers'),
                        'percentage': format_percentage(count / total_customers * 100) if total_customers > 0 else '0%'
                    }
                    for bucket, count in distance_buckets.items()
                }
            else:
                distance_distribution = {}
                total_customers = 0
            
            # Demographic analysis if available
            demographics = {}
            if customer_data and 'demographics' in customer_data:
                demo_data = customer_data['demographics']
                
                demographics = {
                    'age_groups': demo_data.get('age_groups', {}),
                    'family_status': demo_data.get('family_status', {}),
                    'income_segments': demo_data.get('income_segments', {}),
                    'gender_split': demo_data.get('gender_split', {})
                }
            
            # Calculate catchment area statistics
            area_sq_km = math.pi * (radius_km ** 2)
            
            # Estimated population (rough estimate for Indian tier-2/3 cities: ~3000 per sq km)
            estimated_population = int(area_sq_km * 3000)
            
            # Market penetration
            penetration_rate = (total_customers / estimated_population * 100) if estimated_population > 0 else 0
            
            result = {
                'success': True,
                'store_location': {
                    'latitude': latitude,
                    'longitude': longitude,
                    'radius_km': radius_km
                },
                'catchment_stats': {
                    'catchment_area': f"{area_sq_km:.2f} sq km",
                    'estimated_population': format_quantity(estimated_population, 'people'),
                    'known_customers': format_quantity(total_customers, 'customers'),
                    'market_penetration': format_percentage(penetration_rate, 2),
                    'penetration_grade': 'Excellent' if penetration_rate > 5 else (
                        'Good' if penetration_rate > 3 else (
                            'Average' if penetration_rate > 1 else 'Low'
                        )
                    )
                },
                'distance_distribution': distance_distribution,
                'demographics': demographics,
                'analysis_date': datetime.now().strftime('%d-%b-%Y')
            }
            
            # Get AI insights on catchment area
            if self.gemini_engine:
                query = f"""
                Analyze customer catchment area and provide growth strategies.
                
                Store Location: {latitude}, {longitude}
                Catchment Radius: {radius_km} km
                Total Area: {area_sq_km:.2f} sq km
                Estimated Population: {format_quantity(estimated_population, 'people')}
                Known Customers: {format_quantity(total_customers, 'customers')}
                Market Penetration: {format_percentage(penetration_rate, 2)}
                
                Customer Distribution:
                {distance_distribution}
                
                Provide insights on:
                1. **Catchment Area Assessment**: Is the current penetration good?
                2. **Growth Opportunities**: Untapped areas within catchment
                3. **Marketing Strategies**: How to reach more customers in area
                4. **Location Advantages**: What makes this location good/challenging
                5. **Competition Analysis**: Likely competitor presence in area
                6. **Expansion Potential**: Should we open more stores nearby?
                7. **Customer Acquisition**: Best channels to acquire customers
                8. **Retention Strategies**: How to retain existing catchment customers
                9. **Local Partnerships**: Community connections to explore
                10. **Action Plan**: Specific steps to improve penetration to 5%+
                """
                
                ai_insights = self.gemini_engine.analyze_customer_behavior({
                    'analysis_type': 'catchment_area',
                    'data': result
                })
                result['ai_insights'] = ai_insights
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to analyze catchment area'
            }
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        
        Returns:
            Distance in kilometers
        """
        # Earth radius in kilometers
        R = 6371
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        # Haversine formula
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance
