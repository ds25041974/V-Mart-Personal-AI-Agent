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
from src.utils.file_processor import process_uploaded_file
from src.utils.path_manager import path_manager

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
    # Ask a question with real-time progress updates (Server-Sent Events)
    # Query parameters: question, store_id, city, include_weather, include_competitors, include_analytics, file_context
    # Returns progress updates as the AI processes the question.
    question = request.args.get("question")
    if not question:
        return jsonify({"error": "Question is required"}), 400

    store_id = request.args.get("store_id")
    city = request.args.get("city")
    include_weather = request.args.get("include_weather", "true").lower() == "true"
    include_competitors = (
        request.args.get("include_competitors", "true").lower() == "true"
    )
    include_analytics = request.args.get("include_analytics", "false").lower() == "true"

    file_context_str = request.args.get("file_context")
    file_context = None
    if file_context_str:
        try:
            file_context = json.loads(file_context_str)
            print(f"\n🔍 FILE CONTEXT RECEIVED: {len(file_context)} files")
            for idx, f in enumerate(file_context):
                print(
                    f"   File {idx + 1}: {f.get('filename', 'Unknown')} - Content length: {len(f.get('content', ''))} chars"
                )
        except Exception as e:
            print(f"❌ Failed to parse file_context: {e}")

    use_paths = request.args.get("use_paths", "true").lower() == "true"
    progress_queue = Queue()

    def progress_callback(message: str):
        progress_queue.put({"type": "progress", "message": message})

    def generate():
        try:
            yield f"data: {json.dumps({'type': 'start', 'message': 'Processing your question...'})}\n\n"

            greetings = [
                "hi",
                "hello",
                "hey",
                "good morning",
                "good afternoon",
                "good evening",
                "thanks",
                "thank you",
                "bye",
            ]
            question_lower = question.lower().strip()
            is_greeting = any(
                question_lower == g
                or question_lower.startswith(f"{g} ")
                or question_lower.startswith(f"{g},")
                for g in greetings
            )
            if is_greeting:
                greeting_response = "Hello, I am your V-Mart Personal AI Agent"
                yield f"data: {json.dumps({'type': 'response', 'message': greeting_response, 'format': 'paragraph'})}\n\n"
                yield f"data: {json.dumps({'type': 'complete', 'message': 'Greeting complete'})}\n\n"
                return

            def format_response(ai_response):
                import re

                lines = ai_response.split("\n")
                num_lines = [line for line in lines if re.search(r"\d", line)]
                if len(num_lines) > 2:
                    table = []
                    for line in num_lines:
                        clean = re.sub(r"[^\w\d,.% ]", "", line)
                        table.append(clean)
                    return {"format": "table", "table": table, "insights": lines}
                else:
                    clean = re.sub(r"[^\w\d,.% ]", "", ai_response)
                    return {"format": "paragraph", "paragraph": clean}

            analytics_context = None
            if include_analytics and store_id:
                try:
                    yield f"data: {json.dumps({'type': 'progress', 'message': '📊 Loading analytics data...'})}\n\n"
                    # from src.analytics.analytics_service import AnalyticsService

                    # AnalyticsService initialized if needed, but not used here
                except Exception as e:
                    yield f"data: {json.dumps({'type': 'warning', 'message': f'⚠️ Analytics unavailable: {str(e)}'})}\n\n"

            file_summary = ""
            has_path_files = False
            has_uploaded_files = False

            # PRIORITY 1: Try configured paths first (if enabled and paths exist)
            if use_paths:
                try:
                    paths = path_manager.get_all_paths()
                    if paths and len(paths) > 0:
                        yield f"data: {json.dumps({'type': 'progress', 'message': f'🔍 Searching {len(paths)} configured path(s)...'})}\n\n"
                        search_results = path_manager.search_files(question, limit=10)
                        if search_results and len(search_results) > 0:
                            yield f"data: {json.dumps({'type': 'progress', 'message': f'📁 Found {len(search_results)} relevant file(s) from configured paths'})}\n\n"
                            file_summary += "\n\n**Files from Configured Paths:**\n"
                            for result in search_results[:5]:
                                file_path = result.get("path", "")
                                file_name = result.get("name", "")
                                try:
                                    with open(file_path, "rb") as f:
                                        file_bytes = f.read()
                                    processed = process_uploaded_file(
                                        file_bytes, file_name
                                    )
                                    if processed.get("success"):
                                        content = processed.get("text", "")
                                        file_type = processed.get("file_type", "")
                                        file_summary += f"\n**File: {file_name}** (Type: {file_type})\n"
                                        file_summary += f"Path: {file_path}\n"
                                        if content:
                                            file_summary += f"{content[:2000]}\n"
                                            if len(content) > 2000:
                                                file_summary += f"... (truncated, total {len(content)} characters)\n"
                                            has_path_files = True
                                except Exception as file_error:
                                    file_summary += f"\n**File: {file_name}** - Error: {str(file_error)}\n"
                            if has_path_files:
                                yield f"data: {json.dumps({'type': 'progress', 'message': '✅ Path files processed successfully'})}\n\n"
                            else:
                                yield f"data: {json.dumps({'type': 'warning', 'message': '⚠️ Path files found but could not be processed'})}\n\n"
                        else:
                            yield f"data: {json.dumps({'type': 'info', 'message': '📁 No relevant files found in configured paths'})}\n\n"
                    else:
                        yield f"data: {json.dumps({'type': 'info', 'message': 'ℹ️ No paths configured yet - use browser upload instead'})}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({'type': 'warning', 'message': f'⚠️ Path search warning: {str(e)}'})}\n\n"

            # PRIORITY 2: Process browser-uploaded files (ALWAYS if provided)
            if file_context:
                try:
                    file_label = (
                        "Additional Uploaded Files"
                        if has_path_files
                        else "Uploaded Files"
                    )
                    yield f"data: {json.dumps({'type': 'progress', 'message': f'📎 Processing {len(file_context)} uploaded file(s)...'})}\n\n"
                    file_summary += f"\n\n**{file_label}:**\n"
                    for file_info in file_context:
                        filename = file_info.get("filename", "Unknown")
                        content = file_info.get("content", "")
                        file_type = file_info.get(
                            "file_type", file_info.get("type", "")
                        )
                        file_summary += f"\n**File: {filename}** (Type: {file_type})\n"
                        if content:
                            file_summary += f"{content[:10000]}\n"
                            if len(content) > 10000:
                                file_summary += f"... (truncated, total {len(content)} characters)\n"
                            has_uploaded_files = True
                    if has_uploaded_files:
                        yield f"data: {json.dumps({'type': 'progress', 'message': '✅ Uploaded files processed successfully'})}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({'type': 'warning', 'message': f'⚠️ File processing warning: {str(e)}'})}\n\n"

            # Build final context message
            if has_path_files and has_uploaded_files:
                pass
            elif has_path_files:
                pass
            elif has_uploaded_files:
                pass
            else:
                yield f"data: {json.dumps({'type': 'info', 'message': 'ℹ️ No files available - configure paths or upload files for better insights'})}\n\n"

            # Combine file summary with question
            if file_summary:
                question_with_files = (
                    "🎯 FILE-BASED ANALYSIS MODE - GEMINI AI INSIGHTS ANALYZER 🎯\n\n"
                    "═══ DATA SOURCE HIERARCHY ═══\n"
                    "✓ PRIMARY SOURCE: ONLY the uploaded files below for ALL business metrics (revenue, sales, inventory, stores, products, etc.)\n"
                    "✓ SUPPLEMENTARY: Live weather data ONLY (current temperature, forecast, conditions)\n"
                    "✗ FORBIDDEN: Any stored/trained data about V-Mart stores, sales, or operations\n\n"
                    "═══ MANDATORY ANALYSIS BEHAVIORS ═══\n"
                    "1. COMPREHENSIVE FILE READING:\n"
                    "   - Read ALL uploaded files COMPLETELY (do not skip any sections)\n"
                    "   - Extract EVERY relevant data point, metric, and value\n"
                    "   - Parse all columns, rows, and data structures thoroughly\n\n"
                    "2. CROSS-FILE CORRELATION & RELATIONSHIPS:\n"
                    "   - Identify common keys across files (Store_ID, Date, Product_ID, Location, etc.)\n"
                    "   - MERGE and CORRELATE data from multiple files using these keys\n"
                    "   - Example: Match Store_ID from CSV with Excel inventory to create unified insights\n"
                    "   - Find patterns that emerge ONLY when correlating multiple files\n"
                    "   - Build relationships between datasets (e.g., sales trends + weather patterns + inventory levels)\n\n"
                    "3. DUPLICATE DETECTION & ELIMINATION:\n"
                    "   - Identify any duplicate entries across files (same Store_ID, Date, Product, etc.)\n"
                    "   - MERGE duplicates intelligently (use most recent, complete, or accurate data)\n"
                    "   - Flag any discrepancies in duplicate data\n"
                    "   - Present consolidated, de-duplicated results ONLY\n"
                    "   - DO NOT double-count metrics (sales, revenue, inventory) from duplicate entries\n\n"
                    "4. DATA CURATION & VALIDATION:\n"
                    "   - Validate data integrity (check for missing values, outliers, inconsistencies)\n"
                    "   - Curate data by removing noise and focusing on relevant metrics\n"
                    "   - Standardize formats (dates, currency, units) across all files\n"
                    "   - Flag any data quality issues (e.g., 'Store_101 has missing revenue data in file X')\n\n"
                    "5. EXACT VALUE QUOTATION:\n"
                    "   - Quote exact values as they appear in files (e.g., 'Revenue: ₹45,678', not '~45k')\n"
                    "   - Reference file names for EVERY data point (e.g., 'From sales_report.csv: Store_101 revenue = ₹45,678')\n"
                    "   - Include units, currency symbols, and proper formatting\n\n"
                    "6. WEATHER INTEGRATION:\n"
                    "   - Use live weather ONLY for context/recommendations\n"
                    "   - Example: 'Weather today: 28°C sunny → Recommend outdoor product displays'\n"
                    "   - Correlate weather with sales/footfall trends if data supports it\n\n"
                    "🚨 CRITICAL DATA AVAILABILITY RULE 🚨\n"
                    "If asked about ANY store, location, metric, or data point NOT found in the uploaded files:\n"
                    "RESPOND EXACTLY: 'This information is not available in the uploaded files. The uploaded files only contain data for: [list what IS in the files].'\n"
                    "DO NOT provide ANY information about stores/locations not explicitly mentioned in the files.\n\n"
                    "═══ STRICTLY FORBIDDEN ═══\n"
                    "✗ NO stored V-Mart data from your training\n"
                    "✗ NO database lookups for sales/revenue\n"
                    "✗ NO assumptions or estimates\n"
                    "✗ NO data about stores not in the uploaded files\n"
                    "✗ NO double-counting of metrics from duplicate entries\n\n"
                    "═══ UPLOADED FILES (YOUR ONLY DATA SOURCE) ═══\n"
                    f"{file_summary}\n\n"
                    "═══ RESPONSE REQUIREMENTS ═══\n"
                    f"USER'S QUESTION: {question}\n\n"
                    "YOUR RESPONSE MUST INCLUDE:\n\n"
                    "📋 1. FILES ANALYZED:\n"
                    "   - List all files processed\n"
                    "   - Note any data quality issues\n\n"
                    "📊 2. DATA SUMMARY (Curated & Validated):\n"
                    "   - Key metrics extracted from files (with exact values + file citations)\n"
                    "   - De-duplicated data (if duplicates were found, explain how you handled them)\n"
                    "   - Data validation notes (missing values, outliers, inconsistencies)\n\n"
                    "🔗 3. CROSS-FILE DATA CORRELATION:\n"
                    "   - Relationships discovered across multiple files\n"
                    "   - Merged insights using common keys (Store_ID, Date, etc.)\n"
                    "   - Example: 'Store_101 (from sales.csv) + Inventory_Store_101 (from inventory.xlsx) = 80% inventory turnover'\n"
                    "   - Patterns that emerge only when correlating files\n\n"
                    "🌤️ 4. WEATHER CONTEXT (if applicable):\n"
                    "   - Current/forecast weather for relevant locations\n"
                    "   - How weather impacts sales/footfall based on file data\n\n"
                    "💡 5. CRISP INSIGHTS (Clear & Actionable):\n"
                    "   - Direct findings from the curated, correlated file data\n"
                    "   - Highlight trends, patterns, anomalies\n"
                    "   - Use bullet points for clarity\n\n"
                    "🎯 6. CURATED & RELEVANT RECOMMENDATIONS:\n"
                    "   - Specific, actionable strategies based on correlated file data + weather\n"
                    "   - Prioritized by impact (High/Medium/Low)\n"
                    "   - Each recommendation must cite supporting data from files\n\n"
                    "✅ 7. CONCISE STRATEGIC ACTIONABLES:\n"
                    "   - Summarized next steps (3-5 key actions)\n"
                    "   - Timeline (Immediate/Short-term/Long-term)\n"
                    "   - Expected outcomes\n\n"
                    "📝 8. DETAILED SUMMARY:\n"
                    "   - Comprehensive overview of ALL findings\n"
                    "   - Integrate all sections above into a cohesive narrative\n"
                    "   - Ensure no critical insights are missed\n\n"
                    "📌 9. SOURCES & CITATIONS:\n"
                    "   - Cite file name + specific row/column for EVERY data point\n"
                    "   - Example: '[sales_report.csv, Row 5, Store_ID: 101, Revenue: ₹45,678]'\n\n"
                    "🚀 BEGIN GEMINI AI INSIGHTS ANALYSIS 🚀\n"
                    "(Using ONLY uploaded file data + live weather, with full correlation, de-duplication, and curation)"
                )
            else:
                question_with_files = question

            try:
                response = gemini_agent.get_response(
                    prompt=question_with_files,
                    store_id=store_id,
                    city=city,
                    analytics_context=analytics_context,
                    include_weather=include_weather,
                    include_competitors=include_competitors,
                    progress_callback=progress_callback,
                )

                while not progress_queue.empty():
                    progress_msg = progress_queue.get()
                    yield f"data: {json.dumps(progress_msg)}\n\n"

                yield f"data: {json.dumps({'type': 'response', 'message': response})}\n\n"
                yield f"data: {json.dumps({'type': 'complete', 'message': 'Analysis complete'})}\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
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


