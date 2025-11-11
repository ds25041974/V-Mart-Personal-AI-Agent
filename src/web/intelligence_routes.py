"""
Retail Intelligence API Routes for V-Mart
Provides AI-powered insights, analytics, and recommendations
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any
import os

# Import retail intelligence modules
try:
    from retail_intelligence import (
        GeminiRetailInsights,
        SalesAnalyzer,
        InventoryPlanner,
        FashionTrendAnalyzer,
        CustomerAnalyzer,
        FestivalPlanner,
        DataIntegrationManager
    )
except ImportError:
    # Try with src prefix
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from retail_intelligence import (
        GeminiRetailInsights,
        SalesAnalyzer,
        InventoryPlanner,
        FashionTrendAnalyzer,
        CustomerAnalyzer,
        FestivalPlanner,
        DataIntegrationManager
    )

# Create blueprint
intelligence_bp = Blueprint('intelligence', __name__, url_prefix='/api/intelligence')

# Initialize AI engine and analyzers
try:
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    gemini_engine = GeminiRetailInsights(api_key=gemini_api_key) if gemini_api_key else None
    
    sales_analyzer = SalesAnalyzer(gemini_engine=gemini_engine)
    inventory_planner = InventoryPlanner(gemini_engine=gemini_engine)
    fashion_analyzer = FashionTrendAnalyzer(gemini_engine=gemini_engine)
    customer_analyzer = CustomerAnalyzer(gemini_engine=gemini_engine)
    festival_planner = FestivalPlanner(gemini_engine=gemini_engine)
    data_integration_manager = DataIntegrationManager(gemini_engine=gemini_engine)
    
    print("✓ Retail Intelligence modules initialized successfully")
except Exception as e:
    print(f"⚠ Error initializing Retail Intelligence: {e}")
    gemini_engine = None
    sales_analyzer = None
    inventory_planner = None
    fashion_analyzer = None
    customer_analyzer = None
    festival_planner = None
    data_integration_manager = None


# ==================== CHAT & GENERAL INSIGHTS ====================

@intelligence_bp.route('/chat', methods=['POST'])
def chat_with_ai():
    """
    Natural conversation with AI for retail insights
    Handles greetings and routes to appropriate analysis
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        context_data = data.get('context_data', {})
        
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'}), 400
        
        if not gemini_engine:
            return jsonify({'success': False, 'error': 'Gemini AI engine not initialized'}), 500
        
        # Check if it's a greeting
        greeting_words = ['hi', 'hello', 'hey', 'namaste', 'good morning', 'good afternoon', 'good evening']
        if any(greeting in query.lower() for greeting in greeting_words):
            response = gemini_engine.handle_greeting(query)
            return jsonify({
                'success': True,
                'response': response,
                'type': 'greeting'
            })
        
        # General AI insights
        response = gemini_engine.get_insights(
            query=query,
            context_data=context_data,
            analytics_type='general'
        )
        
        return jsonify({
            'success': True,
            'query': query,
            'response': response,
            'type': 'ai_insights'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== SALES ANALYTICS ====================

@intelligence_bp.route('/sales/daily', methods=['POST'])
def analyze_daily_sales():
    """Analyze daily sales performance"""
    try:
        data = request.get_json()
        sales_data = data.get('sales_data', {})
        store_id = data.get('store_id', 'ALL')
        
        result = sales_analyzer.analyze_daily_sales(sales_data, store_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@intelligence_bp.route('/sales/hourly', methods=['POST'])
def analyze_hourly_sales():
    """Analyze hourly sales patterns"""
    try:
        data = request.get_json()
        hourly_data = data.get('hourly_data', [])
        date = data.get('date', '')
        
        result = sales_analyzer.analyze_hourly_sales(hourly_data, date)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@intelligence_bp.route('/sales/salesperson', methods=['POST'])
def analyze_salesperson_performance():
    """Analyze salesperson performance"""
    try:
        data = request.get_json()
        salesperson_data = data.get('salesperson_data', [])
        period = data.get('period', 'monthly')
        
        result = sales_analyzer.analyze_salesperson_performance(salesperson_data, period)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@intelligence_bp.route('/sales/forecast', methods=['POST'])
def forecast_sales():
    """Forecast future sales"""
    try:
        data = request.get_json()
        historical_data = data.get('historical_data', [])
        forecast_days = data.get('forecast_days', 30)
        
        result = sales_analyzer.forecast_sales(historical_data, forecast_days)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== FESTIVAL PLANNING ====================

@intelligence_bp.route('/festival/upcoming', methods=['GET'])
def get_upcoming_festivals():
    """Get upcoming festivals for planning"""
    try:
        region = request.args.get('region')
        months_ahead = int(request.args.get('months_ahead', 6))
        
        result = festival_planner.get_upcoming_festivals(region, months_ahead)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== FILE UPLOAD & DATA INTEGRATION ====================

@intelligence_bp.route('/data/upload', methods=['POST'])
def upload_and_analyze_file():
    """
    Upload file (CSV, Excel, PDF, JSON, TXT) and get AI analysis
    """
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        data_context = request.form.get('data_context', 'Unknown')
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Save file temporarily
        upload_folder = '/tmp/vmart_uploads'
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        
        # Process file
        result = data_integration_manager.process_uploaded_file(
            file_path=file_path,
            data_context=data_context
        )
        
        # Clean up
        try:
            os.remove(file_path)
        except:
            pass
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@intelligence_bp.route('/data/google-sheets', methods=['POST'])
def analyze_google_sheet():
    """
    Read and analyze data from Google Sheets
    """
    try:
        data = request.get_json()
        spreadsheet_id = data.get('spreadsheet_id')
        range_name = data.get('range', 'Sheet1!A1:Z1000')
        credentials_path = data.get('credentials_path')
        
        if not spreadsheet_id:
            return jsonify({'success': False, 'error': 'spreadsheet_id is required'}), 400
        
        # Connect to Google Sheets
        if credentials_path:
            connection_result = data_integration_manager.connect_google_sheets(credentials_path)
            if not connection_result['success']:
                return jsonify(connection_result), 500
        
        # Read and analyze sheet
        result = data_integration_manager.read_google_sheet(spreadsheet_id, range_name)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@intelligence_bp.route('/data/database', methods=['POST'])
def query_and_analyze_database():
    """
    Connect to database, execute query, and analyze results
    """
    try:
        data = request.get_json()
        db_type = data.get('db_type')  # 'mssql', 'postgresql', 'oracle', 'mysql'
        connection_params = data.get('connection_params', {})
        query = data.get('query')
        query_context = data.get('query_context', 'Unknown')
        
        if not db_type or not connection_params or not query:
            return jsonify({
                'success': False,
                'error': 'db_type, connection_params, and query are required'
            }), 400
        
        # Connect to database
        connection_result = data_integration_manager.connect_database(db_type, connection_params)
        if not connection_result['success']:
            return jsonify(connection_result), 500
        
        # Execute query and analyze
        result = data_integration_manager.query_database(query, query_context)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== CUSTOM INSIGHTS ====================

@intelligence_bp.route('/insights/custom', methods=['POST'])
def get_custom_insights():
    """
    Get custom AI insights for any retail query
    Routes to appropriate analyzer based on analytics_type
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        analytics_type = data.get('analytics_type', 'general')
        context_data = data.get('context_data', {})
        
        # Route to appropriate analyzer
        if analytics_type == 'sales':
            # Sales-related query
            if 'hourly' in query.lower():
                result = sales_analyzer.analyze_hourly_sales(context_data.get('hourly_data', []), context_data.get('date', ''))
            else:
                result = gemini_engine.analyze_sales_performance(context_data)
                
        elif analytics_type == 'inventory':
            result = inventory_planner.forecast_inventory_needs(
                context_data.get('sales_forecast', {}),
                context_data.get('current_stock', {})
            )
            
        elif analytics_type == 'fashion':
            if 'image' in context_data:
                result = fashion_analyzer.analyze_product_image(context_data['image'])
            elif 'global' in query.lower():
                result = fashion_analyzer.analyze_global_trends(
                    context_data.get('season', 'Summer'),
                    context_data.get('year', 2025)
                )
            else:
                result = fashion_analyzer.analyze_local_trends(
                    context_data.get('region', 'Uttar Pradesh'),
                    context_data.get('sales_data', {})
                )
                
        elif analytics_type == 'customer':
            if 'footfall' in query.lower():
                result = customer_analyzer.analyze_footfall(context_data)
            elif 'conversion' in query.lower():
                result = customer_analyzer.analyze_conversion(
                    context_data.get('footfall', 0),
                    context_data.get('transactions', 0),
                    context_data.get('sales_inr', 0)
                )
            else:
                result = customer_analyzer.analyze_catchment_area(
                    context_data.get('store_location', [0, 0]),
                    context_data.get('customer_data')
                )
                
        elif analytics_type == 'festival':
            result = festival_planner.forecast_festival_sales(
                context_data.get('festival_name', 'Diwali'),
                context_data.get('base_daily_sales', 200000)
            )
            
        elif analytics_type == 'logistics':
            result = gemini_engine.optimize_logistics(context_data)
            
        elif analytics_type == 'marketing':
            result = gemini_engine.analyze_marketing_performance(context_data)
            
        else:
            # General AI insights
            result = gemini_engine.get_insights(query, context_data, analytics_type)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== SYSTEM HEALTH ====================

@intelligence_bp.route('/health', methods=['GET'])
def health_check():
    """Check system health and module status"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'modules': {
            'gemini_engine': gemini_engine is not None,
            'sales_analyzer': sales_analyzer is not None,
            'inventory_planner': inventory_planner is not None,
            'fashion_analyzer': fashion_analyzer is not None,
            'customer_analyzer': customer_analyzer is not None,
            'festival_planner': festival_planner is not None,
            'data_integration': data_integration_manager is not None
        },
        'features': [
            'Natural AI Conversation',
            'Sales Analytics',
            'Inventory Planning',
            'Fashion Trend Analysis',
            'Customer Analytics',
            'Festival Planning',
            'File Upload & Analysis',
            'Google Sheets Integration',
            'Database Integration'
        ]
    })

