"""
Inventory Planning Module for V-Mart Retail Intelligence
Provides forecasting, IST planning, and procurement recommendations
"""

from typing import Dict, List, Optional, Any
from .formatters import format_inr, format_quantity, format_percentage, format_growth
from datetime import datetime, timedelta


class InventoryPlanner:
    """AI-powered inventory planning and optimization"""
    
    def __init__(self, gemini_engine=None):
        """
        Initialize InventoryPlanner
        
        Args:
            gemini_engine: GeminiRetailInsights instance for AI-powered recommendations
        """
        self.gemini_engine = gemini_engine
    
    def forecast_inventory_needs(
        self,
        sales_forecast: Dict[str, Any],
        current_stock: Dict[str, int],
        lead_time_days: int = 7
    ) -> Dict[str, Any]:
        """
        Forecast inventory requirements based on sales forecast
        
        Args:
            sales_forecast: Sales forecast by category/product
            current_stock: Current stock levels by category/product
            lead_time_days: Supplier lead time in days
            
        Returns:
            Dict with inventory forecast, reorder points, stock-out risks
        """
        try:
            # Calculate inventory requirements
            forecast_period_days = sales_forecast.get('forecast_days', 30)
            safety_stock_multiplier = 1.2  # 20% buffer
            
            inventory_needs = {}
            stock_out_risks = []
            reorder_points = {}
            
            for category, forecast_qty in sales_forecast.get('forecasted_sales', {}).items():
                current_qty = current_stock.get(category, 0)
                daily_demand = forecast_qty / forecast_period_days
                
                # Calculate requirements
                lead_time_demand = daily_demand * lead_time_days
                safety_stock = daily_demand * 3  # 3 days safety
                reorder_point = lead_time_demand + safety_stock
                required_stock = (daily_demand * forecast_period_days * safety_stock_multiplier)
                
                # Check stock-out risk
                days_of_stock = current_qty / daily_demand if daily_demand > 0 else 999
                risk_level = "HIGH" if days_of_stock < lead_time_days else ("MEDIUM" if days_of_stock < (lead_time_days + 7) else "LOW")
                
                inventory_needs[category] = {
                    'current_stock': format_quantity(current_qty, 'pieces'),
                    'daily_demand': format_quantity(daily_demand, 'pieces/day', 1),
                    'required_for_period': format_quantity(required_stock, 'pieces'),
                    'shortage': format_quantity(max(0, required_stock - current_qty), 'pieces'),
                    'days_of_stock_remaining': f"{days_of_stock:.1f} days",
                    'reorder_point': format_quantity(reorder_point, 'pieces'),
                    'risk_level': risk_level
                }
                
                reorder_points[category] = reorder_point
                
                if risk_level in ['HIGH', 'MEDIUM']:
                    stock_out_risks.append({
                        'category': category,
                        'risk_level': risk_level,
                        'days_remaining': f"{days_of_stock:.1f}",
                        'action_required': 'URGENT ORDER' if risk_level == 'HIGH' else 'PLAN ORDER'
                    })
            
            result = {
                'success': True,
                'forecast_period_days': forecast_period_days,
                'lead_time_days': lead_time_days,
                'inventory_needs': inventory_needs,
                'stock_out_risks': stock_out_risks,
                'reorder_points': reorder_points,
                'summary': {
                    'total_categories': len(inventory_needs),
                    'high_risk_categories': len([r for r in stock_out_risks if r['risk_level'] == 'HIGH']),
                    'medium_risk_categories': len([r for r in stock_out_risks if r['risk_level'] == 'MEDIUM'])
                }
            }
            
            # Get AI recommendations
            if self.gemini_engine:
                ai_insights = self.gemini_engine.forecast_inventory(result)
                result['ai_recommendations'] = ai_insights
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to forecast inventory needs'
            }
    
    def plan_inter_store_transfer(
        self,
        store_stocks: Dict[str, Dict[str, int]],
        demand_forecast: Optional[Dict[str, Dict[str, int]]] = None
    ) -> Dict[str, Any]:
        """
        Recommend inter-store transfers to optimize stock distribution
        
        Args:
            store_stocks: Stock levels by store and category
            demand_forecast: Optional demand forecast by store
            
        Returns:
            Dict with recommended transfers, quantities, priorities
        """
        try:
            # Calculate average stock per category across all stores
            category_totals = {}
            store_count = len(store_stocks)
            
            for store_id, stocks in store_stocks.items():
                for category, qty in stocks.items():
                    if category not in category_totals:
                        category_totals[category] = []
                    category_totals[category].append((store_id, qty))
            
            # Calculate averages and identify imbalances
            transfer_recommendations = []
            
            for category, store_qtys in category_totals.items():
                total_qty = sum(qty for _, qty in store_qtys)
                avg_qty = total_qty / store_count
                
                # Identify surplus and deficit stores
                surplus_stores = [(sid, qty) for sid, qty in store_qtys if qty > avg_qty * 1.3]
                deficit_stores = [(sid, qty) for sid, qty in store_qtys if qty < avg_qty * 0.7]
                
                # Create transfer recommendations
                for surplus_store, surplus_qty in surplus_stores:
                    for deficit_store, deficit_qty in deficit_stores:
                        transfer_qty = min(
                            surplus_qty - avg_qty,
                            avg_qty - deficit_qty
                        )
                        
                        if transfer_qty > 10:  # Minimum transfer quantity
                            # Calculate demand if available
                            demand_ratio = 1.0
                            if demand_forecast:
                                surplus_demand = demand_forecast.get(surplus_store, {}).get(category, avg_qty)
                                deficit_demand = demand_forecast.get(deficit_store, {}).get(category, avg_qty)
                                demand_ratio = deficit_demand / surplus_demand if surplus_demand > 0 else 1.0
                            
                            priority = 'HIGH' if demand_ratio > 1.5 else ('MEDIUM' if demand_ratio > 1.2 else 'LOW')
                            
                            transfer_recommendations.append({
                                'from_store': surplus_store,
                                'to_store': deficit_store,
                                'category': category,
                                'quantity': format_quantity(int(transfer_qty), 'pieces'),
                                'priority': priority,
                                'reason': f'Balance stock - From {surplus_qty} to {deficit_qty} (avg: {int(avg_qty)})',
                                'demand_ratio': f"{demand_ratio:.2f}x"
                            })
            
            # Sort by priority
            priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
            transfer_recommendations.sort(key=lambda x: priority_order[x['priority']])
            
            result = {
                'success': True,
                'total_transfers_recommended': len(transfer_recommendations),
                'transfers_by_priority': {
                    'HIGH': len([t for t in transfer_recommendations if t['priority'] == 'HIGH']),
                    'MEDIUM': len([t for t in transfer_recommendations if t['priority'] == 'MEDIUM']),
                    'LOW': len([t for t in transfer_recommendations if t['priority'] == 'LOW'])
                },
                'recommended_transfers': transfer_recommendations[:20],  # Top 20
                'category_summary': {
                    cat: {
                        'total_stock': format_quantity(sum(qty for _, qty in qtys), 'pieces'),
                        'avg_per_store': format_quantity(sum(qty for _, qty in qtys) / store_count, 'pieces'),
                        'stores_with_stock': len(qtys)
                    }
                    for cat, qtys in category_totals.items()
                }
            }
            
            # Get AI optimization recommendations
            if self.gemini_engine:
                ai_insights = self.gemini_engine.optimize_logistics({
                    'operation': 'inter_store_transfer',
                    'transfers': transfer_recommendations[:10],
                    'store_count': store_count
                })
                result['ai_optimization'] = ai_insights
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to plan inter-store transfers'
            }
    
    def recommend_procurement(
        self,
        inventory_data: Dict[str, Any],
        lead_time_days: int = 7,
        safety_stock_days: int = 3
    ) -> Dict[str, Any]:
        """
        Generate procurement recommendations with quantities and INR amounts
        
        Args:
            inventory_data: Current inventory, sales velocity, supplier info
            lead_time_days: Supplier lead time
            safety_stock_days: Safety stock buffer
            
        Returns:
            Dict with procurement recommendations, quantities, INR amounts
        """
        try:
            current_stock = inventory_data.get('current_stock', {})
            daily_sales = inventory_data.get('daily_sales_velocity', {})
            unit_costs = inventory_data.get('unit_cost_inr', {})
            min_order_qty = inventory_data.get('min_order_quantity', {})
            
            procurement_orders = []
            total_procurement_value = 0
            
            for category, current_qty in current_stock.items():
                daily_demand = daily_sales.get(category, 0)
                unit_cost = unit_costs.get(category, 0)
                min_qty = min_order_qty.get(category, 100)
                
                if daily_demand == 0:
                    continue
                
                # Calculate requirements
                days_of_stock = current_qty / daily_demand
                safety_stock = daily_demand * safety_stock_days
                lead_time_stock = daily_demand * lead_time_days
                reorder_point = safety_stock + lead_time_stock
                
                # Economic Order Quantity (simplified)
                monthly_demand = daily_demand * 30
                eoq = max(min_qty, int(monthly_demand * 0.5))  # 15 days worth
                
                # Determine if order needed
                if current_qty <= reorder_point:
                    order_qty = max(eoq, int(reorder_point - current_qty + safety_stock))
                    order_value = order_qty * unit_cost
                    total_procurement_value += order_value
                    
                    urgency = 'CRITICAL' if days_of_stock < lead_time_days else (
                        'URGENT' if days_of_stock < (lead_time_days + 3) else 'PLANNED'
                    )
                    
                    procurement_orders.append({
                        'category': category,
                        'order_quantity': format_quantity(order_qty, 'pieces'),
                        'order_value': format_inr(order_value),
                        'unit_cost': format_inr(unit_cost),
                        'current_stock': format_quantity(current_qty, 'pieces'),
                        'days_remaining': f"{days_of_stock:.1f} days",
                        'urgency': urgency,
                        'expected_delivery': (datetime.now() + timedelta(days=lead_time_days)).strftime('%d-%b-%Y'),
                        'reason': f"Stock below reorder point ({format_quantity(reorder_point, 'pieces')})"
                    })
            
            # Sort by urgency
            urgency_order = {'CRITICAL': 0, 'URGENT': 1, 'PLANNED': 2}
            procurement_orders.sort(key=lambda x: urgency_order[x['urgency']])
            
            result = {
                'success': True,
                'total_orders': len(procurement_orders),
                'total_procurement_value': format_inr(total_procurement_value),
                'orders_by_urgency': {
                    'CRITICAL': len([o for o in procurement_orders if o['urgency'] == 'CRITICAL']),
                    'URGENT': len([o for o in procurement_orders if o['urgency'] == 'URGENT']),
                    'PLANNED': len([o for o in procurement_orders if o['urgency'] == 'PLANNED'])
                },
                'procurement_orders': procurement_orders,
                'lead_time_days': lead_time_days,
                'safety_stock_days': safety_stock_days,
                'recommendations': []
            }
            
            # Add AI-powered procurement insights
            if self.gemini_engine:
                ai_insights = self.gemini_engine.get_insights(
                    query="Analyze procurement orders and provide optimization recommendations",
                    context_data=result,
                    analytics_type='procurement'
                )
                result['ai_recommendations'] = ai_insights
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to generate procurement recommendations'
            }