@ai_chat_bp.route("/store-weather/<store_id>", methods=["GET"])
def get_store_weather_summary(store_id: str):
    # Get weather summary for a specific store with AI insights
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
        prompt = (
            f"Based on the current weather conditions for store {store_id}, "
            "provide a brief analysis (2-3 sentences) of how this weather might impact: "
            "1. Customer footfall "
            "2. Product categories that may see increased/decreased demand "
            "3. Any operational considerations"
        )

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
    # Get competitor analysis for a specific store with AI recommendations
    try:
        if not gemini_agent.context_manager:
            return jsonify({"error": "Context manager not available"}), 500

        # Get store context
        store_ctx = gemini_agent.context_manager.get_store_context(store_id)

        if not store_ctx:
            return jsonify({"error": "Store not found"}), 404

        # Get AI analysis of competition
        prompt = (
            f"Based on the competitor data for store {store_id}, provide: "
            "1. Assessment of competitive pressure (Low/Medium/High) "
            "2. Key competitive threats "
            "3. Two specific recommendations to differentiate from competitors "
            "Keep response concise (3-4 sentences)."
        )

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
    # Get comprehensive daily briefing with weather, competitors, and AI insights
    try:
        if not gemini_agent.context_manager:
            return jsonify({"error": "Context manager not available"}), 500

        # Get comprehensive context
        store_ctx = gemini_agent.context_manager.get_store_context(store_id)

        if not store_ctx:
            return jsonify({"error": "Store not found"}), 404

        # Get AI daily briefing
        today = datetime.now().strftime("%A, %B %d, %Y")
        prompt = (
            f"Generate a concise daily briefing for {today} covering: "
            "1. Weather impact on operations today "
            "2. Key competitive considerations "
            "3. Top 2-3 action items for store manager "
            "4. Any alerts or opportunities "
            "Keep it professional and action-oriented (5-6 sentences)."
        )

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