from flask import Blueprint, jsonify, request
from retail_intelligence import (
    GeminiRetailInsights,
    SalesAnalyzer,
    InventoryPlanner,
    FashionTrendAnalyzer,
    CustomerAnalyzer,
    FestivalPlanner,
)
import os

# Create blueprint
intelligence_bp = Blueprint("intelligence", __name__, url_prefix="/api/intelligence")

# Initialize AI engines
gemini_engine = GeminiRetailInsights(api_key=os.getenv("GEMINI_API_KEY"))
sales_analyzer = SalesAnalyzer(gemini_engine)
inventory_planner = InventoryPlanner(gemini_engine)
fashion_analyzer = FashionTrendAnalyzer(gemini_engine)
customer_analyzer = CustomerAnalyzer(gemini_engine)
festival_planner = FestivalPlanner(gemini_engine)


@intelligence_bp.route("/chat", methods=["POST"])
def chat_with_ai():
    """
    Chat with Gemini AI for retail insights
    Handles greetings naturally and provides detailed analysis
    """
    try:
        data = request.get_json()
        query = data.get("query", "")
        context = data.get("context", {})
        analytics_type = data.get("type")

        if not query:
            return jsonify({"success": False, "error": "Query is required"}), 400

        # Check for greetings
        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "namaste"]
        if any(greeting in query.lower() for greeting in greetings):
            response = gemini_engine.handle_greeting(query)
            return jsonify(response)

        # Get AI insights
        response = gemini_engine.get_insights(query, context, analytics_type)
        return jsonify(response)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@intelligence_bp.route("/sales/daily", methods=["POST"])
