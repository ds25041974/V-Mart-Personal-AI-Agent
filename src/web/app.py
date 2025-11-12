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
from typing import Optional

from flask import Flask, jsonify, redirect, render_template, request, send_file, session

from src.agent.gemini_agent import GeminiAgent
from src.auth import google_auth
from src.backend.ai_insights import AIInsightsEngine
from src.backend.config_manager import config_manager
from src.backend.db_manager import db_manager
from src.backend.rbac import Permission, rbac_manager
from src.connectors.data_reader import DataReaderConnector
from src.connectors.local_files import LocalFilesConnector
from src.scheduler.task_scheduler import TaskScheduler

# Import PDF OCR utilities
try:
    from src.utils.pdf_ocr import PDFOCRExtractor, analyze_pdf_structure

    PDF_OCR_AVAILABLE = True
except ImportError:
    PDF_OCR_AVAILABLE = False
    print(
        "Warning: PDF OCR not available. Install dependencies: pip install pytesseract pdf2image PyPDF2"
    )

# Import Export utilities
try:
    from src.utils.export_utils import ExportGenerator

    EXPORT_AVAILABLE = True
except ImportError:
    EXPORT_AVAILABLE = False
    print(
        "Warning: Export functionality not available. Install dependencies: pip install reportlab xlsxwriter"
    )

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# Disable template caching to force reload of changes
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

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

# Initialize Path Manager for local file access
from src.utils.path_manager import PathManager

path_manager = PathManager()

# Initialize Retail Intelligence Modules
try:
    from src.retail_intelligence.customer_analytics import CustomerAnalyzer
    from src.retail_intelligence.fashion_analyzer import FashionAnalyzer
    from src.retail_intelligence.festival_planner import FestivalPlanner
    from src.retail_intelligence.inventory_planner import InventoryPlanner
    from src.retail_intelligence.sales_analytics import SalesAnalyzer

    sales_analyzer = SalesAnalyzer(gemini_engine=ai_insights)
    inventory_planner = InventoryPlanner(gemini_engine=ai_insights)
    customer_analyzer = CustomerAnalyzer(gemini_engine=ai_insights)
    fashion_analyzer = FashionAnalyzer(gemini_engine=ai_insights)
    festival_planner = FestivalPlanner(gemini_engine=ai_insights)

    RETAIL_INTELLIGENCE_AVAILABLE = True
    print("✅ Retail Intelligence Modules loaded successfully")
except ImportError as e:
    RETAIL_INTELLIGENCE_AVAILABLE = False
    sales_analyzer = None
    inventory_planner = None
    customer_analyzer = None
    fashion_analyzer = None
    festival_planner = None
    print(f"⚠ Warning: Retail Intelligence modules not available: {e}")

# Initialize enhanced utilities
try:
    from src.utils.file_cross_referencer import FileCrossReferencer
    from src.utils.response_formatter import ResponseFormatter

    response_formatter = ResponseFormatter()
    file_cross_referencer = FileCrossReferencer()

    ENHANCED_UTILS_AVAILABLE = True
    print("✅ Enhanced utilities loaded successfully")
except ImportError as e:
    ENHANCED_UTILS_AVAILABLE = False
    response_formatter = None
    file_cross_referencer = None
    print(f"⚠ Warning: Enhanced utilities not available: {e}")

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

# Register AI Chat Blueprint (NEW - Path Configuration Feature)
try:
    from web.ai_chat_routes import ai_chat_bp

    app.register_blueprint(ai_chat_bp)
    print("✓ AI Chat routes registered at /ai-chat")
except Exception as e:
    print(f"⚠ AI Chat routes not available: {e}")

# Register Path Manager Blueprint (NEW - File Path Configuration)
try:
    from src.web.path_routes import path_bp

    app.register_blueprint(path_bp)
    print("✓ Path Manager routes registered at /api/paths")
except Exception as e:
    print(f"⚠ Path Manager routes not available: {e}")

# Register Email Authentication Blueprint (NEW - Email Signup/Login)
try:
    from src.auth.email_auth import email_auth_bp

    app.register_blueprint(email_auth_bp, url_prefix="/auth")
    print("✓ Email authentication routes registered at /auth")
except Exception as e:
    print(f"⚠ Email authentication routes not available: {e}")

