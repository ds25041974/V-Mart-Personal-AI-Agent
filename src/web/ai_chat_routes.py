"""
AI Chat Routes with Context-Aware Responses
Flask blueprint for intelligent chatbot with store, weather, and competitor context

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import io
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
    send_file,
    stream_with_context,
)

from src.agent.gemini_agent import GeminiAgent
from src.utils.export_generator import generate_docx, generate_pdf
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
    """
    Ask a question with real-time progress updates (Server-Sent Events)

    Query parameters:
        - question: The question to ask
        - store_id: Optional store ID
        - city: Optional city name
        - include_weather: true/false
        - include_competitors: true/false
        - include_analytics: true/false
        - file_context: JSON string with file data

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
        )

        # Get file context if provided
        file_context_str = request.args.get("file_context")
        file_context = None
        if file_context_str:
            try:
                file_context = json.loads(file_context_str)
            except:
                pass

        # Check if we should use configured paths
        use_paths = request.args.get("use_paths", "true").lower() == "true"

        # Create a queue for progress updates
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

            # Build complete file context with fallback priority:
            # Priority 1: Configured paths with available files
            # Priority 2: Browser-uploaded files
            # Priority 3: No file context (question only)
            file_summary = ""
            has_path_files = False
            has_uploaded_files = False

            # PRIORITY 1: Try configured paths first (if enabled and paths exist)
            if use_paths:
                try:
                    paths = path_manager.get_all_paths()
                    if paths and len(paths) > 0:
                        yield f"data: {json.dumps({'type': 'progress', 'message': f'🔍 Searching {len(paths)} configured path(s)...'})}\n\n"

                        # Search for relevant files based on question keywords
                        search_results = path_manager.search_files(question, limit=10)

                        if search_results and len(search_results) > 0:
                            yield f"data: {json.dumps({'type': 'progress', 'message': f'📁 Found {len(search_results)} relevant file(s) from configured paths'})}\n\n"

                            file_summary += "\n\n**Files from Configured Paths:**\n"

                            for result in search_results[
                                :5
                            ]:  # Limit to 5 most relevant files
                                file_path = result.get("path", "")
                                file_name = result.get("name", "")

                                try:
                                    # Read file content
                                    with open(file_path, "rb") as f:
                                        file_bytes = f.read()

                                    # Process file using file_processor
                                    processed = process_uploaded_file(
                                        file_bytes, file_name
                                    )

                                    if processed.get("success"):
                                        content = processed.get("text", "")
                                        file_type = processed.get("file_type", "")

                                        file_summary += f"\n**File: {file_name}** (Type: {file_type})\n"
                                        file_summary += f"Path: {file_path}\n"

                                        # Limit content to first 2000 characters per file
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

            # PRIORITY 2: Fallback to browser-uploaded files if no path files available
            if file_context and not has_path_files:
                try:
                    yield f"data: {json.dumps({'type': 'progress', 'message': f'📎 Processing {len(file_context)} uploaded file(s)...'})}\n\n"

                    file_summary += "\n\n**Uploaded Files:**\n"
                    for file_info in file_context:
                        filename = file_info.get("filename", "Unknown")
                        content = file_info.get("content", "")
                        file_type = file_info.get("file_type", "")

                        file_summary += f"\n**File: {filename}** (Type: {file_type})\n"
                        # Limit content to first 2000 characters per file
                        if content:
                            file_summary += f"{content[:2000]}\n"
                            if len(content) > 2000:
                                file_summary += f"... (truncated, total {len(content)} characters)\n"
                            has_uploaded_files = True

                    if has_uploaded_files:
                        yield f"data: {json.dumps({'type': 'progress', 'message': '✅ Uploaded files processed'})}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({'type': 'warning', 'message': f'⚠️ File processing warning: {str(e)}'})}\n\n"

            # PRIORITY 3: Use both if available
            elif file_context and has_path_files:
                try:
                    yield f"data: {json.dumps({'type': 'progress', 'message': f'📎 Adding {len(file_context)} uploaded file(s) to context...'})}\n\n"

                    file_summary += "\n\n**Additional Uploaded Files:**\n"
                    for file_info in file_context:
                        filename = file_info.get("filename", "Unknown")
                        content = file_info.get("content", "")
                        file_type = file_info.get("file_type", "")

                        file_summary += f"\n**File: {filename}** (Type: {file_type})\n"
                        if content:
                            file_summary += f"{content[:2000]}\n"
                            if len(content) > 2000:
                                file_summary += f"... (truncated)\n"

                    yield f"data: {json.dumps({'type': 'progress', 'message': '✅ Combined path and uploaded files'})}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({'type': 'warning', 'message': f'⚠️ Additional file warning: {str(e)}'})}\n\n"

            # Build final context message
            context_status = ""
            if has_path_files and has_uploaded_files:
                context_status = "Using configured paths + uploaded files"
            elif has_path_files:
                context_status = "Using configured paths"
            elif has_uploaded_files:
                context_status = "Using uploaded files"
            else:
                context_status = "No file context - using question only"
                yield f"data: {json.dumps({'type': 'info', 'message': 'ℹ️ No files available - configure paths or upload files for better insights'})}\n\n"

            # Combine file summary with question
            if file_summary:
                question_with_files = f"{file_summary}\n\n**User Question:** {question}"
            else:
                question_with_files = question

            # Get AI response with progress tracking
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