def analyze_daily_sales():
    """Analyze daily sales performance"""
    try:
        data = request.get_json()
        sales_data = data.get("sales_data", [])
        store_id = data.get("store_id")

        analysis = sales_analyzer.analyze_daily_sales(sales_data, store_id)
        return jsonify({"success": True, **analysis})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@intelligence_bp.route("/sales/hourly", methods=["POST"])
def analyze_hourly_sales():
    """Analyze hourly sales for peak hour identification"""
    try:
        data = request.get_json()
        hourly_data = data.get("hourly_data", [])
        date = data.get("date")

        analysis = sales_analyzer.analyze_hourly_sales(hourly_data, date)
        return jsonify({"success": True, **analysis})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@intelligence_bp.route("/sales/salesperson", methods=["POST"])
def analyze_salesperson():
    """Analyze salesperson performance"""
    try:
        data = request.get_json()
        salesperson_data = data.get("salesperson_data", [])
        period = data.get("period", "month")

        analysis = sales_analyzer.analyze_salesperson_performance(
            salesperson_data, period
        )
        return jsonify({"success": True, **analysis})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@intelligence_bp.route("/sales/forecast", methods=["POST"])
def forecast_sales():
    """Forecast future sales"""
    try:
        data = request.get_json()
        historical_data = data.get("historical_data", [])
        forecast_days = data.get("forecast_days", 30)

        forecast = sales_analyzer.forecast_sales(historical_data, forecast_days)
        return jsonify({"success": True, **forecast})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@intelligence_bp.route("/festival/upcoming", methods=["GET"])
