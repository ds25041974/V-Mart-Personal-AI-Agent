"""
AI Chat Routes with Context-Aware Responses
Flask blueprint for intelligent chatbot with store, weather, and competitor context

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import json
import os
from datetime import datetime
from queue import Queue

from flask import (
    Blueprint,
    Response,
    jsonify,
    render_template,
    request,
    stream_with_context,
)
from src.agent.gemini_agent import GeminiAgent

# Create blueprint
ai_chat_bp = Blueprint("ai_chat", __name__, url_prefix="/ai-chat")

# Initialize Gemini Agent
gemini_agent = GeminiAgent(os.getenv("GEMINI_API_KEY") or "demo_key")


@ai_chat_bp.route("/", methods=["GET"])
def chat_interface():
    """Serve the AI chat interface"""
    return render_template("ai_chat.html")


@ai_chat_bp.route("/ask", methods=["POST"])
def ask_with_context():
    """
    Ask a question with automatic store/weather/competitor context injection

    Request JSON:
    {
        "question": "How will the weather affect sales today?",
        "store_id": "VM_DL_001",  // Optional
        "city": "Mumbai",  // Optional (alternative to store_id)
        "include_weather": true,  // Default: true
        "include_competitors": true,  // Default: true
        "include_analytics": false  // Default: false
    }
    """
    try:
        data = request.get_json()

        if not data or "question" not in data:
            return jsonify({"error": "Question is required"}), 400

        question = data["question"]
        store_id = data.get("store_id")
        city = data.get("city")
        include_weather = data.get("include_weather", True)
        include_competitors = data.get("include_competitors", True)
        include_analytics = data.get("include_analytics", False)

        # Get analytics context if requested
        analytics_context = None
        if include_analytics and store_id:
            try:
                from src.analytics.analytics_service import AnalyticsService

                analytics_service = AnalyticsService()
                insights = analytics_service.get_store_insights(store_id)
                if insights:
                    analytics_context = json.dumps(insights, indent=2)
            except Exception as e:
                print(f"Warning: Could not load analytics: {e}")

        # Get AI response with context
        response = gemini_agent.get_response(
            prompt=question,
            store_id=store_id,
            city=city,
            analytics_context=analytics_context,
            include_weather=include_weather,
            include_competitors=include_competitors,
        )

        return jsonify(
            {
                "success": True,
                "question": question,
                "response": response,
                "context_used": {
                    "store_id": store_id,
                    "city": city,
                    "weather_included": include_weather,
                    "competitors_included": include_competitors,
                    "analytics_included": include_analytics
                    and analytics_context is not None,
                },
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_chat_bp.route("/ask-stream", methods=["GET"])
def ask_with_progress():
    """
    Ask a question with real-time progress updates (Server-Sent Events)

    Query parameters:
        - question: The question to ask
        - store_id: Optional store ID
        - city: Optional city name
        - include_weather: true/false
        - include_competitors: true/false
        - include_analytics: true/false

    Returns progress updates as the AI processes the question.
    """
    try:
        question = request.args.get("question")

        if not question:
            return jsonify({"error": "Question is required"}), 400

        store_id = request.args.get("store_id")
        city = request.args.get("city")
        include_weather = request.args.get("include_weather", "true").lower() == "true"
        include_competitors = (
            request.args.get("include_competitors", "true").lower() == "true"
        )
        include_analytics = (
            request.args.get("include_analytics", "false").lower() == "true"
        )  # Create a queue for progress updates
        progress_queue = Queue()

        def progress_callback(message: str):
            """Callback to send progress updates"""
            progress_queue.put({"type": "progress", "message": message})

        def generate():
            """Generator for streaming responses"""
            # Send initial status
            yield f"data: {json.dumps({'type': 'start', 'message': 'Processing your question...'})}\n\n"

            # Get analytics context if requested
            analytics_context = None
            if include_analytics and store_id:
                try:
                    yield f"data: {json.dumps({'type': 'progress', 'message': '📊 Loading analytics data...'})}\n\n"
                    from src.analytics.analytics_service import AnalyticsService

                    analytics_service = AnalyticsService()
                    insights = analytics_service.get_store_insights(store_id)
                    if insights:
                        analytics_context = json.dumps(insights, indent=2)
                        yield f"data: {json.dumps({'type': 'progress', 'message': '✅ Analytics loaded'})}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({'type': 'warning', 'message': f'⚠️ Analytics unavailable: {str(e)}'})}\n\n"

            # Get AI response with progress tracking
            try:
                response = gemini_agent.get_response(
                    prompt=question,
                    store_id=store_id,
                    city=city,
                    analytics_context=analytics_context,
                    include_weather=include_weather,
                    include_competitors=include_competitors,
                    progress_callback=progress_callback,
                )

                # Send progress updates from queue
                while not progress_queue.empty():
                    progress_msg = progress_queue.get()
                    yield f"data: {json.dumps(progress_msg)}\n\n"

                # Send final response
                yield f"data: {json.dumps({'type': 'response', 'message': response})}\n\n"
                yield f"data: {json.dumps({'type': 'complete', 'message': 'Analysis complete'})}\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        return Response(
            stream_with_context(generate()),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_chat_bp.route("/store-weather/<store_id>", methods=["GET"])
def get_store_weather_summary(store_id: str):
    """
    Get weather summary for a specific store with AI insights
    """
    try:
        if not gemini_agent.context_manager:
            return jsonify({"error": "Context manager not available"}), 500

        # Get weather context
        weather_ctx = gemini_agent.context_manager.get_weather_context(
            store_id, include_forecast=True
        )

        if not weather_ctx:
            return jsonify({"error": "Store not found"}), 404

        # Get AI insight about weather impact
        prompt = f"""Based on the current weather conditions for store {store_id}, 
        provide a brief analysis (2-3 sentences) of how this weather might impact:
        1. Customer footfall
        2. Product categories that may see increased/decreased demand
        3. Any operational considerations"""

        ai_insight = gemini_agent.get_response(
            prompt=prompt,
            store_id=store_id,
            use_context=False,
        )

        return jsonify(
            {
                "success": True,
                "store_id": store_id,
                "weather": weather_ctx,
                "ai_insight": ai_insight,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_chat_bp.route("/competitor-analysis/<store_id>", methods=["GET"])
def get_competitor_analysis(store_id: str):
    """
    Get competitor analysis for a specific store with AI recommendations
    """
    try:
        if not gemini_agent.context_manager:
            return jsonify({"error": "Context manager not available"}), 500

        # Get store context
        store_ctx = gemini_agent.context_manager.get_store_context(store_id)

        if not store_ctx:
            return jsonify({"error": "Store not found"}), 404

        # Get AI analysis of competition
        prompt = f"""Based on the competitor data for store {store_id}, provide:
        1. Assessment of competitive pressure (Low/Medium/High)
        2. Key competitive threats
        3. Two specific recommendations to differentiate from competitors
        Keep response concise (3-4 sentences)."""

        ai_analysis = gemini_agent.get_response(
            prompt=prompt,
            store_id=store_id,
            use_context=False,
        )

        return jsonify(
            {
                "success": True,
                "store_id": store_id,
                "competitors": store_ctx["competitors"],
                "ai_analysis": ai_analysis,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_chat_bp.route("/daily-briefing/<store_id>", methods=["GET"])
def get_daily_briefing(store_id: str):
    """
    Get comprehensive daily briefing with weather, competitors, and AI insights
    """
    try:
        if not gemini_agent.context_manager:
            return jsonify({"error": "Context manager not available"}), 500

        # Get comprehensive context
        store_ctx = gemini_agent.context_manager.get_store_context(store_id)

        if not store_ctx:
            return jsonify({"error": "Store not found"}), 404

        # Get AI daily briefing
        today = datetime.now().strftime("%A, %B %d, %Y")
        prompt = f"""Generate a concise daily briefing for {today} covering:
        1. Weather impact on operations today
        2. Key competitive considerations
        3. Top 2-3 action items for store manager
        4. Any alerts or opportunities
        
        Keep it professional and action-oriented (5-6 sentences)."""

        briefing = gemini_agent.get_response(
            prompt=prompt,
            store_id=store_id,
            use_context=False,
        )

        return jsonify(
            {
                "success": True,
                "store_id": store_id,
                "date": today,
                "store_info": store_ctx["store"],
                "weather": store_ctx["weather"],
                "competition_summary": {
                    "total_nearby": store_ctx["competitors"]["total_nearby"],
                    "closest": store_ctx["competitors"]["closest"],
                },
                "ai_briefing": briefing,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