@ai_chat_bp.route("/upload", methods=["POST"])
def upload_files():
    """
    Handle file uploads and extract content

    Accepts multiple files via multipart/form-data
    Returns extracted text/data from each file
    """
    try:
        if "files" not in request.files:
            return jsonify({"success": False, "error": "No files uploaded"}), 400

        files = request.files.getlist("files")

        if not files or len(files) == 0:
            return jsonify({"success": False, "error": "No files provided"}), 400

        # Import file processor
        from src.utils.file_processor import process_uploaded_file

        file_data = []

        for file in files:
            if file.filename == "":
                continue

            # Read file bytes
            file_bytes = file.read()

            # Process file
            result = process_uploaded_file(file_bytes, file.filename)

            if result.get("success"):
                file_data.append(
                    {
                        "filename": result["filename"],
                        "file_type": result["file_type"],
                        "content": result.get("text", ""),
                        "metadata": {
                            k: v
                            for k, v in result.items()
                            if k not in ["filename", "file_type", "text", "success"]
                        },
                    }
                )
            else:
                file_data.append(
                    {
                        "filename": file.filename,
                        "error": result.get("error", "Processing failed"),
                    }
                )

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
            "file_data": file_data,
        }

        # Add cross-reference analysis if available
        if cross_reference_analysis:
            response_data["cross_reference_analysis"] = cross_reference_analysis

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@ai_chat_bp.route("/export-pdf", methods=["POST"])
def export_pdf():
    """
    Generate PDF export from AI response content

    Request JSON:
    {
        "content": "AI response text",
        "store_id": "VM_DL_001"  // Optional
    }
    """
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
    """
    Generate DOCX export from AI response content

    Request JSON:
    {
        "content": "AI response text",
        "store_id": "VM_DL_001"  // Optional
    }
    """
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
    """Get all configured local paths"""
    try:
        paths = path_manager.get_all_paths()
        return jsonify({"success": True, "paths": paths})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_chat_bp.route("/paths", methods=["POST"])
def add_configured_path():
    """Add a new path configuration"""
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
    """Remove a path configuration"""
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
    """Scan a configured path and count files"""
    try:
        result = path_manager.scan_path(path_id)
        return jsonify({"success": True, **result})

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_chat_bp.route("/paths/<int:path_id>/files", methods=["GET"])
def get_path_files(path_id: int):
    """Get list of files from a configured path"""
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
    """Search for files across configured paths"""
    try:
        query = request.args.get("query")

        if not query:
            return jsonify({"error": "Query parameter is required"}), 400

        limit = int(request.args.get("limit", 50))

        results = path_manager.search_files(query, limit=limit)

        return jsonify({"success": True, "results": results, "count": len(results)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
