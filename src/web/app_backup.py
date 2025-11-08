"""
Main Flask Application for V-Mart Personal AI Agent
Enhanced with multi-connector support and advanced features
"""

import json
import os

from agent.gemini_agent import GeminiAgent
from auth import google_auth
from connectors.local_files import LocalFilesConnector
from flask import Flask, jsonify, redirect, render_template, request, session
from scheduler.task_scheduler import TaskScheduler

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# Configure Google OAuth
app.config["GOOGLE_CLIENT_ID"] = os.environ.get("GOOGLE_CLIENT_ID")
app.config["GOOGLE_CLIENT_SECRET"] = os.environ.get("GOOGLE_CLIENT_SECRET")
google_auth.init_app(app)

# Initialize Gemini Agent
gemini_agent = GeminiAgent(api_key=os.environ.get("GEMINI_API_KEY"))

# Initialize Local Files Connector
local_connector = LocalFilesConnector(base_path=os.path.expanduser("~"))

# Initialize Task Scheduler
scheduler = TaskScheduler()
scheduler.start()


@app.route("/")
def index():
    if "user" in session:
        return render_template("index.html", user=session["user"])

    # Check if we're in demo mode (no OAuth configured)
    if (
        not app.config.get("GOOGLE_CLIENT_ID")
        or app.config["GOOGLE_CLIENT_ID"] == "your_google_client_id_here"
    ):
        return """
        <html>
        <head><title>V-Mart AI Agent - Demo Mode</title></head>
        <body style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px;">
            <h1>🤖 V-Mart Personal AI Agent</h1>
            <p>Google OAuth is not configured yet.</p>
            <h3>To enable full functionality:</h3>
            <ol>
                <li>Get Google OAuth credentials from <a href="https://console.cloud.google.com">Google Cloud Console</a></li>
                <li>Get Gemini API key from <a href="https://makersuite.google.com/app/apikey">Google AI Studio</a></li>
                <li>Update the <code>.env</code> file with your credentials</li>
                <li>Restart the server</li>
            </ol>
            <p><strong>For testing without OAuth:</strong></p>
            <form action="/demo-login" method="post" style="margin-top: 20px;">
                <button type="submit" style="padding: 10px 20px; background: #4285f4; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">
                    Enter Demo Mode
                </button>
            </form>
            <p style="color: #666; margin-top: 20px;"><small>Demo mode allows you to test the interface without Google authentication.</small></p>
        </body>
        </html>
        """

    return 'Welcome! Please <a href="/auth/login">login with Google</a>.'


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
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    prompt = data.get("prompt")
    use_context = data.get("use_context", True)

    if not prompt:
        return jsonify({"error": "Please provide a prompt."}), 400

    # Enhanced: Search for relevant context from various sources
    enhanced_prompt = prompt
    context_sources = []

    try:
        # Check if user is asking about documents, emails, files, etc.
        keywords_email = ["email", "mail", "inbox", "message", "sent"]
        keywords_drive = [
            "drive",
            "document",
            "doc",
            "sheet",
            "slide",
            "presentation",
            "file",
        ]
        keywords_local = ["local", "computer", "system", "folder", "directory"]

        prompt_lower = prompt.lower()

        # Search Gmail for relevant emails
        if any(keyword in prompt_lower for keyword in keywords_email):
            try:
                from auth.google_auth import get_credentials
                from connectors.gmail_connector import GmailConnector

                credentials = get_credentials()
                if credentials:
                    gmail = GmailConnector(credentials)
                    messages = gmail.list_messages(query="", max_results=5)
                    if messages:
                        context_sources.append("📧 Found recent emails in Gmail")
                        email_context = "\n\nRecent Gmail context:\n"
                        for msg in messages[:3]:
                            msg_data = gmail.read_message(msg.get("id", ""))
                            if msg_data:
                                email_context += (
                                    f"- {msg_data.get('subject', 'No subject')}\n"
                                )
                        enhanced_prompt += email_context
            except Exception as e:
                print(f"Gmail search error: {e}")

        # Search Google Drive for documents
        if any(keyword in prompt_lower for keyword in keywords_drive):
            try:
                from auth.google_auth import get_credentials
                from connectors.google_docs_connector import GoogleDocsConnector
                from connectors.google_drive import GoogleDriveConnector
                from connectors.google_sheets_connector import GoogleSheetsConnector

                credentials = get_credentials()
                if credentials:
                    drive = GoogleDriveConnector(credentials)

                    # Search for relevant files
                    search_terms = [
                        word for word in prompt_lower.split() if len(word) > 3
                    ]
                    if search_terms:
                        query = f"name contains '{search_terms[0]}'"
                        files = drive.search_file(query, page_size=5)

                        if files:
                            context_sources.append(
                                f"📁 Found {len(files)} files in Google Drive"
                            )
                            drive_context = "\n\nGoogle Drive files found:\n"

                            for file in files[:3]:
                                file_name = file.get("name", "")
                                file_id = file.get("id", "")
                                drive_context += f"- {file_name}\n"

                                # Try to read content based on file type
                                if "sheet" in file_name.lower():
                                    try:
                                        sheets = GoogleSheetsConnector(credentials)
                                        data = sheets.read_range(
                                            file_id, "Sheet1!A1:Z100"
                                        )
                                        if data:
                                            drive_context += f"  (Contains {len(data)} rows of data)\n"
                                    except:
                                        pass
                                elif "doc" in file_name.lower():
                                    try:
                                        docs = GoogleDocsConnector(credentials)
                                        content = docs.read_document(file_id)
                                        if content:
                                            preview = (
                                                content[:200]
                                                if len(content) > 200
                                                else content
                                            )
                                            drive_context += (
                                                f"  Preview: {preview}...\n"
                                            )
                                    except:
                                        pass

                            enhanced_prompt += drive_context
            except Exception as e:
                print(f"Google Drive search error: {e}")

        # Search local files
        if any(keyword in prompt_lower for keyword in keywords_local):
            try:
                # Search common document locations
                search_paths = [
                    os.path.expanduser("~/Documents"),
                    os.path.expanduser("~/Desktop"),
                    os.path.expanduser("~/Downloads"),
                ]

                local_files = []
                search_terms = [word for word in prompt_lower.split() if len(word) > 3]

                for base_path in search_paths:
                    if os.path.exists(base_path):
                        results = local_connector.search_files(
                            base_path,
                            pattern=f"*{search_terms[0]}*" if search_terms else "*",
                        )
                        local_files.extend(results[:5])

                if local_files:
                    context_sources.append(f"💻 Found {len(local_files)} local files")
                    local_context = "\n\nLocal files found:\n"
                    for file_path in local_files[:3]:
                        local_context += f"- {os.path.basename(file_path)}\n"

                        # Try to read text files
                        if file_path.endswith((".txt", ".md", ".csv")):
                            try:
                                content = local_connector.read_file(file_path)
                                if content:
                                    preview = (
                                        content[:200] if len(content) > 200 else content
                                    )
                                    local_context += f"  Preview: {preview}...\n"
                            except:
                                pass

                    enhanced_prompt += local_context
            except Exception as e:
                print(f"Local file search error: {e}")

        # Add context sources info to response
        if context_sources:
            enhanced_prompt = f"Context gathered from: {', '.join(context_sources)}\n\n{enhanced_prompt}"

    except Exception as e:
        print(f"Error gathering context: {e}")

    # Get AI response with enhanced context
    response = gemini_agent.get_response(enhanced_prompt, use_context=use_context)

    # Add metadata about sources
    result = {"response": response}
    if context_sources:
        result["sources"] = context_sources

    return jsonify(result)


@app.route("/analyze", methods=["POST"])
def analyze():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    data_to_analyze = data.get("data")
    analysis_type = data.get("type", "general")

    if not data_to_analyze:
        return jsonify({"error": "Please provide data to analyze."}), 400

    analysis = gemini_agent.analyze_data(data_to_analyze, analysis_type=analysis_type)
    return jsonify({"analysis": analysis})


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

    result = gemini_agent.decision_support(decision, context, options)
    return jsonify(result)


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


@app.route("/clear-history", methods=["POST"])
def clear_history():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    gemini_agent.clear_history()
    return jsonify({"status": "success"})


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
