"""
V-Mart Personal AI Agent - Main Flask Application
Enhanced with multi-connector support and advanced features

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
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
    """
    Enhanced ask function that searches local files for context
    """
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    prompt = data.get("prompt")
    use_context = data.get("use_context", True)

    if not prompt:
        return jsonify({"error": "Please provide a prompt."}), 400

    # Enhanced: Search for relevant context from various sources
    enhanced_prompt = prompt
    context_info = []

    try:
        # Keywords to detect what user is asking about
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
            "local",
            "computer",
            "system",
            "folder",
            "desktop",
            "documents",
            "downloads",
        ]
        keywords_progress = [
            "progress",
            "report",
            "status",
            "result",
            "metric",
            "data",
            "analysis",
        ]

        prompt_lower = prompt.lower()

        # Search local files if relevant keywords detected
        should_search_local = any(
            keyword in prompt_lower
            for keyword in keywords_local + keywords_doc + keywords_progress
        )

        if should_search_local:
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
                                    filename.lower().endswith(ext)
                                    for ext in doc_extensions
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

                    file_context = "\n\n📁 AVAILABLE DOCUMENTS:\n"
                    file_context += "=" * 60 + "\n"

                    for idx, file_info in enumerate(all_files_found[:8], 1):
                        file_size_kb = file_info["size"] / 1024
                        file_context += f"\n{idx}. {file_info['name']}\n"
                        file_context += f"   Location: {file_info['location']}\n"
                        file_context += f"   Size: {file_size_kb:.1f} KB\n"
                        file_context += (
                            f"   Path: {os.path.dirname(file_info['path'])}\n"
                        )

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
                    enhanced_prompt += (
                        "   - ~/Documents\n   - ~/Desktop\n   - ~/Downloads\n"
                    )
                    enhanced_prompt += "\nPlease specify exact file names or check these locations for your documents.\n"

            except Exception as e:
                print(f"Error searching local files: {e}")
                enhanced_prompt += (
                    f"\n\n(Note: Error accessing local files: {str(e)})\n"
                )

        # Add helpful context about Gmail/Drive
        if any(word in prompt_lower for word in ["email", "gmail", "mail", "inbox"]):
            enhanced_prompt += "\n\n📧 Note: Gmail search requires Google OAuth authentication (currently in demo mode).\n"

        if any(word in prompt_lower for word in ["google drive", "drive", "cloud"]):
            enhanced_prompt += "\n\n☁️ Note: Google Drive search requires OAuth authentication (currently in demo mode).\n"

    except Exception as e:
        print(f"Error in context gathering: {e}")

    # Prepare the final prompt with instructions
    if context_info:
        instruction = f"\n\nYou are analyzing documents and data. Context: {', '.join(context_info)}.\n"
        instruction += "Based on the documents listed above, provide a detailed answer to the user's question.\n"
        instruction += "Reference specific documents by name when relevant.\n\n"
        enhanced_prompt = instruction + enhanced_prompt

    # Get AI response
    response = gemini_agent.get_response(enhanced_prompt, use_context=use_context)

    # Add source attribution
    if context_info:
        response = f"📚 **Sources**: {', '.join(context_info)}\n\n{response}"

    return jsonify({"response": response})


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
