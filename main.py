"""
V-Mart Personal AI Agent - Main Entry Point

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from web.app import app

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    print(f"""
    ╔══════════════════════════════════════════╗
    ║   V-Mart Personal AI Agent Starting     ║
    ╚══════════════════════════════════════════╝
    
    🚀 Server running on http://{host}:{port}
    🔐 Authentication: Google OAuth
    🤖 AI Model: Gemini Pro
    📊 Features: Chat, Analysis, Files, Decision Support
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    💡 Developed by: DSR
    ✨ Inspired by: LA
    🤖 Powered by: Gemini AI
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Press CTRL+C to stop the server
    """)

    app.run(host=host, port=port, debug=debug)
