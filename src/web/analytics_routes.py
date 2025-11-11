"""
Analytics API Routes for V-Mart Store Intelligence

Provides REST endpoints for sales analytics, inventory optimization,
competition analysis, demand forecasting, and business insights.
"""

from datetime import date, timedelta

from analytics.engine import AnalyticsEngine
from flask import Blueprint, jsonify, request

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

# Initialize analytics engine
analytics_engine = AnalyticsEngine()


@analytics_bp.route("/sales-trends/<store_id>", methods=["GET"])
def get_sales_trends(store_id: str):
    """
    Get sales trend analysis for a store

    Query params:
        days: Number of days to analyze (default: 30)
    """
    try:
        days = int(request.args.get("days", 30))

        trend = analytics_engine.analyze_sales_trends(store_id, days)

        return jsonify(
            {
                "success": True,
                "store_id": store_id,
                "analysis_period_days": days,
                "trend": trend.to_dict(),
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@analytics_bp.route("/weather-impact/<store_id>", methods=["GET"])
def get_weather_impact(store_id: str):
    """
    Analyze weather impact on sales for a store

    Query params:
        days: Number of days to analyze (default: 30)
    """
    try:
        days = int(request.args.get("days", 30))

        impact = analytics_engine.analyze_weather_impact(store_id, days)

        return jsonify(
            {
                "success": True,
                "store_id": store_id,
                "analysis_period_days": days,
                "weather_impact": impact.to_dict(),
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@analytics_bp.route("/competition-impact/<store_id>", methods=["GET"])
def get_competition_impact(store_id: str):
    """
    Analyze competition impact on store performance

    Query params:
        radius: Search radius in km (default: 10.0)
    """
    try:
        radius = float(request.args.get("radius", 10.0))

        impact = analytics_engine.analyze_competition_impact(store_id, radius)

        return jsonify(
            {
                "success": True,
                "store_id": store_id,
                "search_radius_km": radius,
                "competition_impact": impact.to_dict(),
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@analytics_bp.route("/inventory-recommendations/<store_id>", methods=["GET"])
def get_inventory_recommendations(store_id: str):
    """
    Get inventory optimization recommendations for a store
    """
    try:
        recommendations = analytics_engine.generate_inventory_recommendations(store_id)

        return jsonify(
            {
                "success": True,
                "store_id": store_id,
                "recommendation_count": len(recommendations),
                "recommendations": [rec.to_dict() for rec in recommendations],
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@analytics_bp.route("/demand-forecast/<store_id>/<category>", methods=["GET"])
def get_demand_forecast(store_id: str, category: str):
    """
    Get demand forecast for a specific category

    Query params:
        days: Number of days to forecast (default: 7)
    """
    try:
        days_ahead = int(request.args.get("days", 7))

        forecasts = analytics_engine.forecast_demand(store_id, category, days_ahead)

        return jsonify(
            {
                "success": True,
                "store_id": store_id,
                "category": category,
                "forecast_days": days_ahead,
                "forecasts": [f.to_dict() for f in forecasts],
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@analytics_bp.route("/insights/<store_id>", methods=["GET"])
def get_insights(store_id: str):
    """
    Get all business insights for a store

    Query params:
        priority: Filter by priority (critical, high, medium, low)
        category: Filter by category (sales, inventory, competition, weather, operations, customer)
    """
    try:
        insights = analytics_engine.generate_insights(store_id)

        # Apply filters
        priority_filter = request.args.get("priority")
        category_filter = request.args.get("category")

        if priority_filter:
            insights = [
                i for i in insights if i.priority.value == priority_filter.lower()
            ]

        if category_filter:
            insights = [
                i for i in insights if i.category.value == category_filter.lower()
            ]

        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        insights.sort(key=lambda x: priority_order.get(x.priority.value, 4))

        return jsonify(
            {
                "success": True,
                "store_id": store_id,
                "insight_count": len(insights),
                "insights": [i.to_dict() for i in insights],
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@analytics_bp.route("/performance-metrics/<store_id>", methods=["GET"])
def get_performance_metrics(store_id: str):
    """
    Get comprehensive performance metrics for a store

    Query params:
        days: Number of days to analyze (default: 30)
    """
    try:
        days = int(request.args.get("days", 30))

        metrics = analytics_engine.get_performance_metrics(store_id, days)

        return jsonify(
            {
                "success": True,
                "store_id": store_id,
                "analysis_period_days": days,
                "metrics": metrics.to_dict(),
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@analytics_bp.route("/dashboard/<store_id>", methods=["GET"])
def get_analytics_dashboard(store_id: str):
    """
    Get comprehensive analytics dashboard with all key metrics and insights
    """
    try:
        days = int(request.args.get("days", 30))

        # Gather all analytics
        sales_trend = analytics_engine.analyze_sales_trends(store_id, days)
        weather_impact = analytics_engine.analyze_weather_impact(store_id, days)
        competition = analytics_engine.analyze_competition_impact(store_id)
        inventory_recs = analytics_engine.generate_inventory_recommendations(store_id)
        insights = analytics_engine.generate_insights(store_id)
        metrics = analytics_engine.get_performance_metrics(store_id, days)

        # Categorize inventory recommendations by urgency
        critical_inventory = [
            r for r in inventory_recs if r.reorder_urgency.value == "critical"
        ]
        high_inventory = [
            r for r in inventory_recs if r.reorder_urgency.value == "high"
        ]

        # Categorize insights by priority
        critical_insights = [i for i in insights if i.priority.value == "critical"]
        high_insights = [i for i in insights if i.priority.value == "high"]

        return jsonify(
            {
                "success": True,
                "store_id": store_id,
                "analysis_period_days": days,
                "generated_at": date.today().isoformat(),
                # Summary metrics
                "performance_summary": metrics.to_dict(),
                # Sales analysis
                "sales": {
                    "trend": sales_trend.to_dict(),
                    "total_revenue": sales_trend.total_sales,
                    "growth_rate": sales_trend.sales_growth,
                    "peak_day": sales_trend.peak_sales_day,
                    "peak_period": sales_trend.peak_sales_period,
                },
                # Weather impact
                "weather": {
                    "impact": weather_impact.to_dict(),
                    "current_condition": weather_impact.weather_condition,
                    "sales_variance": weather_impact.sales_variance,
                },
                # Competition analysis
                "competition": {
                    "impact": competition.to_dict(),
                    "competitor_count": competition.competitor_count,
                    "market_share": competition.estimated_market_share,
                    "nearest_competitor_km": competition.nearest_competitor_distance,
                },
                # Inventory status
                "inventory": {
                    "total_recommendations": len(inventory_recs),
                    "critical_items": len(critical_inventory),
                    "high_priority_items": len(high_inventory),
                    "recommendations": [r.to_dict() for r in inventory_recs],
                },
                # Actionable insights
                "insights": {
                    "total_count": len(insights),
                    "critical_count": len(critical_insights),
                    "high_priority_count": len(high_insights),
                    "all_insights": [i.to_dict() for i in insights],
                    "top_actions": [
                        action
                        for insight in critical_insights + high_insights
                        for action in insight.recommended_actions
                    ][:10],  # Top 10 recommended actions
                },
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@analytics_bp.route("/all-stores/summary", methods=["GET"])
def get_all_stores_summary():
    """
    Get analytics summary for all V-Mart stores
    """
    try:
        from stores.database import StoreDatabase

        store_db = StoreDatabase()

        all_stores = store_db.get_all_vmart_stores()

        summaries = []
        for store in all_stores:
            try:
                metrics = analytics_engine.get_performance_metrics(
                    store.store_id, days=30
                )
                insights = analytics_engine.generate_insights(store.store_id)

                critical_insights = sum(
                    1 for i in insights if i.priority.value == "critical"
                )

                summaries.append(
                    {
                        "store_id": store.store_id,
                        "store_name": store.store_name,
                        "city": store.location.city,
                        "revenue": metrics.total_revenue,
                        "revenue_growth": metrics.revenue_growth,
                        "market_share": metrics.market_share_estimate,
                        "competitive_position": metrics.competitive_position,
                        "critical_insights": critical_insights,
                        "stockout_rate": metrics.stockout_rate,
                    }
                )
            except Exception as e:
                print(f"Error analyzing store {store.store_id}: {e}")
                continue

        # Sort by revenue
        summaries.sort(key=lambda x: x["revenue"], reverse=True)

        # Calculate network-wide metrics
        total_revenue = sum(s["revenue"] for s in summaries)
        avg_growth = (
            sum(s["revenue_growth"] for s in summaries) / len(summaries)
            if summaries
            else 0
        )
        total_critical_insights = sum(s["critical_insights"] for s in summaries)

        return jsonify(
            {
                "success": True,
                "store_count": len(summaries),
                "network_metrics": {
                    "total_revenue": total_revenue,
                    "average_growth_rate": avg_growth,
                    "total_critical_insights": total_critical_insights,
                    "analysis_date": date.today().isoformat(),
                },
                "stores": summaries,
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@analytics_bp.route("/recommendations/consolidated/<store_id>", methods=["GET"])
def get_consolidated_recommendations(store_id: str):
    """
    Get consolidated, prioritized recommendations across all categories
    """
    try:
        insights = analytics_engine.generate_insights(store_id)
        inventory_recs = analytics_engine.generate_inventory_recommendations(store_id)
        competition = analytics_engine.analyze_competition_impact(store_id)

        # Consolidate all recommendations
        all_recommendations = []

        # Add insight-based recommendations
        for insight in insights:
            for action in insight.recommended_actions:
                all_recommendations.append(
                    {
                        "category": insight.category.value,
                        "priority": insight.priority.value,
                        "action": action,
                        "rationale": insight.description,
                        "expected_impact": insight.impact,
                        "confidence": insight.confidence_score,
                    }
                )

        # Add inventory recommendations
        for rec in inventory_recs:
            if rec.reorder_urgency.value in ["critical", "high"]:
                all_recommendations.append(
                    {
                        "category": "inventory",
                        "priority": rec.reorder_urgency.value,
                        "action": f"Reorder {rec.reorder_quantity} units of {rec.category}",
                        "rationale": rec.reasoning,
                        "expected_impact": f"Reduce stockout risk from {rec.estimated_stockout_risk:.1f}%",
                        "confidence": 85.0,
                    }
                )

        # Add competition strategies
        for strategy in competition.recommended_strategies[:3]:  # Top 3
            all_recommendations.append(
                {
                    "category": "competition",
                    "priority": "medium",
                    "action": strategy,
                    "rationale": f"Strategic response to {competition.competitor_count} nearby competitors",
                    "expected_impact": f"Improve market share (currently {competition.estimated_market_share:.1f}%)",
                    "confidence": 70.0,
                }
            )

        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        all_recommendations.sort(key=lambda x: priority_order.get(x["priority"], 4))

        return jsonify(
            {
                "success": True,
                "store_id": store_id,
                "total_recommendations": len(all_recommendations),
                "critical_count": sum(
                    1 for r in all_recommendations if r["priority"] == "critical"
                ),
                "high_priority_count": sum(
                    1 for r in all_recommendations if r["priority"] == "high"
                ),
                "recommendations": all_recommendations,
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@analytics_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for analytics service"""
    return jsonify(
        {
            "success": True,
            "service": "V-Mart Analytics Engine",
            "status": "operational",
            "version": "1.0.0",
        }
    )


@analytics_bp.route("/dashboard-ui/<store_id>", methods=["GET"])
def analytics_dashboard_ui(store_id: str):
    """
    Interactive analytics dashboard with charts and visualizations
    """
    from flask import render_template_string

    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>V-Mart Analytics Dashboard - {{ store_id }}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        
        .dashboard-container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .dashboard-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .dashboard-header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .store-info {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }
        
        .metric-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        
        .metric-label {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }
        
        .metric-change {
            font-size: 0.9em;
            margin-top: 10px;
        }
        
        .metric-change.positive {
            color: #28a745;
        }
        
        .metric-change.negative {
            color: #dc3545;
        }
        
        .charts-section {
            padding: 30px;
        }
        
        .chart-container {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .chart-title {
            font-size: 1.5em;
            margin-bottom: 20px;
            color: #333;
        }
        
        .insights-section {
            padding: 30px;
            background: #f8f9fa;
        }
        
        .insights-header {
            font-size: 2em;
            margin-bottom: 20px;
            color: #333;
        }
        
        .insight-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 5px solid #667eea;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .insight-card.critical {
            border-left-color: #dc3545;
        }
        
        .insight-card.high {
            border-left-color: #fd7e14;
        }
        
        .insight-card.medium {
            border-left-color: #ffc107;
        }
        
        .insight-title {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        
        .insight-description {
            color: #666;
            margin-bottom: 15px;
            line-height: 1.6;
        }
        
        .insight-actions {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
        }
        
        .insight-actions h4 {
            margin-bottom: 10px;
            color: #667eea;
        }
        
        .action-item {
            padding: 8px 0;
            border-bottom: 1px solid #dee2e6;
        }
        
        .action-item:last-child {
            border-bottom: none;
        }
        
        .priority-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        
        .priority-badge.critical {
            background: #dc3545;
            color: white;
        }
        
        .priority-badge.high {
            background: #fd7e14;
            color: white;
        }
        
        .priority-badge.medium {
            background: #ffc107;
            color: #333;
        }
        
        .priority-badge.low {
            background: #28a745;
            color: white;
        }
        
        .loading {
            text-align: center;
            padding: 50px;
            font-size: 1.5em;
            color: #666;
        }
        
        .error {
            text-align: center;
            padding: 50px;
            font-size: 1.2em;
            color: #dc3545;
        }
        
        .refresh-button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 1em;
            cursor: pointer;
            margin: 20px auto;
            display: block;
            transition: background 0.3s;
        }
        
        .refresh-button:hover {
            background: #5568d3;
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="dashboard-header">
            <h1>📊 V-Mart Analytics Dashboard</h1>
            <div class="store-info">Store: <span id="storeName">Loading...</span> | <span id="storeCity">...</span></div>
            <div class="store-info">Analysis Period: Last 30 Days | Updated: <span id="updateTime"></span></div>
        </div>
        
        <div id="loadingIndicator" class="loading">
            Loading analytics data...
        </div>
        
        <div id="errorMessage" class="error" style="display: none;">
            Error loading data. Please try again.
        </div>
        
        <div id="dashboardContent" style="display: none;">
            <!-- Key Metrics -->
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Total Revenue</div>
                    <div class="metric-value" id="totalRevenue">₹0</div>
                    <div class="metric-change" id="revenueChange"></div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Market Share</div>
                    <div class="metric-value" id="marketShare">0%</div>
                    <div class="metric-change" id="competitivePosition"></div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Competitors Nearby</div>
                    <div class="metric-value" id="competitorCount">0</div>
                    <div class="metric-change" id="nearestCompetitor"></div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Critical Insights</div>
                    <div class="metric-value" id="criticalInsights">0</div>
                    <div class="metric-change" id="totalInsights"></div>
                </div>
            </div>
            
            <!-- Charts Section -->
            <div class="charts-section">
                <div class="chart-container">
                    <div class="chart-title">Sales Trend & Performance</div>
                    <canvas id="salesChart"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">Category Performance</div>
                    <canvas id="categoryChart"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">Inventory Status by Category</div>
                    <canvas id="inventoryChart"></canvas>
                </div>
            </div>
            
            <!-- Insights Section -->
            <div class="insights-section">
                <h2 class="insights-header">🎯 Actionable Insights & Recommendations</h2>
                <div id="insightsContainer"></div>
            </div>
            
            <button class="refresh-button" onclick="loadDashboard()">🔄 Refresh Data</button>
        </div>
    </div>
    
    <script>
        const storeId = '{{ store_id }}';
        let salesChart, categoryChart, inventoryChart;
        
        async function loadDashboard() {
            try {
                document.getElementById('loadingIndicator').style.display = 'block';
                document.getElementById('dashboardContent').style.display = 'none';
                document.getElementById('errorMessage').style.display = 'none';
                
                // Fetch dashboard data
                const response = await fetch(`/analytics/dashboard/${storeId}`);
                const data = await response.json();
                
                if (!data.success) {
                    throw new Error(data.error || 'Failed to load data');
                }
                
                // Update store info
                const storeResponse = await fetch(`/stores/vmart/${storeId}`);
                const storeData = await storeResponse.json();
                if (storeData.success) {
                    document.getElementById('storeName').textContent = storeData.store.store_name;
                    document.getElementById('storeCity').textContent = storeData.store.location.city;
                }
                
                document.getElementById('updateTime').textContent = new Date().toLocaleTimeString();
                
                // Update metrics
                updateMetrics(data);
                
                // Create charts
                createCharts(data);
                
                // Display insights
                displayInsights(data.insights.all_insights);
                
                // Show dashboard
                document.getElementById('loadingIndicator').style.display = 'none';
                document.getElementById('dashboardContent').style.display = 'block';
                
            } catch (error) {
                console.error('Error loading dashboard:', error);
                document.getElementById('loadingIndicator').style.display = 'none';
                document.getElementById('errorMessage').style.display = 'block';
                document.getElementById('errorMessage').textContent = 'Error: ' + error.message;
            }
        }
        
        function updateMetrics(data) {
            const metrics = data.performance_summary;
            const competition = data.competition;
            const insights = data.insights;
            
            // Revenue
            document.getElementById('totalRevenue').textContent = 
                '₹' + (metrics.sales_metrics.total_revenue / 100000).toFixed(2) + 'L';
            const revenueChange = metrics.sales_metrics.revenue_growth;
            document.getElementById('revenueChange').textContent = 
                (revenueChange >= 0 ? '↑' : '↓') + ' ' + Math.abs(revenueChange).toFixed(1) + '% vs last period';
            document.getElementById('revenueChange').className = 
                'metric-change ' + (revenueChange >= 0 ? 'positive' : 'negative');
            
            // Market Share
            document.getElementById('marketShare').textContent = 
                metrics.competition_metrics.market_share_estimate.toFixed(1) + '%';
            document.getElementById('competitivePosition').textContent = 
                'Position: ' + metrics.competition_metrics.competitive_position;
            
            // Competitors
            document.getElementById('competitorCount').textContent = competition.competitor_count;
            document.getElementById('nearestCompetitor').textContent = 
                'Nearest: ' + competition.nearest_competitor_km.toFixed(1) + ' km away';
            
            // Insights
            document.getElementById('criticalInsights').textContent = insights.critical_count;
            document.getElementById('totalInsights').textContent = 
                insights.total_count + ' total insights';
        }
        
        function createCharts(data) {
            const sales = data.sales;
            const inventory = data.inventory;
            
            // Destroy existing charts
            if (salesChart) salesChart.destroy();
            if (categoryChart) categoryChart.destroy();
            if (inventoryChart) inventoryChart.destroy();
            
            // Sales Trend Chart
            const salesCtx = document.getElementById('salesChart').getContext('2d');
            salesChart = new Chart(salesCtx, {
                type: 'line',
                data: {
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                    datasets: [{
                        label: 'Revenue (₹ Lakhs)',
                        data: generateWeeklySales(sales.total_revenue),
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: true },
                        title: { display: false }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
            
            // Category Performance Chart
            const trending = sales.trend.trending_categories || [];
            const underperforming = sales.trend.underperforming_categories || [];
            
            const categoryCtx = document.getElementById('categoryChart').getContext('2d');
            categoryChart = new Chart(categoryCtx, {
                type: 'bar',
                data: {
                    labels: [...trending.map(c => c.category), ...underperforming.map(c => c.category)],
                    datasets: [{
                        label: 'Growth %',
                        data: [...trending.map(c => c.growth), ...underperforming.map(c => c.decline)],
                        backgroundColor: function(context) {
                            const value = context.parsed.y;
                            return value >= 0 ? 'rgba(40, 167, 69, 0.7)' : 'rgba(220, 53, 69, 0.7)';
                        },
                        borderColor: function(context) {
                            const value = context.parsed.y;
                            return value >= 0 ? 'rgb(40, 167, 69)' : 'rgb(220, 53, 69)';
                        },
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            }
                        }
                    }
                }
            });
            
            // Inventory Status Chart
            const inventoryRecs = inventory.recommendations || [];
            const invCtx = document.getElementById('inventoryChart').getContext('2d');
            inventoryChart = new Chart(invCtx, {
                type: 'doughnut',
                data: {
                    labels: inventoryRecs.map(r => r.category),
                    datasets: [{
                        label: 'Stock Level',
                        data: inventoryRecs.map(r => r.current_stock),
                        backgroundColor: [
                            '#667eea', '#764ba2', '#f093fb', '#4facfe',
                            '#43e97b', '#fa709a'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'right' }
                    }
                }
            });
        }
        
        function generateWeeklySales(totalRevenue) {
            // Simple simulation of weekly distribution
            const weekly = totalRevenue / 4;
            const variance = 0.15;
            return [
                (weekly * (1 - variance)) / 100000,
                (weekly * (1 + variance)) / 100000,
                (weekly * (1 - variance * 0.5)) / 100000,
                (weekly * (1 + variance * 0.8)) / 100000
            ];
        }
        
        function displayInsights(insights) {
            const container = document.getElementById('insightsContainer');
            container.innerHTML = '';
            
            if (!insights || insights.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #666;">No insights available at this time.</p>';
                return;
            }
            
            insights.forEach(insight => {
                const card = document.createElement('div');
                card.className = 'insight-card ' + insight.priority;
                
                card.innerHTML = `
                    <div class="priority-badge ${insight.priority}">${insight.priority}</div>
                    <div class="insight-title">${insight.title}</div>
                    <div class="insight-description">${insight.description}</div>
                    <div style="margin: 10px 0; color: #667eea;"><strong>Impact:</strong> ${insight.impact}</div>
                    <div style="margin: 10px 0; color: #28a745;"><strong>Confidence:</strong> ${insight.confidence_score.toFixed(1)}%</div>
                    <div class="insight-actions">
                        <h4>🎯 Recommended Actions:</h4>
                        ${insight.recommended_actions.map(action => 
                            `<div class="action-item">✓ ${action}</div>`
                        ).join('')}
                    </div>
                `;
                
                container.appendChild(card);
            });
        }
        
        // Load dashboard on page load
        window.addEventListener('load', loadDashboard);
    </script>
</body>
</html>
    """

    return render_template_string(html_template, store_id=store_id)