# Register Admin Panel Blueprint (NEW - User Management & Access Control)
try:
    from src.admin import admin_bp, init_admin_db
    from src.admin.access_control import AccessControl, DataFilter

    # Initialize admin database tables
    init_admin_db()
    print("✓ Admin database initialized")

    # Register admin blueprint
    app.register_blueprint(admin_bp)
    print("✓ Admin Panel routes registered at /admin")

    # Create global instances for use in routes
    admin_access_control = AccessControl()
    admin_data_filter = DataFilter()

    ADMIN_PANEL_AVAILABLE = True
except Exception as e:
    ADMIN_PANEL_AVAILABLE = False
    admin_access_control = None
    admin_data_filter = None
    print(f"⚠ Admin Panel not available: {e}")

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

    # Redirect to email-based signup/login page
    return redirect("/auth/login")


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


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect("/")


# ==========================================
# PATH MANAGER HELPER FUNCTIONS
# ==========================================


def get_path_manager_context(query: str, limit: int = 5) -> Optional[str]:
    """
    Search configured paths for relevant files based on query.
    Returns formatted context string with file contents if found.
    """
    try:
        # Search for relevant files in configured paths
        results = path_manager.search_files(query, limit=limit)

        if not results:
            return None

        # Build context from found files
        context_parts = [
            f"\n📁 **Found {len(results)} relevant file(s) from configured paths:**\n"
        ]

        for i, file_info in enumerate(results, 1):
            file_path = file_info.get("path")
            file_name = file_info.get("name")
            source_path = file_info.get("source_path", "Unknown")

            try:
                # Read file content (limit to reasonable size)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(10000)  # Limit to 10KB

                context_parts.append(
                    f"\n**File {i}: {file_name}** (from {source_path})"
                )
                context_parts.append(
                    f"```\n{content[:5000]}\n```\n"
                )  # Limit to 5KB per file

            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                continue

        if len(context_parts) > 1:  # More than just the header
            return "\n".join(context_parts)

        return None

    except Exception as e:
        print(f"Error getting path manager context: {e}")
        return None


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
    file_context = data.get("file_context", [])  # Files uploaded from File Browser
    catalogue_context = data.get("catalogue_context")  # Data Catalogue Configuration

    if not prompt:
        return jsonify({"error": "Please provide a prompt."}), 400

    # Enhanced: Intelligent context gathering with priority
    enhanced_prompt = prompt
    context_info = []

    try:
        prompt_lower = prompt.lower().strip()

        # PRIORITY 0: Simple Greeting Detection - No Gemini call, instant response
        # Returns simple greeting without any analysis, file reading, or database queries
        SIMPLE_GREETINGS = [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "greetings",
            "namaste",
            "hola",
            "bonjour",
        ]

        if prompt_lower in SIMPLE_GREETINGS:
            print("🎯 Simple greeting detected - returning instant response")
            return jsonify({"response": "Hi! I am V-Mart Personal AI Agent"})

        # PRIORITY 1: Handle uploaded files from File Browser (highest priority for data analysis)
        if file_context and len(file_context) > 0:
            print(f"\n{'=' * 80}")
            print(
                f"📎 FILE CONTEXT DETECTED: {len(file_context)} file(s) uploaded from File Browser"
            )

            # Check if too many files - recommend batch processing
            if len(file_context) > 5:
                return jsonify(
                    {
                        "response": f"""⚠️ **Too Many Files for Single Analysis**

You've uploaded **{len(file_context)} files**, which may cause rate limit issues.

**Recommended approach:**
1. ✅ Analyze **3-5 files at a time** for best results
2. ✅ Start with the most important files first
3. ✅ Ask specific questions about each batch

**Why this helps:**
- Prevents API rate limit errors
- Faster responses
- More focused analysis

**Please upload fewer files (max 5) and try again.**"""
                    }
                )

            # Build comprehensive file analysis context
            files_summary = []
            full_file_content = []

            for idx, file_info in enumerate(file_context, 1):
                filename = file_info.get("filename", f"file_{idx}")
                file_type = file_info.get("type", "unknown")
                content = file_info.get("content", "")
                metadata = file_info.get("metadata", {})

                print(f"   File {idx}: {filename} ({file_type})")
                if metadata:
                    print(f"           Metadata: {metadata}")

                files_summary.append(f"- {filename} ({file_type})")

                # Add file content with clear markers - limit to 20KB per file to prevent rate limits
                content_preview = content[:20000]  # Reduced from 50000 to 20000
                truncated = len(content) > 20000

                full_file_content.append(f"""
{"=" * 80}
FILE {idx}: {filename}
TYPE: {file_type}
METADATA: {metadata}
SIZE: {len(content)} characters{" (showing first 20,000)" if truncated else ""}
{"=" * 80}
{content_preview}
{f"... [Content truncated - {len(content) - 20000} more characters. Ask specific questions about this file.]" if truncated else ""}
{"=" * 80}
""")

            # Create enhanced prompt for V-Mart retail analysis with multi-file correlation
            context_info.append(f"Analyzing {len(file_context)} uploaded file(s)")

            # Enhanced prompt with correlation instructions
            correlation_hint = ""
            if len(file_context) > 1:
                correlation_hint = f"""

**🔗 MULTI-FILE CORRELATION REQUIRED:**
You have {len(file_context)} files to analyze together. You MUST:
1. Find common fields/IDs across files (e.g., Store_ID, Product_ID, Item_Code, Region, Date)
2. Join/correlate data based on matching fields
3. Identify patterns that emerge from cross-file analysis
4. Highlight discrepancies or anomalies across files

Examples:
- If file1 has Store_ID and file2 has Store_ID → analyze by store
- If file1 has Product_Code and file2 has Item_ID → check if they match
- If both have dates → perform temporal correlation
"""

            enhanced_prompt = f"""**🚨 ABSOLUTE CRITICAL INSTRUCTION FOR AI 🚨**

You are analyzing ATTACHED/UPLOADED FILES ONLY. You MUST follow these rules WITHOUT EXCEPTION:

❌ DO NOT use any stored data or databases (except the files below)
❌ DO NOT use your training knowledge about V-Mart or retail
❌ DO NOT use general knowledge or assumptions
❌ DO NOT reference information not in the files below
❌ DO NOT use previous conversations or context
❌ DO NOT make inferences beyond the explicit data

✅ ONLY analyze the file content provided below
✅ ONLY cite data explicitly visible in these files
✅ ONLY quote exact values, names, IDs from the files
✅ If information is NOT in the files, respond: "This information is not available in the uploaded files"
{correlation_hint}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📎 UPLOADED FILES ({len(file_context)} file(s)):
{chr(10).join(files_summary)}

📊 FILE CONTENT (USE ONLY THIS DATA):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{"".join(full_file_content)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**User's Question:** {prompt}

**MANDATORY RESPONSE STRUCTURE:**

📊 **INSIGHTS** (What the data reveals):
[If numbers/metrics, present in clean tables]
[If text observations, write in proper paragraphs]

Format for tables (when presenting numerical data):
| Metric | Value | Analysis |
|--------|-------|----------|
| Sales  | $XXX  | Insight  |

Format for text paragraphs:
Write in complete sentences using only commas, periods and question marks when needed. No special characters like asterisks, hyphens or bullet points. Present insights as flowing paragraphs.

💡 **RECOMMENDATIONS** (What should be done):
[If multiple recommendations with priorities, use tables]
[If narrative recommendations, use paragraphs]

Format for recommendations table:
| Priority | Recommendation | Expected Impact |
|----------|----------------|-----------------|
| High     | Action item    | Impact desc     |

✅ **ACTIONABLES** (Precise steps with timelines):
Always present as a table:

| Step | Action | Timeline | Owner |
|------|--------|----------|-------|
| 1    | Do X   | 2 weeks  | Team  |
| 2    | Do Y   | 1 month  | Dept  |

🎯 **STRATEGY** (Long-term approach):
Write as proper paragraphs without special characters. Use only commas, periods and question marks. Present strategic direction in flowing narrative form.

**CITATION REQUIREMENTS:**
1. Source every fact with the file name it came from
2. Use exact values as they appear in the files (no rounding or estimates)
3. If a store/product/metric isn't in the files, it doesn't exist for this analysis
4. State "Based on the uploaded file [filename]..." in your response
5. Do NOT add information from your general knowledge

**Forbidden Actions:**
- Referencing stores not listed in the files above
- Using revenue/sales figures not in the files above
- Making assumptions about data not explicitly stated
- Using "typical" or "usually" or "generally" statements
- Citing V-Mart information from your training data

BEGIN DEEP ANALYSIS WITH INSIGHTS, RECOMMENDATIONS, ACTIONABLES & STRATEGY:"""

            print(f"{'=' * 80}\n")

            # Send to Gemini for FILE-ONLY analysis
            response = gemini_agent.get_response(enhanced_prompt, use_context=False)
            formatted_response = format_ai_response(response)

            # Add file browser indicator
            formatted_response = f"""<div class="file-browser-response">
    <p><strong>📎 File Browser Analysis ({len(file_context)} file(s))</strong></p>
    {formatted_response}
</div>"""

            return jsonify({"response": formatted_response})

        # PRIORITY 2: Handle Data Catalogue Configuration context
        # Enhanced to also use File Browser uploaded files for correlation
        if catalogue_context and catalogue_context.get("has_data"):
            print(f"\n{'=' * 80}")
            print("📚 DATA CATALOGUE CONTEXT DETECTED")

            catalogue_data = catalogue_context.get("data", {})
            catalogue_metadata = catalogue_context.get("metadata", {})
            catalogue_summary = catalogue_context.get("summary", "")

            # Check if File Browser files are also available for correlation
            has_file_browser_data = file_context and len(file_context) > 0
            if has_file_browser_data:
                print(
                    f"   + File Browser data available for correlation: {len(file_context)} file(s)"
                )

            # Build catalogue context sections
            catalogue_sections = []

            if catalogue_data.get("itemMaster"):
                items = catalogue_data["itemMaster"]
                meta = catalogue_metadata.get("itemMaster", {})
                catalogue_sections.append(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 ITEM MASTER DATA
File: {meta.get("originalFilename", "N/A")}
Records: {meta.get("recordCount", 0)}
Uploaded: {meta.get("uploadTimestamp", "N/A")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{items[:30000]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

            if catalogue_data.get("storeMaster"):
                stores = catalogue_data["storeMaster"]
                meta = catalogue_metadata.get("storeMaster", {})
                catalogue_sections.append(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏪 STORE MASTER DATA
File: {meta.get("originalFilename", "N/A")}
Records: {meta.get("recordCount", 0)}
Uploaded: {meta.get("uploadTimestamp", "N/A")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{stores[:30000]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

            if catalogue_data.get("competitionMaster"):
                competition = catalogue_data["competitionMaster"]
                meta = catalogue_metadata.get("competitionMaster", {})
                catalogue_sections.append(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 COMPETITION MASTER DATA
File: {meta.get("originalFilename", "N/A")}
Records: {meta.get("recordCount", 0)}
Uploaded: {meta.get("uploadTimestamp", "N/A")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{competition[:30000]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

            if catalogue_data.get("marketingPlan"):
                marketing = catalogue_data["marketingPlan"]
                meta = catalogue_metadata.get("marketingPlan", {})
                catalogue_sections.append(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📢 MARKETING PLAN DATA
File: {meta.get("originalFilename", "N/A")}
Records: {meta.get("recordCount", 0)}
Uploaded: {meta.get("uploadTimestamp", "N/A")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{marketing[:30000]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

            # Create enhanced prompt with catalogue correlation and master data joins
            context_info.append(f"Data Catalogue: {catalogue_summary}")

            # Identify available masters for correlation guidance
            available_masters = []
            if catalogue_data.get("itemMaster"):
                available_masters.append("Item Master")
            if catalogue_data.get("storeMaster"):
                available_masters.append("Store Master")
            if catalogue_data.get("competitionMaster"):
                available_masters.append("Competition Master")
            if catalogue_data.get("marketingPlan"):
                available_masters.append("Marketing Plan")

            # Build master join instructions based on available data
            join_instructions = ""
            if len(available_masters) > 1:
                join_instructions = f"""

**🔗 MASTER DATA JOIN INSTRUCTIONS:**

You have {len(available_masters)} master datasets. Perform intelligent joins:

1. **Store Master ↔ Competition Master:**
   - Join on: Store_ID, Region, City, or Geographic proximity
   - Analysis: Competitive landscape impact on store performance
   - Look for: Stores with high competition vs revenue patterns

2. **Item Master ↔ Marketing Plan:**
   - Join on: Item_ID, Product_Code, Category
   - Analysis: Marketing campaign effectiveness by product
   - Look for: ROI of campaigns on specific items/categories

3. **Store Master ↔ Marketing Plan:**
   - Join on: Store_ID, Region, City
   - Analysis: Regional marketing effectiveness
   - Look for: Campaign impact by store location/region

4. **Item Master ↔ Store Master:**
   - Join on: Store_ID with Item performance data
   - Analysis: Product performance by store location
   - Look for: Best-selling items by geography

**JOIN KEY EXAMPLES:**
- Store_ID (primary key for store-related joins)
- Item_ID / Product_ID / SKU (for item-related joins)
- Region / City / State (geographical joins)
- Date / Month / Quarter (temporal joins)
- Category / Department (categorical joins)

**CRITICAL:** Always cite which masters you're joining and on which keys!
"""

            # Add File Browser files to correlation if available
            file_browser_section = ""
            if has_file_browser_data:
                files_list = []
                file_contents = []

                for idx, file_info in enumerate(file_context, 1):
                    filename = file_info.get("filename", f"file_{idx}")
                    file_type = file_info.get("type", "unknown")
                    content = file_info.get("content", "")

                    files_list.append(f"- {filename} ({file_type})")

                    # Add file content (limited to 15KB to leave room for masters)
                    content_preview = content[:15000]
                    truncated = len(content) > 15000

                    file_contents.append(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📎 FILE BROWSER FILE {idx}: {filename}
Type: {file_type}
Size: {len(content)} characters{" (showing first 15,000)" if truncated else ""}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{content_preview}
{f"... [Truncated - {len(content) - 15000} more characters]" if truncated else ""}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

                file_browser_section = f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📎 FILE BROWSER UPLOADED FILES ({len(file_context)} file(s))
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**ADDITIONAL CORRELATION REQUIRED:**
You also have {len(file_context)} file(s) uploaded via File Browser.
You MUST correlate these files with the master data above!

**Files Available:**
{chr(10).join(files_list)}

**FILE CONTENT FOR CORRELATION:**
{"".join(file_contents)}

**CORRELATION INSTRUCTIONS:**
1. Find common fields between uploaded files and masters
2. Join File Browser data with relevant masters
3. Examples:
   - If uploaded file has Store_ID → Join with Store Master
   - If uploaded file has Product_ID → Join with Item Master
   - If uploaded file has sales data → Correlate with Marketing Plan
   - If uploaded file has competitor data → Join with Competition Master
4. Provide insights from both master data AND uploaded files together

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

            enhanced_prompt = f"""**🚨 V-MART DATA CATALOGUE CORRELATION ANALYSIS 🚨**

You are analyzing V-Mart's operational data from the Data Catalogue Configuration system{" AND File Browser uploaded files" if has_file_browser_data else ""}.
Your task is to perform DEEP CORRELATION ANALYSIS with MASTER DATA JOINS across multiple sources.

**CRITICAL INSTRUCTIONS:**
✅ Perform intelligent joins across master datasets (use join keys: Store_ID, Item_ID, Region, Date, etc.)
{f"✅ ALSO join File Browser uploaded files with master data" if has_file_browser_data else ""}
✅ Analyze ALL available master data sources together{" with uploaded files" if has_file_browser_data else ""}
✅ Find correlations, patterns, and relationships across joined datasets
✅ Provide actionable insights based on cross-referenced data
✅ Consider temporal, geographical, and categorical relationships
✅ ONLY use the exact data provided below - no assumptions

❌ DO NOT use external knowledge or assumptions beyond the masters{" and uploaded files" if has_file_browser_data else ""}
❌ DO NOT reference data not in the catalogue{" or uploaded files" if has_file_browser_data else ""}
❌ DO NOT make estimates - use exact values only from masters{" and files" if has_file_browser_data else ""}
❌ DO NOT ignore relationships between masters{" and uploaded files" if has_file_browser_data else ""}
{join_instructions}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 DATA CATALOGUE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{catalogue_summary}

📊 AVAILABLE MASTERS: {", ".join(available_masters)}
{f"📎 ADDITIONAL FILES: {len(file_context)} uploaded file(s) from File Browser" if has_file_browser_data else ""}

📊 MASTER DATA SOURCES (WITH JOIN KEYS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{"".join(catalogue_sections)}
{file_browser_section}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**User's Question:** {prompt}

**MANDATORY RESPONSE STRUCTURE:**

📊 **MASTER DATA JOINS PERFORMED:**
Present as a simple table:

| Join | Masters Connected | Join Key | Purpose |
|------|-------------------|----------|---------|
| 1    | Store ↔ Competition | Store_ID | Analyze competitive impact |
| 2    | Item ↔ Marketing | Product_ID | Campaign effectiveness |

📈 **INSIGHTS** (What correlated data reveals):
[If numerical metrics, use tables]
[If observations, use proper paragraphs]

For tables with numbers:
| Store ID | Revenue | Competition Count | Impact Analysis |
|----------|---------|-------------------|-----------------|
| S001     | $XXX    | 3                 | Insight         |

For text insights:
Write in flowing paragraphs using only commas, periods and question marks. No special characters or bullet points. Present findings as complete sentences in narrative form.

💡 **RECOMMENDATIONS** (Based on master correlations):
Present as clean table:

| Priority | Recommendation | Data Source | Expected Impact |
|----------|----------------|-------------|-----------------|
| High     | Action         | Master(s)   | Impact          |
| Medium   | Action         | Master(s)   | Impact          |

✅ **ACTIONABLES** (Precise steps with timelines):
Always present as structured table:

| Step | Action | Timeline | Owner | Master Data Used |
|------|--------|----------|-------|------------------|
| 1    | Do X   | 2 weeks  | Team  | Store Master     |
| 2    | Do Y   | 1 month  | Dept  | Item Master      |

🎯 **STRATEGY** (Long-term approach based on masters):
Write as proper paragraphs without special characters. Use only commas, periods and question marks when needed. Present strategic direction as flowing narrative based on master data relationships.

**CITATION REQUIREMENTS:**
1. Always state which master file(s) you're using
2. Specify join keys used for correlation
3. Use exact values from masters (no rounding)
4. Reference record IDs when possible
5. Cite temporal context (dates from data)

**CORRELATION EXAMPLES TO ANALYZE:**
- Store revenue (Store Master) vs competition intensity (Competition Master)
- Item sales patterns (Item Master) vs marketing campaigns (Marketing Plan)
- Store performance by region (Store Master) vs regional marketing spend (Marketing Plan)
- Product pricing (Item Master) vs competitor pricing (Competition Master)
- Marketing ROI by store location (Store Master + Marketing Plan)

BEGIN MASTER DATA CORRELATION ANALYSIS WITH JOINS:"""

            print(f"{'=' * 80}\n")

            # Send to Gemini for correlation analysis
            response = gemini_agent.get_response(enhanced_prompt, use_context=False)
            formatted_response = format_ai_response(response)

            # Add catalogue indicator with File Browser info if applicable
            if has_file_browser_data:
                formatted_response = f"""<div class="catalogue-response">
    <p><strong>📚 Data Catalogue + File Browser Correlation Analysis</strong></p>
    <p><em>{catalogue_summary} + {len(file_context)} uploaded file(s)</em></p>
    {formatted_response}
</div>"""
            else:
                formatted_response = f"""<div class="catalogue-response">
    <p><strong>📚 Data Catalogue Correlation Analysis</strong></p>
    <p><em>{catalogue_summary}</em></p>
    {formatted_response}
</div>"""

            return jsonify({"response": formatted_response})

        # PRIORITY 2: If user has browsed a file AND asking about it, use it directly
        elif browsed_file and browsed_file.get("content"):
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
            # FIRST: Try to get context from configured paths (Path Manager)
            path_context = get_path_manager_context(prompt, limit=3)

            if path_context:
                # Found relevant files in configured paths
                context_info.append("Using files from configured paths")
                enhanced_prompt = f"""{path_context}

**USER'S QUESTION:** {prompt}

Please answer the question using the files provided above from the configured paths. If the files don't contain relevant information, let the user know."""

            # FALLBACK: Only search other files/sources if no path manager files found
            elif not path_context:
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
    # STRICT RESTRICTION: For general queries (no files/catalogue), ONLY use live weather data
    # NO stored database data except weather API
    analytics_context_text = None
    try:
        from analytics.context_provider import AnalyticsContextProvider

        # Check if this is a weather-related query
        weather_keywords = [
            "weather",
            "temperature",
            "climate",
            "rain",
            "sunny",
            "forecast",
            "humidity",
            "wind",
            "storm",
            "hot",
            "cold",
        ]

        is_weather_query = any(keyword in prompt_lower for keyword in weather_keywords)

        # CRITICAL: Only allow weather data for general queries
        if is_weather_query:
            # Get ONLY weather context (live API data)
            context_provider = AnalyticsContextProvider()
            analytics_context = context_provider.get_context_for_prompt(
                prompt, days=0
            )  # days=0 for live data only

            if analytics_context.get("has_data"):
                # Format context for AI - weather only
                analytics_context_text = context_provider.format_context_for_ai(
                    analytics_context
                )
                context_info.append("Live Weather Data")
        else:
            # NOT a weather query and no files uploaded
            # Block access to stored database/analytics data
            print(
                "🚫 General query without files/catalogue - database access restricted to weather only"
            )
            # No analytics context for non-weather general queries

    except Exception as e:
        print(f"⚠ Analytics context not available: {e}")

    # ========== ENHANCED AI INTEGRATION WITH CURATED RESPONSES ==========
    # Gather all data sources for curated response formatting
    data_sources = []
    file_references = []
    analytics_data_dict = None

    # Track store/weather/competition data if available
    try:
        # Check if store context was requested
        store_id_param = data.get("store_id")
        city_param = data.get("city")

        if store_id_param or city_param:
            data_sources.append(
                {
                    "type": "store" if store_id_param else "city",
                    "store_id": store_id_param,
                    "location": city_param or "N/A",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Add weather data source if detected in prompt
        if any(
            word in prompt_lower
            for word in ["weather", "temperature", "climate", "rain", "sunny"]
        ):
            data_sources.append(
                {
                    "type": "weather",
                    "location": city_param or "N/A",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Add competition data if detected
        if any(
            word in prompt_lower
            for word in ["competition", "competitor", "rival", "market"]
        ):
            data_sources.append(
                {
                    "type": "competition",
                    "count": "variable",
                    "timestamp": datetime.now().isoformat(),
                }
            )
    except Exception as e:
        print(f"Error tracking data sources: {e}")

    # Track file references
    if browsed_file and browsed_file.get("content"):
        file_references.append(
            {
                "name": browsed_file.get("name", "Unknown"),
                "format": browsed_file.get("format", "text"),
                "size": len(browsed_file.get("content", "")),
                "source": browsed_file.get("source", "browser"),
            }
        )

    # Convert analytics context to dict if available
    if analytics_context_text:
        analytics_data_dict = {
            "source": "V-Mart Analytics Engine",
            "period": "last 30 days",
            "has_data": True,
        }

    # Get AI response with analytics context
    response = gemini_agent.get_response(
        enhanced_prompt,
        use_context=use_context,
        analytics_context=analytics_context_text,
    )

    # ========== APPLY CURATED RESPONSE FORMATTING ==========
    try:
        from src.utils.response_formatter import ResponseFormatter

        formatter = ResponseFormatter()
        curated = formatter.format_curated_response(
            ai_response=response,
            data_sources=data_sources if data_sources else None,
            analytics_data=analytics_data_dict,
            file_references=file_references if file_references else None,
            include_citations=True,
        )

        # Use the curated response with enhanced formatting
        response = curated["response"]

        # Add insights section if available
        if curated.get("insights"):
            insights_html = "<div class='ai-insights'><h4>🔍 Key Insights:</h4><ul>"
            for insight in curated["insights"][:3]:  # Top 3
                insights_html += f"<li>{insight}</li>"
            insights_html += "</ul></div>"
            response = insights_html + "\n\n" + response

        # Add recommendations section if available
        if curated.get("recommendations"):
            rec_html = (
                "<div class='ai-recommendations'><h4>💡 Recommendations:</h4><ul>"
            )
            for rec in curated["recommendations"][:3]:  # Top 3
                rec_html += f"<li>{rec}</li>"
            rec_html += "</ul></div>"
            response = response + "\n\n" + rec_html

        # Add citations if available
        if curated.get("citations"):
            citations_html = "<div class='ai-citations'><h4>📚 Data Sources:</h4><ul>"
            for cite in curated["citations"]:
                citations_html += (
                    f"<li><strong>{cite.get('type')}</strong>: {cite.get('source')} "
                )
                if cite.get("location"):
                    citations_html += f"({cite.get('location')})"
                citations_html += "</li>"
            citations_html += "</ul></div>"
            response = response + "\n\n" + citations_html

    except Exception as e:
        print(f"⚠ Response formatting enhancement skipped: {e}")
        # Fall back to original response if formatting fails

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
    # Disable debug mode for background processes to avoid terminal I/O errors
    # Set FLASK_DEBUG=1 environment variable to enable debug mode
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=8000, debug=debug_mode, use_reloader=False)
