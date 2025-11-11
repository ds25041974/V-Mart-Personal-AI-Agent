"""
V-Mart Personal AI Agent - Main Flask Application
Enhanced with multi-connector support and advanced features

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import os
import subprocess
from datetime import datetime

from agent.gemini_agent import GeminiAgent
from auth import google_auth
from backend.ai_insights import AIInsightsEngine
from backend.config_manager import config_manager
from backend.db_manager import db_manager
from backend.rbac import Permission, rbac_manager
from connectors.data_reader import DataReaderConnector
from connectors.local_files import LocalFilesConnector
from flask import Flask, jsonify, redirect, render_template, request, send_file, session
from scheduler.task_scheduler import TaskScheduler

# Import PDF OCR utilities
try:
    from utils.pdf_ocr import PDFOCRExtractor, analyze_pdf_structure

    PDF_OCR_AVAILABLE = True
except ImportError:
    PDF_OCR_AVAILABLE = False
    print(
        "Warning: PDF OCR not available. Install dependencies: pip install pytesseract pdf2image PyPDF2"
    )

# Import Export utilities
try:
    from utils.export_utils import ExportGenerator

    EXPORT_AVAILABLE = True
except ImportError:
    EXPORT_AVAILABLE = False
    print(
        "Warning: Export functionality not available. Install dependencies: pip install reportlab xlsxwriter"
    )

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# Configure Google OAuth
app.config["GOOGLE_CLIENT_ID"] = os.environ.get("GOOGLE_CLIENT_ID")
app.config["GOOGLE_CLIENT_SECRET"] = os.environ.get("GOOGLE_CLIENT_SECRET")
google_auth.init_app(app)

# Initialize Gemini Agent
gemini_agent = GeminiAgent(api_key=os.environ.get("GEMINI_API_KEY") or "")

# Initialize Local Files Connector
local_connector = LocalFilesConnector(base_path=os.path.expanduser("~"))

# Initialize Data Reader Connector
data_reader = DataReaderConnector()

# Initialize Task Scheduler
scheduler = TaskScheduler()
scheduler.start()

# Initialize AI Insights Engine
ai_insights = AIInsightsEngine(api_key=os.environ.get("GEMINI_API_KEY") or "")

# Initialize demo admin user if not exists
demo_email = "demo@vmart.co.in"
if not rbac_manager.get_user(demo_email):
    rbac_manager.create_user(demo_email, demo_email, ["admin"])
    print(f"✓ Created demo admin user: {demo_email}")

# Register Store Management Blueprint
try:
    from web.stores_routes import stores_bp

    app.register_blueprint(stores_bp)
    print("✓ Store Management routes registered at /stores")
except Exception as e:
    print(f"⚠ Store Management routes not available: {e}")

# Register Analytics Blueprint
try:
    from web.analytics_routes import analytics_bp

    app.register_blueprint(analytics_bp)
    print("✓ Analytics & Insights routes registered at /analytics")
except Exception as e:
    print(f"⚠ Analytics routes not available: {e}")

# Register Retail Intelligence Blueprint (NEW)
try:
    from web.intelligence_routes import intelligence_bp

    app.register_blueprint(intelligence_bp)
    print("✓ Retail Intelligence AI routes registered at /api/intelligence")
except Exception as e:
    print(f"⚠ Retail Intelligence routes not available: {e}")

# AI Chat features now integrated into main interface
# No separate /ai-chat routes needed


# Helper function to format AI responses for better readability
def format_ai_response(response):
    """
    Format AI response with proper HTML structure for better display.
    Converts markdown-style formatting to HTML.
    """
    import re

    # Convert **bold** to <strong>
    response = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", response)

    # Convert section headers (lines starting with **) to h4
    response = re.sub(
        r"^<strong>(.+?)</strong>$", r"<h4>\1</h4>", response, flags=re.MULTILINE
    )

    # Convert tables (lines with | characters) to HTML tables
    lines = response.split("\n")
    formatted_lines = []
    in_table = False
    table_lines = []

    for line in lines:
        if "|" in line and line.strip().startswith("|"):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
        else:
            if in_table:
                # Process accumulated table
                formatted_lines.append(convert_table_to_html(table_lines))
                in_table = False
                table_lines = []
            formatted_lines.append(line)

    # Process any remaining table
    if in_table and table_lines:
        formatted_lines.append(convert_table_to_html(table_lines))

    response = "\n".join(formatted_lines)

    # Convert double newlines to paragraphs
    response = re.sub(r"\n\n+", "</p><p>", response)
    response = "<p>" + response + "</p>"

    # Clean up empty paragraphs
    response = re.sub(r"<p>\s*</p>", "", response)

    return response


def convert_table_to_html(table_lines):
    """Convert markdown-style table to HTML table"""
    if not table_lines:
        return ""

    html = '<table class="ai-table" style="border-collapse: collapse; margin: 15px 0; width: 100%;">'

    for i, line in enumerate(table_lines):
        cells = [
            cell.strip() for cell in line.split("|")[1:-1]
        ]  # Remove first and last empty splits

        # Skip separator lines (----)
        if all(set(cell.strip()) <= {"-", " ", ":"} for cell in cells):
            continue

        if i == 0:
            # Header row
            html += "<thead><tr>"
            for cell in cells:
                html += f'<th style="border: 1px solid #ddd; padding: 10px; background: #667eea; color: white; text-align: left;">{cell}</th>'
            html += "</tr></thead><tbody>"
        else:
            # Data row
            html += "<tr>"
            for cell in cells:
                html += (
                    f'<td style="border: 1px solid #ddd; padding: 10px;">{cell}</td>'
                )
            html += "</tr>"

    html += "</tbody></table>"
    return html


@app.route("/")
def index():
    if "user" in session:
        return render_template("index.html", user=session["user"])

    # Always show email login form (simplified mode)
    return """
    <html>
    <head>
        <title>V-Mart AI Agent - Login</title>
        <style>
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
            .login-container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); max-width: 400px; width: 100%; }
            h1 { color: #333; margin-bottom: 10px; font-size: 28px; }
            .subtitle { color: #666; margin-bottom: 30px; font-size: 14px; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; color: #555; font-weight: 500; }
            input[type="email"], input[type="text"] { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; box-sizing: border-box; }
            input[type="email"]:focus, input[type="text"]:focus { outline: none; border-color: #4285f4; }
            button { width: 100%; padding: 12px; background: #4285f4; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: 500; transition: background 0.3s; }
            button:hover { background: #357ae8; }
            .note { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; font-size: 13px; color: #666; }
            .note strong { color: #333; }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>🤖 V-Mart AI Agent</h1>
            <p class="subtitle">Login to access your AI assistant</p>
            <form action="/email-login" method="post">
                <div class="form-group">
                    <label for="email">Email Address</label>
                    <input type="email" id="email" name="email" placeholder="your.email@vmart.co.in" required>
                </div>
                <div class="form-group">
                    <label for="name">Your Name</label>
                    <input type="text" id="name" name="name" placeholder="Your Full Name" required>
                </div>
                <button type="submit">Login</button>
            </form>
            <div class="note">
                <strong>📧 Allowed domains:</strong> vmart.co.in, vmartretail.com, limeroad.com<br>
                <strong>🔐 Note:</strong> For Google Drive/Gmail access, you'll need to authorize with your Google account separately.
            </div>
        </div>
    </body>
    </html>
    """


@app.route("/email-login", methods=["POST"])
def email_login():
    """Simple email-based login without OAuth for basic access"""
    email = request.form.get("email", "").strip()
    name = request.form.get("name", "").strip()

    if not email or not name:
        return "Email and name are required", 400

    # Validate email domain
    allowed_domains = os.getenv(
        "ALLOWED_DOMAINS", "vmart.co.in,vmartretail.com,limeroad.com"
    ).split(",")
    email_domain = email.split("@")[-1] if "@" in email else ""

    if email_domain not in allowed_domains:
        return (
            f"""
        <html>
        <head><title>Access Denied</title></head>
        <body style="font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; text-align: center;">
            <h1 style="color: #d32f2f;">❌ Access Denied</h1>
            <p>Your email domain <strong>{email_domain}</strong> is not authorized.</p>
            <p>Allowed domains: {", ".join(allowed_domains)}</p>
            <a href="/" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #4285f4; color: white; text-decoration: none; border-radius: 5px;">Back to Login</a>
        </body>
        </html>
        """,
            403,
        )

    # Create session
    session["user"] = {
        "email": email,
        "name": name,
        "picture": "",
        "hd": email_domain,
    }

    # Create user in RBAC if doesn't exist
    if not rbac_manager.get_user(email):
        rbac_manager.create_user(email, name, ["user"])

    return redirect("/")


@app.route("/demo-login", methods=["POST"])
def demo_login():
    """Demo login for testing without OAuth"""
    session["user"] = {
        "email": "demo@vmart.co.in",
        "name": "Demo User",
        "picture": "",
        "hd": "vmart.co.in",
    }
    return redirect("/")


@app.route("/ask", methods=["POST"])
def ask():
    """
    Enhanced ask function with priority: browsed file > comparison mode > local files > other sources
    Smart greeting detection - only analyze files when relevant to the query
    """
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    prompt = data.get("prompt")
    use_context = data.get("use_context", True)
    browsed_file = data.get("browsed_file")  # {name, content, source}

    if not prompt:
        return jsonify({"error": "Please provide a prompt."}), 400

    # Enhanced: Intelligent context gathering with priority
    enhanced_prompt = prompt
    context_info = []

    try:
        prompt_lower = prompt.lower().strip()

        # SMART DETECTION: Check if it's just a greeting or casual query
        greetings = [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "how are you",
            "what's up",
            "whats up",
            "sup",
            "greetings",
        ]
        simple_queries = [
            "thanks",
            "thank you",
            "ok",
            "okay",
            "yes",
            "no",
            "sure",
            "got it",
            "understood",
            "bye",
            "goodbye",
        ]

        # Check if the entire prompt is just a greeting or simple response
        is_simple_greeting = (
            prompt_lower in greetings
            or prompt_lower in simple_queries
            or any(prompt_lower == greeting for greeting in greetings)
            or (
                len(prompt.split()) <= 3
                and any(greeting in prompt_lower for greeting in greetings)
            )
        )

        # If it's just a greeting, respond naturally without analyzing files
        if is_simple_greeting:
            response = gemini_agent.get_response(prompt, use_context=use_context)
            formatted_response = format_ai_response(response)
            return jsonify({"response": formatted_response})

        # PRIORITY 1: If user has browsed a file AND asking about it, use it directly
        if browsed_file and browsed_file.get("content"):
            file_name = browsed_file.get("name", "unknown file")
            file_content = browsed_file.get("content", "")

            # Check if the question is actually about the file or something else
            file_question_keywords = [
                "this file",
                "the file",
                "document",
                "pdf",
                "content",
                "data",
                "analyze",
                "summary",
                "summarize",
                "what does",
                "explain",
                "show me",
                "find",
                "search",
                "look for",
                "contains",
                "about this",
                "in this",
                "from this",
                "based on",
                "according to",
            ]

            asking_about_file = any(
                keyword in prompt_lower for keyword in file_question_keywords
            )

            # If NOT asking about the file, ignore it and respond normally
            if not asking_about_file and not (
                "compare" in prompt_lower or "versus" in prompt_lower
            ):
                response = gemini_agent.get_response(prompt, use_context=use_context)
                formatted_response = format_ai_response(response)
                return jsonify({"response": formatted_response})

            # Check if user wants to compare with local files
            comparison_keywords = [
                "compare",
                "difference",
                "diff",
                "versus",
                "vs",
                "match",
                "similar",
            ]
            wants_comparison = any(
                keyword in prompt_lower for keyword in comparison_keywords
            )

            if wants_comparison:
                # User wants to compare browsed file with local files
                context_info.append(f"Browsed file: {file_name}")
                enhanced_prompt = f"""**BROWSED FILE:** {file_name}

**CONTENT:**
{file_content[:8000]}

**USER'S REQUEST:** {prompt}

The user wants to compare this browsed file with local system files. First, analyze the browsed file above, then search for and compare with relevant local files."""

                # Search local files for comparison
                enhanced_prompt = search_local_files_for_comparison(
                    enhanced_prompt, prompt_lower, context_info
                )
            else:
                # User just wants to work with the browsed file
                context_info.append(f"Using browsed file: {file_name}")
                enhanced_prompt = f"""**CONTEXT:** You are analyzing the browsed file '{file_name}'.

**FILE CONTENT:**
{file_content[:10000]}

**USER'S QUESTION:** {prompt}

Please answer the question based on the file content above. Be specific and reference relevant parts of the file."""

        # PRIORITY 2: No browsed file - check if user is explicitly asking about files/data sources
        else:
            # Only search files/sources if explicitly mentioned
            keywords_doc = [
                "document",
                "doc",
                "file",
                "sheet",
                "slide",
                "presentation",
                "pdf",
                "excel",
                "word",
                "ppt",
            ]
            keywords_local = [
                "local file",
                "my file",
                "my computer",
                "my system",
                "my folder",
                "my desktop",
                "my documents",
                "my downloads",
                "find file",
                "search file",
                "open file",
            ]
            keywords_progress = [
                "progress report",
                "status report",
                "my report",
                "data file",
                "analysis file",
                "metrics file",
            ]

            # Only search local files if EXPLICITLY asking for them
            should_search_local = any(
                keyword in prompt_lower
                for keyword in keywords_local + keywords_progress
            ) or (
                any(keyword in prompt_lower for keyword in keywords_doc)
                and any(
                    word in prompt_lower
                    for word in ["show", "find", "search", "open", "get", "read"]
                )
            )

            if should_search_local:
                enhanced_prompt = search_local_files_for_comparison(
                    prompt, prompt_lower, context_info
                )

            # Add notes about other sources if mentioned
            if any(
                word in prompt_lower for word in ["email", "gmail", "mail", "inbox"]
            ):
                enhanced_prompt += (
                    "\n\n📧 Note: Email access requires Google OAuth authentication.\n"
                )
                context_info.append("Email search (requires OAuth)")

            if any(word in prompt_lower for word in ["google drive", "drive", "cloud"]):
                enhanced_prompt += (
                    "\n\n☁️ Note: Google Drive access requires OAuth authentication.\n"
                )
                context_info.append("Drive search (requires OAuth)")

            if any(
                word in prompt_lower for word in ["screen", "screenshot", "display"]
            ):
                enhanced_prompt += (
                    "\n\n🖥️ Note: Screen capture functionality not yet implemented.\n"
                )
                context_info.append("Screen capture (pending)")

    except Exception as e:
        print(f"Error in context gathering: {e}")

    # Add formatting instructions
    formatting_instructions = """

**RESPONSE FORMATTING REQUIREMENTS:**
- Write in clear, readable paragraphs with proper punctuation
- Use **bold headers** for major sections
- Present data in table format with pipe characters (|) when applicable
- Structure responses with: context, findings, insights, recommendations
- Write professionally with proper grammar
"""

    enhanced_prompt += formatting_instructions

    # ========== ANALYTICS CONTEXT INTEGRATION ==========
    # Detect if this is a business/analytics question and add relevant data
    analytics_context_text = None
    try:
        from analytics.context_provider import AnalyticsContextProvider

        analytics_keywords = [
            "sales",
            "revenue",
            "inventory",
            "stock",
            "weather",
            "competition",
            "competitor",
            "market",
            "trend",
            "growth",
            "performance",
            "store",
            "recommend",
            "insight",
            "analysis",
            "forecast",
            "demand",
        ]

        # Check if question is analytics-related
        is_analytics_query = any(
            keyword in prompt_lower for keyword in analytics_keywords
        )

        if is_analytics_query:
            # Get analytics context
            context_provider = AnalyticsContextProvider()
            analytics_context = context_provider.get_context_for_prompt(prompt, days=30)

            if analytics_context.get("has_data"):
                # Format context for AI
                analytics_context_text = context_provider.format_context_for_ai(
                    analytics_context
                )
                context_info.append(
                    f"Analytics: {analytics_context.get('context_summary', 'Live data')}"
                )

    except Exception as e:
        print(f"⚠ Analytics context not available: {e}")

    # Get AI response with analytics context
    response = gemini_agent.get_response(
        enhanced_prompt,
        use_context=use_context,
        analytics_context=analytics_context_text,
    )

    # Format the response
    formatted_response = format_ai_response(response)

    # Add source attribution
    if context_info:
        formatted_response = f"<p><strong>📚 Sources:</strong> {', '.join(context_info)}</p>{formatted_response}"

    return jsonify({"response": formatted_response})


def search_local_files_for_comparison(base_prompt, prompt_lower, context_info):
    """Helper function to search local files and add to prompt"""
    enhanced_prompt = base_prompt

    try:
        # Search common document locations
        search_paths = [
            ("Documents", os.path.expanduser("~/Documents")),
            ("Desktop", os.path.expanduser("~/Desktop")),
            ("Downloads", os.path.expanduser("~/Downloads")),
        ]

        all_files_found = []

        # Extract potential search terms from prompt
        words = prompt_lower.split()
        search_terms = [
            w
            for w in words
            if len(w) > 4
            and w
            not in [
                "about",
                "please",
                "could",
                "would",
                "should",
                "there",
                "where",
                "which",
                "compare",
                "comparison",
            ]
        ]

        for location_name, base_path in search_paths:
            if not os.path.exists(base_path):
                continue

            try:
                # Walk through directories (limited depth)
                for root, dirs, files in os.walk(base_path):
                    # Limit depth to avoid too much scanning
                    depth = root.count(os.sep) - base_path.count(os.sep)
                    if depth > 2:
                        continue

                    # Skip hidden directories
                    dirs[:] = [d for d in dirs if not d.startswith(".")]

                    for filename in files:
                        # Skip hidden files
                        if filename.startswith("."):
                            continue

                        # Check if it's a document file
                        doc_extensions = [
                            ".pdf",
                            ".doc",
                            ".docx",
                            ".txt",
                            ".xlsx",
                            ".xls",
                            ".ppt",
                            ".pptx",
                            ".csv",
                            ".md",
                            ".rtf",
                        ]

                        is_document = any(
                            filename.lower().endswith(ext) for ext in doc_extensions
                        )

                        if not is_document:
                            continue

                        # Check if filename matches search terms
                        filename_lower = filename.lower()
                        matches = not search_terms or any(
                            term in filename_lower for term in search_terms
                        )

                        if matches:
                            file_path = os.path.join(root, filename)
                            file_info = {
                                "name": filename,
                                "path": file_path,
                                "location": location_name,
                                "size": os.path.getsize(file_path),
                                "modified": os.path.getmtime(file_path),
                            }
                            all_files_found.append(file_info)

                        # Limit total files
                        if len(all_files_found) >= 15:
                            break

                    if len(all_files_found) >= 15:
                        break

            except Exception as e:
                print(f"Error scanning {location_name}: {e}")
                continue

        # Process found files
        if all_files_found:
            # Sort by most recently modified
            all_files_found.sort(key=lambda x: x["modified"], reverse=True)

            context_info.append(
                f"Found {len(all_files_found)} documents in local system"
            )

            file_context = "\n\n📁 AVAILABLE LOCAL DOCUMENTS:\n"
            file_context += "=" * 60 + "\n"

            for idx, file_info in enumerate(all_files_found[:8], 1):
                file_size_kb = file_info["size"] / 1024
                file_context += f"\n{idx}. {file_info['name']}\n"
                file_context += f"   Location: {file_info['location']}\n"
                file_context += f"   Size: {file_size_kb:.1f} KB\n"
                file_context += f"   Path: {os.path.dirname(file_info['path'])}\n"

                # Try to read content preview for text files
                if file_info["name"].endswith((".txt", ".md", ".csv")):
                    try:
                        with open(
                            file_info["path"],
                            "r",
                            encoding="utf-8",
                            errors="ignore",
                        ) as f:
                            content = f.read(400)
                            if content.strip():
                                preview = content[:200].replace("\n", " ")
                                file_context += f"   Preview: {preview}...\n"
                    except Exception:
                        file_context += "   (Content preview unavailable)\n"

            file_context += "\n" + "=" * 60 + "\n"
            enhanced_prompt += file_context

        else:
            # No files found - guide the user
            enhanced_prompt += "\n\n📁 No matching documents found in:\n"
            enhanced_prompt += "   - ~/Documents\n   - ~/Desktop\n   - ~/Downloads\n"
            enhanced_prompt += "\nPlease specify exact file names or check these locations for your documents.\n"

    except Exception as e:
        print(f"Error searching local files: {e}")
        enhanced_prompt += f"\n\n(Note: Error accessing local files: {str(e)})\n"

    return enhanced_prompt


@app.route("/analyze", methods=["POST"])
def analyze():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    data_to_analyze = data.get("data")
    analysis_type = data.get("type", "general")

    if not data_to_analyze:
        return jsonify({"error": "Please provide data to analyze."}), 400

    # Add formatting instructions
    formatted_prompt = f"""Analyze the following data:

{data_to_analyze}

**FORMATTING REQUIREMENTS:**
- Write analysis in clear paragraphs with proper punctuation
- Use **bold headers** to organize different sections (Summary, Key Findings, Insights, Recommendations)
- If the data contains numbers or comparisons, present them in a table format using pipe (|) characters
- Provide analytical insights, not just descriptions
- Include actionable recommendations
- Use professional language with proper grammar

Analysis Type: {analysis_type}"""

    analysis = gemini_agent.get_response(formatted_prompt)
    formatted_analysis = format_ai_response(analysis)
    return jsonify({"analysis": formatted_analysis})


@app.route("/reasoning", methods=["POST"])
def reasoning():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    task = data.get("task")
    task_data = data.get("data")

    if not task:
        return jsonify({"error": "Please provide a task description."}), 400

    result = gemini_agent.reasoning_task(task, task_data)
    return jsonify(result)


@app.route("/summarize", methods=["POST"])
def summarize():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    document = data.get("document")
    summary_type = data.get("type", "brief")

    if not document:
        return jsonify({"error": "Please provide a document to summarize."}), 400

    summary = gemini_agent.summarize_document(document, summary_type=summary_type)
    return jsonify({"summary": summary})


@app.route("/decision-support", methods=["POST"])
def decision_support():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    decision = data.get("decision")
    context = data.get("context")
    options = data.get("options", [])

    if not decision or not context:
        return jsonify({"error": "Please provide decision and context."}), 400

    # Enhanced prompt with formatting
    formatted_prompt = f"""You are a decision support analyst. Help analyze this decision:

**Decision to Make:** {decision}

**Context:** {context}

**Options to Consider:**
{chr(10).join(f"- {opt}" for opt in options) if options else "No specific options provided"}

**RESPONSE FORMAT:**
Please provide your analysis using the following structure:

**Decision Overview**
[Brief summary of the decision and its importance]

**Analysis of Options**
[Present a comparison table if multiple options exist, using | for columns. Include pros/cons for each]

**Key Insights**
[Analytical insights about the decision, considering risks, benefits, and implications]

**Recommendation**
[Clear recommendation with reasoning]

**Next Steps**
[Actionable steps to implement the decision]

Use proper paragraphs, tables for comparisons, and bold headers. Write professionally with proper punctuation."""

    result_text = gemini_agent.get_response(formatted_prompt)
    formatted_result = format_ai_response(result_text)

    return jsonify({"analysis": formatted_result})


@app.route("/files/list", methods=["GET"])
def list_files():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    extension = request.args.get("extension")
    files = local_connector.list_files(extension=extension)
    return jsonify({"files": files[:100]})  # Limit to 100 files


@app.route("/files/search", methods=["GET"])
def search_files():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Please provide a search query."}), 400

    files = local_connector.search_files(query)
    return jsonify({"files": files[:50]})  # Limit to 50 files


@app.route("/files/read", methods=["POST"])
def read_file():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    file_path = data.get("path")

    if not file_path:
        return jsonify({"error": "Please provide a file path."}), 400

    content = local_connector.read_file(file_path)
    if content is None:
        return jsonify({"error": "Failed to read file."}), 500

    return jsonify({"content": content})


@app.route("/analyze-file", methods=["POST"])
def analyze_file():
    """Analyze file content with Gemini AI for insights and recommendations"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    filename = data.get("filename", "file")
    content = data.get("content", "")

    if not content:
        return jsonify({"error": "No file content provided"}), 400

    try:
        # Create enhanced analysis prompt with formatting instructions
        prompt = f"""You are an expert analyst. Analyze the file '{filename}' and provide a comprehensive, well-formatted analysis.

**FORMATTING REQUIREMENTS:**
- Use proper paragraph structure for text explanations
- Use clear section headers in **bold** to organize your response
- For data or structured information, present it in tabular format using pipes (|) for columns
- Use proper punctuation (commas, periods) in all sentences
- Write in a professional, analytical manner
- Always include an "Insights" section and a "Recommendations" section

**FILE CONTENT:**
{content[:10000]}

**ANALYSIS STRUCTURE:**
Please provide your analysis in the following format:

**Summary**
[Write a clear paragraph summarizing what this file contains, its purpose, and main components]

**Key Findings**
[Present important discoveries about the file. If there's data, use a table format with headers]

**Insights**
[Provide analytical insights about patterns, quality, completeness, or significance of the content]

**Recommendations**
[Give actionable recommendations for improvements, next steps, or best practices]

**Potential Issues**
[Identify any concerns, risks, or areas that need attention]

Remember: Write naturally with proper grammar, use tables for structured data, and make the analysis clear and actionable."""

        # Get analysis from Gemini
        response = gemini_agent.get_response(prompt)

        # Format the response for better HTML display
        formatted_response = format_ai_response(response)

        return jsonify({"analysis": formatted_response})
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


@app.route("/chat-about-file", methods=["POST"])
def chat_about_file():
    """Chat with Gemini AI about a specific file"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    filename = data.get("filename", "file")
    content = data.get("content", "")
    question = data.get("question", "")

    if not content or not question:
        return jsonify({"error": "File content and question are required"}), 400

    try:
        # Create context-aware prompt with formatting instructions
        prompt = f"""You are analyzing the file '{filename}'. 

**FILE CONTENT:**
{content[:8000]}

**USER'S QUESTION:** {question}

**RESPONSE FORMATTING REQUIREMENTS:**
- Write your answer in clear, readable paragraphs with proper punctuation
- Use **bold headers** to organize different sections if the answer has multiple parts
- If your answer includes data or comparisons, present them in a table format using pipe characters (|)
- Always provide insights or context, not just raw information
- If relevant, include a brief recommendation or next steps
- Use professional language with proper grammar, commas, and periods

Please answer the question based on the file content above. Be specific, analytical, and reference relevant parts of the file."""

        # Get response from Gemini
        response = gemini_agent.get_response(prompt)

        # Format the response for better display
        formatted_response = format_ai_response(response)

        return jsonify({"answer": formatted_response})
    except Exception as e:
        return jsonify({"error": f"Chat failed: {str(e)}"}), 500


@app.route("/analyze-pdf", methods=["POST"])
def analyze_pdf():
    """Analyze PDF file using OCR and provide AI insights"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    if not PDF_OCR_AVAILABLE:
        return jsonify(
            {"error": "PDF OCR not available. Please install required dependencies."}
        ), 500

    try:
        # Check if file is uploaded
        if "file" not in request.files:
            return jsonify({"error": "No PDF file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "File must be a PDF"}), 400

        # Read PDF bytes
        pdf_bytes = file.read()

        # Extract text using OCR
        extractor = PDFOCRExtractor()
        extraction_result = extractor.extract_from_bytes(pdf_bytes)

        if extraction_result.get("error"):
            return jsonify(
                {"error": f"PDF extraction failed: {extraction_result['error']}"}
            ), 500

        extracted_text = extraction_result.get("text", "")

        if not extracted_text.strip():
            return jsonify({"error": "No text could be extracted from the PDF"}), 400

        # Prepare analysis prompt
        prompt = f"""You are analyzing a PDF document: '{file.filename}'

**EXTRACTION METHOD:** {extraction_result.get("method", "unknown")}
**PAGE COUNT:** {extraction_result.get("page_count", 0)} pages
**TOTAL CHARACTERS:** {len(extracted_text)}

**EXTRACTED TEXT:**
{extracted_text[:10000]}

Please provide a comprehensive analysis in the following format:

**Summary**
[Summarize the document's purpose, type, and main content in a clear paragraph]

**Key Findings**
[Present the most important information found in the document. Use a table format if there's structured data]

| Finding | Details |
|---------|---------|
| Document Type | [e.g., Invoice, Report, Contract] |
| Key Dates | [Any important dates mentioned] |
| Key Figures | [Important numbers or metrics] |
| Main Topics | [Primary subjects covered] |

**Data Insights**
[Provide analytical insights about the data quality, completeness, patterns, or significance]

**Recommendations**
[Give actionable recommendations based on the document content]

**Potential Issues**
[Identify any concerns, missing information, or areas needing attention]

Remember: Write naturally with proper grammar and punctuation, use tables for structured data, and make the analysis clear and actionable."""

        # Get analysis from Gemini
        response = gemini_agent.get_response(prompt)

        # Format the response
        formatted_response = format_ai_response(response)

        return jsonify(
            {
                "analysis": formatted_response,
                "filename": file.filename,
                "extraction_method": extraction_result.get("method"),
                "page_count": extraction_result.get("page_count"),
                "char_count": len(extracted_text),
                "extracted_text": extracted_text[:5000],  # First 5000 chars for preview
            }
        )

    except Exception as e:
        return jsonify({"error": f"PDF analysis failed: {str(e)}"}), 500


@app.route("/extract-pdf-text", methods=["POST"])
def extract_pdf_text():
    """Extract text from PDF using OCR (no AI analysis)"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    if not PDF_OCR_AVAILABLE:
        return jsonify({"error": "PDF OCR not available"}), 500

    try:
        if "file" not in request.files:
            return jsonify({"error": "No PDF file uploaded"}), 400

        file = request.files["file"]

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "File must be a PDF"}), 400

        # Extract text
        pdf_bytes = file.read()
        extractor = PDFOCRExtractor()
        result = extractor.extract_from_bytes(pdf_bytes)

        return jsonify(
            {
                "text": result.get("text", ""),
                "pages": result.get("pages", []),
                "page_count": result.get("page_count", 0),
                "method": result.get("method", "unknown"),
                "filename": file.filename,
            }
        )

    except Exception as e:
        return jsonify({"error": f"Text extraction failed: {str(e)}"}), 500


@app.route("/clear-history", methods=["POST"])
def clear_history():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    gemini_agent.clear_history()
    return jsonify({"status": "success"})


@app.route("/github/commit", methods=["POST"])
def github_commit():
    """Auto-commit changes to GitHub"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    commit_message = data.get(
        "message", f"Auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    try:
        # Get current directory (project root)
        project_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        # Run git commands
        commands = [
            ["git", "add", "."],
            ["git", "commit", "-m", commit_message],
            ["git", "push", "origin", "main"],
        ]

        results = []
        for cmd in commands:
            result = subprocess.run(
                cmd, cwd=project_dir, capture_output=True, text=True, timeout=30
            )
            results.append(
                {
                    "command": " ".join(cmd),
                    "output": result.stdout,
                    "error": result.stderr,
                    "returncode": result.returncode,
                }
            )

            # Stop if command failed
            if result.returncode != 0 and "nothing to commit" not in result.stdout:
                return jsonify(
                    {
                        "status": "error",
                        "message": f"Git command failed: {' '.join(cmd)}",
                        "details": results,
                    }
                ), 500

        return jsonify(
            {
                "status": "success",
                "message": "Changes committed and pushed to GitHub",
                "details": results,
            }
        )

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Git operation timed out"}), 500
    except Exception as e:
        return jsonify({"error": f"GitHub commit failed: {str(e)}"}), 500


@app.route("/github/status", methods=["GET"])
def github_status():
    """Get git status of the repository"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        project_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=10,
        )

        has_changes = bool(result.stdout.strip())

        return jsonify(
            {
                "has_changes": has_changes,
                "status": result.stdout,
                "clean": not has_changes,
            }
        )

    except Exception as e:
        return jsonify({"error": f"Failed to get git status: {str(e)}"}), 500


@app.route("/scheduler/tasks", methods=["GET"])
def list_tasks():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    tasks = scheduler.list_tasks()
    return jsonify({"tasks": tasks})


@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "healthy",
            "scheduler_running": scheduler.running,
            "user_authenticated": "user" in session,
        }
    )


# Data Reading API Endpoints


@app.route("/data/read-active-screen", methods=["POST"])
def read_active_screen():
    """Read data from the currently active application"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    include_hidden = data.get("include_hidden", True)

    result = data_reader.read_active_screen_data(include_hidden=include_hidden)
    return jsonify(result)


@app.route("/data/read-excel", methods=["POST"])
def read_excel():
    """Read data from Excel file"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    file_path = data.get("file_path")
    include_hidden = data.get("include_hidden", True)
    active_sheet_only = data.get("active_sheet_only", False)

    if active_sheet_only:
        result = data_reader.read_excel_active_sheet(
            file_path=file_path, include_hidden=include_hidden
        )
    else:
        result = data_reader.read_excel_data(
            file_path=file_path, include_hidden=include_hidden
        )

    return jsonify(result)


@app.route("/data/read-google-sheets", methods=["POST"])
def read_google_sheets():
    """Read data from Google Sheets"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    spreadsheet_id = data.get("spreadsheet_id")
    include_hidden = data.get("include_hidden", True)

    result = data_reader.read_google_sheets_data(
        spreadsheet_id=spreadsheet_id, include_hidden=include_hidden
    )
    return jsonify(result)


@app.route("/data/read-powerpoint", methods=["POST"])
def read_powerpoint():
    """Read data from PowerPoint presentation"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    file_path = data.get("file_path")

    result = data_reader.read_powerpoint_data(file_path=file_path)
    return jsonify(result)


@app.route("/data/read-email", methods=["POST"])
def read_email():
    """Read email data from Gmail"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    max_results = data.get("max_results", 10)
    query = data.get("query", "")

    result = data_reader.read_email_data(max_results=max_results, query=query)
    return jsonify(result)


@app.route("/data/detect-application", methods=["GET"])
def detect_application():
    """Detect the currently active application"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    app_info = data_reader.detect_active_application()
    return jsonify(app_info)


@app.route("/data/format-summary", methods=["POST"])
def format_summary():
    """Get a formatted summary of data"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    if "data" not in data:
        return jsonify({"error": "Please provide data to summarize"}), 400

    summary = data_reader.format_for_chatbot(data["data"])
    return jsonify({"summary": summary})


# Backend Management API Endpoints


@app.route("/backend/connections", methods=["GET"])
def list_connections():
    """List all database connections"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    connections = config_manager.list_database_connections()
    return jsonify({"connections": connections})


@app.route("/backend/connections", methods=["POST"])
def create_connection():
    """Create a new database connection"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    name = data.get("name")
    db_type = data.get("type")
    params = data.get("params", {})

    if not name or not db_type:
        return jsonify({"error": "Name and type are required"}), 400

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.DB_ADMIN
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    config_manager.add_database_connection(name, db_type, params)
    return jsonify({"status": "success", "connection": name})


@app.route("/backend/connections/<name>", methods=["DELETE"])
def delete_connection(name):
    """Delete a database connection"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.DB_ADMIN
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    success = config_manager.delete_credentials(f"db_{name}")
    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"error": "Connection not found"}), 404


@app.route("/backend/query", methods=["POST"])
def execute_query():
    """Execute a database query"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    connection_name = data.get("connection")
    query = data.get("query")

    if not connection_name or not query:
        return jsonify({"error": "Connection and query are required"}), 400

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.DB_QUERY
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    try:
        result = db_manager.execute_query(connection_name, query)
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/backend/schema/<connection_name>", methods=["GET"])
def get_schema(connection_name):
    """Get database schema"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.DB_CONNECT
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    try:
        schema = db_manager.get_schema(connection_name)
        return jsonify({"schema": schema})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/backend/ai/analyze", methods=["POST"])
def ai_analyze_data():
    """Analyze data using AI"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    if "data" not in data:
        return jsonify({"error": "Data is required"}), 400

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.AI_ANALYZE
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    try:
        # Initialize AI insights engine
        ai_engine = AIInsightsEngine(api_key=os.environ.get("GEMINI_API_KEY"))
        context = data.get("context", {})
        result = ai_engine.analyze_data(data["data"], context)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/backend/ai/recommend", methods=["POST"])
def ai_recommendations():
    """Get AI recommendations"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    if "data" not in data or "goal" not in data:
        return jsonify({"error": "Data and goal are required"}), 400

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.AI_RECOMMEND
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    try:
        # Initialize AI insights engine
        ai_engine = AIInsightsEngine(api_key=os.environ.get("GEMINI_API_KEY"))
        context = data.get("context", {})
        recommendations = ai_engine.generate_recommendations(
            data["data"], data["goal"], context
        )
        return jsonify({"recommendations": recommendations})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/backend/users", methods=["GET"])
def list_users():
    """List all users"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.USER_READ
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    users = rbac_manager.list_users()
    return jsonify({"users": users})


@app.route("/backend/users", methods=["POST"])
def create_user():
    """Create a new user"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    roles = data.get("roles", [])

    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.USER_WRITE
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    user_obj = rbac_manager.create_user(username, email, roles)
    if user_obj:
        return jsonify({"status": "success", "user": user_obj.to_dict()})
    else:
        return jsonify({"error": "User already exists"}), 409


@app.route("/backend/users/<username>", methods=["DELETE"])
def delete_user(username):
    """Delete a user"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.USER_DELETE
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    success = rbac_manager.delete_user(username)
    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"error": "User not found"}), 404


@app.route("/backend/users/<username>/roles", methods=["PUT"])
def update_user_roles(username):
    """Update user roles"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    roles = data.get("roles", [])

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.USER_WRITE
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    success = rbac_manager.update_user_roles(username, roles)
    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"error": "User not found"}), 404


@app.route("/backend/roles", methods=["GET"])
def list_roles():
    """List all roles"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.ROLE_READ
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    roles = rbac_manager.list_roles()
    return jsonify({"roles": roles})


@app.route("/backend/roles", methods=["POST"])
def create_role():
    """Create a new role"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    name = data.get("name")
    description = data.get("description", "")
    permissions = data.get("permissions", [])

    if not name:
        return jsonify({"error": "Role name is required"}), 400

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.ROLE_WRITE
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    role = rbac_manager.create_role(name, description, permissions)
    if role:
        return jsonify({"status": "success", "role": role.to_dict()})
    else:
        return jsonify({"error": "Role already exists"}), 409


@app.route("/backend/config", methods=["GET"])
def get_config():
    """Get configuration settings"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.SYSTEM_CONFIG
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    return jsonify({"config": config_manager.config})


@app.route("/backend/config", methods=["PUT"])
def update_config():
    """Update configuration settings"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    key = data.get("key")
    value = data.get("value")

    if not key:
        return jsonify({"error": "Configuration key is required"}), 400

    # Check if user has permission
    if not rbac_manager.check_permission(
        session["user"].get("email", "demo@vmart.co.in"), Permission.SYSTEM_CONFIG
    ):
        return jsonify({"error": "Insufficient permissions"}), 403

    config_manager.set_config(key, value)
    return jsonify({"status": "success"})


@app.route("/export/<format_type>", methods=["POST"])
def export_data(format_type):
    """
    Export analysis data with insights and recommendations in Excel or PDF format

    Args:
        format_type: 'excel' or 'pdf'
    """
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    if not EXPORT_AVAILABLE:
        return jsonify(
            {
                "error": "Export functionality not available. Please install required libraries."
            }
        ), 500

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided for export"}), 400

    try:
        export_gen = ExportGenerator()

        # Prepare export data
        export_data_dict = {
            "title": data.get("title", "AI Analysis Report"),
            "analysis": data.get("analysis", ""),
            "insights": data.get("insights", []),
            "recommendations": data.get("recommendations", []),
            "data_table": data.get("data_table", []),
            "metadata": {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user": session["user"].get("email", "Unknown"),
                "source": data.get("source", "V-Mart AI Agent"),
            },
        }

        if format_type.lower() == "excel":
            # Generate Excel file
            output = export_gen.generate_excel(export_data_dict)
            filename = f"AI_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment=True,
                download_name=filename,
            )

        elif format_type.lower() == "pdf":
            # Generate PDF file
            output = export_gen.generate_pdf(export_data_dict)
            filename = f"AI_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

            return send_file(
                output,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=filename,
            )

        else:
            return jsonify({"error": "Invalid format type. Use 'excel' or 'pdf'"}), 400

    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500


@app.route("/export/check", methods=["GET"])
def check_export_availability():
    """Check if export functionality is available"""
    return jsonify(
        {
            "excel_available": EXPORT_AVAILABLE,
            "pdf_available": EXPORT_AVAILABLE,
            "message": "Export functionality is ready"
            if EXPORT_AVAILABLE
            else "Install reportlab and xlsxwriter to enable exports",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