def get_upcoming_festivals():
    """Get upcoming festivals for planning"""
    try:
        region = request.args.get("region", "Uttar Pradesh")
        months_ahead = int(request.args.get("months_ahead", 3))

        festivals = festival_planner.get_upcoming_festivals(region, months_ahead)
        return jsonify({"success": True, "festivals": festivals})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@intelligence_bp.route("/insights/custom", methods=["POST"])
def get_custom_insights():
    """
    Get custom AI insights for any retail query
    Supports all types of analysis with curated, detailed responses
    """
    try:
        data = request.get_json()
        query = data.get("query", "")
        analytics_type = data.get("analytics_type")
        context_data = data.get("context_data", {})

        if not query:
            return jsonify({"success": False, "error": "Query is required"}), 400

        # Route to appropriate analyzer based on type
        if analytics_type == "sales":
            response = gemini_engine.analyze_sales_performance(context_data)
        elif analytics_type == "inventory":
            response = gemini_engine.forecast_inventory(context_data)
        elif analytics_type == "fashion":
            response = gemini_engine.analyze_fashion_trends(context_data)
        elif analytics_type == "customer":
            response = gemini_engine.analyze_customer_behavior(context_data)
        elif analytics_type == "festival":
            response = gemini_engine.plan_festival_inventory(context_data)
        elif analytics_type == "logistics":
            response = gemini_engine.optimize_logistics(context_data)
        elif analytics_type == "marketing":
            response = gemini_engine.analyze_marketing_performance(context_data)
        else:
            # Generic insights
            response = gemini_engine.get_insights(query, context_data, analytics_type)

        return jsonify(response)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@intelligence_bp.route("/health", methods=["GET"])
def health_check():
    """Check retail intelligence system health"""
    return jsonify(
        {
            "success": True,
            "system": "V-Mart Retail Intelligence",
            "ai_model": "Gemini 2.0 Flash",
            "modules": {
                "sales_analytics": "active",
                "inventory_planning": "active",
                "fashion_analysis": "active",
                "customer_analytics": "active",
                "festival_planning": "active",
            },
        }
    )
