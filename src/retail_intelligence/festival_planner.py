"""
Festival Planning Module for V-Mart Retail Intelligence
Plans for Indian festivals with sales forecasting and inventory optimization
"""

from typing import Dict, List, Optional, Any
from .formatters import format_inr, format_quantity, format_percentage, format_growth
from datetime import datetime, timedelta
import calendar


# Major Indian Festivals with typical sales multipliers
MAJOR_FESTIVALS = {
    'Diwali': {
        'duration_days': 5,
        'sales_multiplier': 3.5,
        'peak_categories': ['Womenswear', 'Menswear', 'Kidswear', 'Accessories'],
        'typical_months': [10, 11],  # Oct-Nov
        'description': 'Festival of Lights - Biggest shopping season'
    },
    'Durga Puja': {
        'duration_days': 5,
        'sales_multiplier': 3.0,
        'peak_categories': ['Womenswear', 'Ethnic wear', 'Accessories'],
        'typical_months': [9, 10],  # Sep-Oct
        'description': 'Major festival in Eastern India (West Bengal, Bihar)'
    },
    'Eid': {
        'duration_days': 3,
        'sales_multiplier': 2.5,
        'peak_categories': ['Menswear', 'Womenswear', 'Kidswear'],
        'typical_months': [3, 4, 5, 6],  # Varies with lunar calendar
        'description': 'Islamic festival - Strong ethnic wear demand'
    },
    'Navratri': {
        'duration_days': 9,
        'sales_multiplier': 2.5,
        'peak_categories': ['Womenswear', 'Ethnic wear', 'Accessories'],
        'typical_months': [9, 10],  # Sep-Oct
        'description': 'Nine nights festival - High demand for traditional wear'
    },
    'Holi': {
        'duration_days': 2,
        'sales_multiplier': 2.0,
        'peak_categories': ['Casualwear', 'White clothing'],
        'typical_months': [3],  # March
        'description': 'Festival of Colors - Casual and white wear popular'
    },
    'Raksha Bandhan': {
        'duration_days': 1,
        'sales_multiplier': 1.8,
        'peak_categories': ['Menswear', 'Kidswear', 'Accessories'],
        'typical_months': [8],  # August
        'description': 'Brother-Sister festival - Gifting season'
    },
    'Christmas': {
        'duration_days': 3,
        'sales_multiplier': 2.0,
        'peak_categories': ['Winterwear', 'Party wear'],
        'typical_months': [12],  # December
        'description': 'Christmas season - Winter and party wear demand'
    },
    'New Year': {
        'duration_days': 2,
        'sales_multiplier': 2.2,
        'peak_categories': ['Party wear', 'Western wear'],
        'typical_months': [12, 1],  # Dec-Jan
        'description': 'New Year celebrations - Party and trendy wear'
    }
}

# Regional Festivals by State
REGIONAL_FESTIVALS = {
    'Uttar Pradesh': {
        'Chhath Puja': {'duration_days': 4, 'multiplier': 1.5, 'month': 11},
        'Ram Navami': {'duration_days': 1, 'multiplier': 1.3, 'month': 4},
        'Janmashtami': {'duration_days': 1, 'multiplier': 1.4, 'month': 8}
    },
    'Bihar': {
        'Chhath Puja': {'duration_days': 4, 'multiplier': 2.0, 'month': 11},
        'Makar Sankranti': {'duration_days': 1, 'multiplier': 1.3, 'month': 1}
    },
    'Madhya Pradesh': {
        'Teej': {'duration_days': 1, 'multiplier': 1.4, 'month': 8},
        'Gangaur': {'duration_days': 1, 'multiplier': 1.3, 'month': 3}
    },
    'Rajasthan': {
        'Gangaur': {'duration_days': 2, 'multiplier': 1.5, 'month': 3},
        'Teej': {'duration_days': 1, 'multiplier': 1.4, 'month': 8},
        'Desert Festival': {'duration_days': 3, 'multiplier': 1.2, 'month': 2}
    }
}