@ai_chat_bp.route("/upload", methods=["POST"])
def upload_files():
    # Handle file uploads and extract content (supports multi-sheet Excel)
    # Accepts multiple files via multipart/form-data
    # Returns extracted text/data from each file
    try:
        print("\n" + "=" * 60)
        print("📤 FILE UPLOAD REQUEST RECEIVED")
        print("=" * 60)

        if "files" not in request.files:
            print("❌ No 'files' field in request")
            return jsonify({"success": False, "error": "No files uploaded"}), 400

        files = request.files.getlist("files")
        print(f"📁 Files received: {len(files)}")

        if not files or len(files) == 0:
            print("❌ Empty files list")
            return jsonify({"success": False, "error": "No files provided"}), 400

        # Import file processor
        from src.utils.file_processor import process_uploaded_file

        file_data = []
        successful_files = 0
        failed_files = 0

        for idx, file in enumerate(files):
            if not file or file.filename == "":
                print(f"⚠️  File {idx + 1}: Empty or no filename")
                continue

            try:
                print(f"\n📄 Processing file {idx + 1}/{len(files)}: {file.filename}")

                # Read file bytes
                file_bytes = file.read()
                file_size = len(file_bytes)
                print(f"   Size: {file_size} bytes")

                if not file_bytes or file_size == 0:
                    print("   ❌ Empty file content")
                    file_data.append(
                        {
                            "filename": file.filename,
                            "type": "error",
                            "size": 0,
                            "error": "Empty file",
                            "content": "",
                            "preview": "",
                        }
                    )
                    failed_files += 1
                    continue

                # Process file
                print("   🔄 Processing with file_processor...")
                result = process_uploaded_file(file_bytes, file.filename or "unknown")
                print(f"   Result success: {result.get('success')}")

                if result.get("success"):
                    # Get content
                    content = result.get("text", "")
                    content_length = len(content)
                    print(f"   ✅ Content extracted: {content_length} characters")

                    # Get content preview (first 500 chars)
                    preview = content[:500] if content else ""

                    file_info = {
                        "filename": result["filename"],
                        "type": result["file_type"],
                        "file_type": result["file_type"],  # Keep for compatibility
                        "size": file_size,
                        "preview": preview,
                        "content": content,
                        "metadata": {
                            k: v
                            for k, v in result.items()
                            if k not in ["filename", "file_type", "text", "success"]
                        },
                    }
                    file_data.append(file_info)
                    successful_files += 1
                    print("   ✅ File processed successfully")
                else:
                    error_msg = result.get("error", "Processing failed")
                    print(f"   ❌ Processing failed: {error_msg}")
                    file_data.append(
                        {
                            "filename": file.filename,
                            "type": "error",
                            "file_type": "error",
                            "size": file_size,
                            "error": error_msg,
                            "content": "",
                            "preview": "",
                        }
                    )
                    failed_files += 1

            except Exception as e:
                error_msg = f"Error processing file: {str(e)}"
                print(f"   ❌ Exception: {error_msg}")
                import traceback

                traceback.print_exc()

                file_data.append(
                    {
                        "filename": file.filename,
                        "type": "error",
                        "file_type": "error",
                        "size": len(file_bytes) if "file_bytes" in locals() else 0,
                        "error": error_msg,
                        "content": "",
                        "preview": "",
                    }
                )
                failed_files += 1

        print("\n📊 UPLOAD SUMMARY:")
        print(f"   ✅ Successful: {successful_files}")
        print(f"   ❌ Failed: {failed_files}")
        print(f"   📁 Total: {len(file_data)}")

        # ========== MULTI-FILE CROSS-REFERENCE ANALYSIS ==========
        cross_reference_analysis = None
        if len(file_data) >= 2:
            try:
                from src.utils.file_cross_referencer import FileCrossReferencer

                cross_ref = FileCrossReferencer()

                # Prepare files for analysis
                files_for_analysis = [
                    {
                        "name": fd["filename"],
                        "content": fd.get("content", ""),
                        "format": fd.get("file_type", "unknown"),
                    }
                    for fd in file_data
                    if "content" in fd and fd.get("content")
                ]

                if len(files_for_analysis) >= 2:
                    # Perform cross-reference analysis
                    analysis = cross_ref.analyze_multiple_files(files_for_analysis)

                    # Format as readable report
                    if analysis.get("success"):
                        cross_reference_analysis = {
                            "report": cross_ref.format_cross_reference_report(analysis),
                            "insights": analysis.get("insights", []),
                            "cross_references_count": len(
                                analysis.get("cross_references", [])
                            ),
                            "correlations_count": len(analysis.get("correlations", [])),
                        }
            except Exception as e:
                print(f"Cross-reference analysis failed: {e}")

        response_data = {
            "success": True,
            "file_count": len(file_data),
            "files": file_data,  # Frontend expects 'files' not 'file_data'
            "file_data": file_data,  # Keep for backward compatibility
        }

        # Add cross-reference analysis if available
        if cross_reference_analysis:
            response_data["cross_reference_analysis"] = cross_reference_analysis

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@ai_chat_bp.route("/export-pdf", methods=["POST"])
def export_pdf():
    # Generate PDF export from AI response content
    # Request JSON: { "content": "AI response text", "store_id": "VM_DL_001" }
    try:
        data = request.get_json()

        if not data or "content" not in data:
            return jsonify({"error": "Content is required"}), 400

        content = data["content"]
        store_id = data.get("store_id")

        # Import export generator
        from src.utils.export_generator import generate_pdf

        # Generate PDF
        pdf_bytes = generate_pdf(content, store_id)

        # Return as downloadable file
        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=vmart_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            },
        )

    except ImportError as e:
        return jsonify({"error": f"PDF generation not available: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"PDF generation failed: {str(e)}"}), 500


@ai_chat_bp.route("/export-docx", methods=["POST"])
def export_docx():
    # Generate DOCX export from AI response content
    # Request JSON: { "content": "AI response text", "store_id": "VM_DL_001" }
    try:
        data = request.get_json()

        if not data or "content" not in data:
            return jsonify({"error": "Content is required"}), 400

        content = data["content"]
        store_id = data.get("store_id")

        # Import export generator
        from src.utils.export_generator import generate_docx

        # Generate DOCX
        docx_bytes = generate_docx(content, store_id)

        # Return as downloadable file
        return Response(
            docx_bytes,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename=vmart_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            },
        )

    except ImportError as e:
        return jsonify({"error": f"DOCX generation not available: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"DOCX generation failed: {str(e)}"}), 500


# ===== Path Configuration Endpoints =====


@ai_chat_bp.route("/paths", methods=["GET"])
def get_configured_paths():
    # Get all configured local paths
    try:
        paths = path_manager.get_all_paths()
        return jsonify({"success": True, "paths": paths})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_chat_bp.route("/paths", methods=["POST"])
def add_configured_path():
    # Add a new path configuration
    try:
        data = request.get_json()
        name = data.get("name")
        location = data.get("location")
        description = data.get("description", "")

        if not name or not location:
            return jsonify({"error": "Name and location are required"}), 400

        path_config = path_manager.add_path(name, location, description)
        return jsonify({"success": True, "path": path_config})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_chat_bp.route("/paths/<int:path_id>", methods=["DELETE"])
def remove_configured_path(path_id: int):
    # Remove a path configuration
    try:
        success = path_manager.remove_path(path_id)

        if success:
            return jsonify({"success": True, "message": "Path removed"})
        else:
            return jsonify({"error": "Failed to remove path"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_chat_bp.route("/paths/<int:path_id>/scan", methods=["POST"])
def scan_configured_path(path_id: int):
    # Scan a configured path and count files
    try:
        result = path_manager.scan_path(path_id)
        return jsonify({"success": True, **result})

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_chat_bp.route("/paths/<int:path_id>/files", methods=["GET"])
def get_path_files(path_id: int):
    # Get list of files from a configured path
    try:
        limit = int(request.args.get("limit", 100))
        extensions = request.args.get("extensions")

        file_extensions = None
        if extensions:
            file_extensions = [ext.strip() for ext in extensions.split(",")]

        files = path_manager.get_files_from_path(path_id, limit, file_extensions)

        return jsonify({"success": True, "files": files, "count": len(files)})

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_chat_bp.route("/paths/search", methods=["GET"])
def search_path_files():
    # Search for files across configured paths
    try:
        query = request.args.get("query")

        if not query:
            return jsonify({"error": "Query parameter is required"}), 400

        limit = int(request.args.get("limit", 50))

        results = path_manager.search_files(query, limit=limit)

        return jsonify({"success": True, "results": results, "count": len(results)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