class FestivalPlanner:
    """AI-powered festival planning and sales forecasting"""
    
    def __init__(self, gemini_engine=None):
        """
        Initialize FestivalPlanner
        
        Args:
            gemini_engine: GeminiRetailInsights instance for AI insights
        """
        self.gemini_engine = gemini_engine
        self.major_festivals = MAJOR_FESTIVALS
        self.regional_festivals = REGIONAL_FESTIVALS
    
    def forecast_festival_sales(
        self,
        festival_name: str,
        base_daily_sales: int,
        duration_days: Optional[int] = None,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Forecast sales for a specific festival
        
        Args:
            festival_name: Name of festival
            base_daily_sales: Normal daily sales in INR
            duration_days: Optional festival duration override
            year: Optional year for forecast
            
        Returns:
            Dict with sales forecast, category breakdown, recommendations
        """
        try:
            # Get festival data
            festival_data = self.major_festivals.get(festival_name)
            
            if not festival_data:
                # Check regional festivals
                for region, festivals in self.regional_festivals.items():
                    if festival_name in festivals:
                        festival_data = festivals[festival_name]
                        festival_data['region'] = region
                        break
            
            if not festival_data:
                return {
                    'success': False,
                    'error': f'Festival "{festival_name}" not found in database'
                }
            
            # Calculate festival sales
            duration = duration_days or festival_data.get('duration_days', 1)
            multiplier = festival_data.get('sales_multiplier') or festival_data.get('multiplier', 1.0)
            
            daily_festival_sales = base_daily_sales * multiplier
            total_festival_sales = daily_festival_sales * duration
            additional_revenue = total_festival_sales - (base_daily_sales * duration)
            
            # Category-wise breakdown
            peak_categories = festival_data.get('peak_categories', ['All Categories'])
            category_allocation = {}
            
            if peak_categories:
                allocation_per_category = 100 / len(peak_categories)
                for category in peak_categories:
                    category_sales = total_festival_sales * (allocation_per_category / 100)
                    category_allocation[category] = {
                        'forecasted_sales': format_inr(category_sales),
                        'allocation': format_percentage(allocation_per_category),
                        'units_estimate': format_quantity(int(category_sales / 800), 'pieces')  # Avg ₹800/piece
                    }
            
            result = {
                'success': True,
                'festival_name': festival_name,
                'festival_description': festival_data.get('description', ''),
                'year': year or datetime.now().year,
                'duration_days': duration,
                'sales_multiplier': f"{multiplier}x",
                'forecast': {
                    'base_daily_sales': format_inr(base_daily_sales),
                    'festival_daily_sales': format_inr(daily_festival_sales),
                    'total_festival_sales': format_inr(total_festival_sales),
                    'additional_revenue': format_inr(additional_revenue),
                    'revenue_increase': format_percentage((multiplier - 1) * 100)
                },
                'category_forecast': category_allocation,
                'peak_categories': peak_categories,
                'summary': {
                    'total_expected': format_inr(total_festival_sales),
                    'uplift': format_percentage((multiplier - 1) * 100),
                    'duration': f"{duration} days"
                }
            }
            
            # Get AI recommendations for festival planning
            if self.gemini_engine:
                query = f"""
                Provide comprehensive festival planning recommendations for {festival_name}.
                
                Festival Details:
                - Duration: {duration} days
                - Expected Sales: {format_inr(total_festival_sales)} ({multiplier}x normal)
                - Additional Revenue: {format_inr(additional_revenue)}
                - Peak Categories: {', '.join(peak_categories)}
                
                Provide detailed plan covering:
                1. **Inventory Planning**: Category-wise stock requirements with quantities and INR values
                2. **Staff Planning**: How many staff needed, their roles, schedules
                3. **Marketing Strategy**: Pre-festival, during-festival, post-festival campaigns
                4. **Pricing Strategy**: Discounts, offers, bundles for maximum revenue
                5. **Visual Merchandising**: Store layout and display recommendations
                6. **Procurement Timeline**: When to order, what quantities, from which suppliers
                7. **Logistics Planning**: Delivery schedules, warehouse management
                8. **Customer Experience**: How to manage crowds, improve satisfaction
                9. **KPIs to Track**: What metrics to monitor daily during festival
                10. **Risk Mitigation**: Contingency plans for stock-outs, overstocking, staff shortages
                11. **Post-Festival Actions**: Clearance sales, inventory management, analysis
                12. **ROI Maximization**: How to ensure maximum profitability
                
                Target: Achieve {format_inr(total_festival_sales)} sales with 30% profit margin
                """
                
                ai_plan = self.gemini_engine.plan_festival_inventory({
                    'festival': festival_name,
                    'forecast': result
                })
                result['ai_recommendations'] = ai_plan
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to forecast festival sales'
            }
    
    def plan_festival_inventory(
        self,
        festival_name: str,
        historical_data: Optional[Dict[str, Any]] = None,
        store_count: int = 11
    ) -> Dict[str, Any]:
        """
        Generate inventory plan for festival
        
        Args:
            festival_name: Name of festival
            historical_data: Optional historical sales data
            store_count: Number of stores to plan for
            
        Returns:
            Dict with inventory requirements, procurement plan, distribution
        """
        try:
            # Get festival data
            festival_data = self.major_festivals.get(festival_name)
            if not festival_data:
                for region, festivals in self.regional_festivals.items():
                    if festival_name in festivals:
                        festival_data = festivals[festival_name]
                        break
            
            if not festival_data:
                return {
                    'success': False,
                    'error': f'Festival "{festival_name}" not found'
                }
            
            # Use historical data or estimates
            if historical_data and 'last_year_sales' in historical_data:
                base_sales = historical_data['last_year_sales']
                growth_estimate = historical_data.get('growth_rate', 1.15)  # 15% YoY growth
                estimated_sales = base_sales * growth_estimate
            else:
                # Default estimates based on festival multiplier
                estimated_sales = 5000000 * festival_data.get('sales_multiplier', 2.0)  # ₹50 Lakh base
            
            multiplier = festival_data.get('sales_multiplier', 2.0)
            duration = festival_data.get('duration_days', 1)
            peak_categories = festival_data.get('peak_categories', ['All Categories'])
            
            # Calculate inventory requirements
            avg_selling_price = 800  # ₹800 average per item
            total_units_needed = int(estimated_sales / avg_selling_price)
            units_per_store = int(total_units_needed / store_count)
            
            # Category-wise distribution
            category_inventory = {}
            for category in peak_categories:
                category_percentage = 100 / len(peak_categories)
                category_units = int(total_units_needed * (category_percentage / 100))
                category_value = category_units * avg_selling_price
                
                category_inventory[category] = {
                    'total_units': format_quantity(category_units, 'pieces'),
                    'units_per_store': format_quantity(int(category_units / store_count), 'pieces'),
                    'estimated_value': format_inr(category_value),
                    'allocation': format_percentage(category_percentage)
                }
            
            # Procurement timeline
            lead_time = 15  # 15 days lead time
            festival_month = festival_data.get('typical_months', [11])[0]
            current_month = datetime.now().month
            
            procurement_timeline = []
            
            # Pre-festival procurement
            procurement_timeline.append({
                'phase': 'Pre-Festival Bulk Order',
                'timing': f'{lead_time + 7} days before festival',
                'percentage': '70%',
                'quantity': format_quantity(int(total_units_needed * 0.7), 'pieces'),
                'value': format_inr(estimated_sales * 0.7 * 0.6),  # 60% of retail value (cost)
                'action': 'Place main order with suppliers'
            })
            
            procurement_timeline.append({
                'phase': 'Top-up Order',
                'timing': f'{lead_time} days before festival',
                'percentage': '20%',
                'quantity': format_quantity(int(total_units_needed * 0.2), 'pieces'),
                'value': format_inr(estimated_sales * 0.2 * 0.6),
                'action': 'Additional stock for fast-moving items'
            })
            
            procurement_timeline.append({
                'phase': 'Last Minute Stock',
                'timing': '3-5 days before festival',
                'percentage': '10%',
                'quantity': format_quantity(int(total_units_needed * 0.1), 'pieces'),
                'value': format_inr(estimated_sales * 0.1 * 0.6),
                'action': 'Quick replenishment for trending items'
            })
            
            result = {
                'success': True,
                'festival_name': festival_name,
                'store_count': store_count,
                'estimated_sales': format_inr(estimated_sales),
                'inventory_requirements': {
                    'total_units': format_quantity(total_units_needed, 'pieces'),
                    'units_per_store': format_quantity(units_per_store, 'pieces'),
                    'avg_selling_price': format_inr(avg_selling_price),
                    'total_inventory_value': format_inr(estimated_sales * 0.6)  # Cost is ~60% of retail
                },
                'category_wise_inventory': category_inventory,
                'procurement_timeline': procurement_timeline,
                'distribution_plan': {
                    'method': 'Proportional to store size and footfall',
                    'high_footfall_stores': f'{int(units_per_store * 1.3)} pieces each',
                    'medium_footfall_stores': f'{units_per_store} pieces each',
                    'low_footfall_stores': f'{int(units_per_store * 0.7)} pieces each'
                },
                'summary': {
                    'total_investment': format_inr(estimated_sales * 0.6),
                    'expected_revenue': format_inr(estimated_sales),
                    'expected_margin': '40%'
                }
            }
            
            # Get AI optimization for inventory plan
            if self.gemini_engine:
                query = f"""
                Optimize inventory plan for {festival_name} across {store_count} stores.
                
                Inventory Plan Summary:
                - Total Units: {format_quantity(total_units_needed, 'pieces')}
                - Total Investment: {format_inr(estimated_sales * 0.6)}
                - Expected Revenue: {format_inr(estimated_sales)}
                - Categories: {', '.join(peak_categories)}
                
                Provide optimization on:
                1. **Category Mix Refinement**: Adjust allocations based on trends
                2. **Store-wise Distribution**: Specific quantities for each store based on performance
                3. **Procurement Strategy**: Best suppliers, negotiation tips, payment terms
                4. **Inventory Placement**: Where to store excess, how to manage warehouse
                5. **Replenishment Strategy**: How to track and reorder during festival
                6. **Risk Management**: What if stock doesn't sell? Clearance strategies
                7. **Cash Flow Management**: Payment schedules, working capital needs
                8. **Quality Checks**: What to verify before accepting deliveries
                9. **Packaging & Display**: How to present products attractively
                10. **Inter-Store Transfers**: Plan for moving stock between stores during festival
                """
                
                ai_optimization = self.gemini_engine.get_insights(
                    query=query,
                    context_data=result,
                    analytics_type='inventory_planning'
                )
                result['ai_optimization'] = ai_optimization
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to plan festival inventory'
            }
    
    def get_upcoming_festivals(
        self,
        region: Optional[str] = None,
        months_ahead: int = 6
    ) -> Dict[str, Any]:
        """
        Get upcoming festivals for planning
        
        Args:
            region: Optional region for regional festivals
            months_ahead: How many months ahead to look
            
        Returns:
            Dict with upcoming festivals, dates, planning deadlines
        """
        try:
            current_date = datetime.now()
            end_date = current_date + timedelta(days=30 * months_ahead)
            
            upcoming = []
            
            # Add major festivals
            for festival_name, fest_data in self.major_festivals.items():
                typical_months = fest_data.get('typical_months', [])
                
                for month in typical_months:
                    if current_date.month <= month <= end_date.month or \
                       (end_date.year > current_date.year and month <= end_date.month):
                        
                        # Estimate date (middle of typical month)
                        year = current_date.year if month >= current_date.month else current_date.year + 1
                        estimated_date = datetime(year, month, 15)
                        
                        days_until = (estimated_date - current_date).days
                        
                        if days_until >= 0 and days_until <= (30 * months_ahead):
                            planning_deadline = estimated_date - timedelta(days=30)
                            
                            upcoming.append({
                                'festival_name': festival_name,
                                'type': 'Major Festival',
                                'estimated_date': estimated_date.strftime('%b %Y'),
                                'days_until': days_until,
                                'duration': fest_data.get('duration_days', 1),
                                'sales_multiplier': fest_data.get('sales_multiplier', 1.0),
                                'planning_deadline': planning_deadline.strftime('%d-%b-%Y'),
                                'planning_status': 'URGENT' if days_until < 30 else ('PLAN NOW' if days_until < 60 else 'UPCOMING'),
                                'description': fest_data.get('description', '')
                            })
            
            # Add regional festivals if region specified
            if region and region in self.regional_festivals:
                for festival_name, fest_data in self.regional_festivals[region].items():
                    month = fest_data.get('month')
                    
                    if month and current_date.month <= month <= end_date.month:
                        year = current_date.year if month >= current_date.month else current_date.year + 1
                        estimated_date = datetime(year, month, 15)
                        days_until = (estimated_date - current_date).days
                        
                        if days_until >= 0:
                            planning_deadline = estimated_date - timedelta(days=20)
                            
                            upcoming.append({
                                'festival_name': festival_name,
                                'type': f'Regional Festival ({region})',
                                'estimated_date': estimated_date.strftime('%b %Y'),
                                'days_until': days_until,
                                'duration': fest_data.get('duration_days', 1),
                                'sales_multiplier': fest_data.get('multiplier', 1.0),
                                'planning_deadline': planning_deadline.strftime('%d-%b-%Y'),
                                'planning_status': 'URGENT' if days_until < 20 else ('PLAN NOW' if days_until < 40 else 'UPCOMING'),
                                'description': f'Regional festival in {region}'
                            })
            
            # Sort by days until festival
            upcoming.sort(key=lambda x: x['days_until'])
            
            result = {
                'success': True,
                'query_date': current_date.strftime('%d-%b-%Y'),
                'lookahead_months': months_ahead,
                'region': region or 'All India',
                'festivals': upcoming,
                'count': len(upcoming),
                'urgent_count': len([f for f in upcoming if f['planning_status'] == 'URGENT']),
                'summary': {
                    'next_major_festival': upcoming[0]['festival_name'] if upcoming else 'None in period',
                    'total_festivals': len(upcoming),
                    'require_immediate_planning': len([f for f in upcoming if f['planning_status'] == 'URGENT'])
                }
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to get upcoming festivals'
            }


