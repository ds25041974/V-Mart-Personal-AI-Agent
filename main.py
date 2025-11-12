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

# Initialize Store Management System
try:
    from stores.update_scheduler import start_store_scheduler

    store_scheduler = start_store_scheduler()
    print("✓ Store Update Scheduler initialized")
except Exception as e:
    print(f"⚠ Store Update Scheduler not available: {e}")
    store_scheduler = None

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    print(f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║           V-Mart Personal AI Agent Starting                     ║
    ║        Context-Aware Intelligence with Live Weather             ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    🚀 Server running on http://{host}:{port}
    🔐 Authentication: Google OAuth
    🤖 AI Model: Gemini 2.0 Flash
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ✨ NEW: AI CHAT WITH CONTEXT AWARENESS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    🧠 AI Chat: http://{host}:{port}/ai-chat/
       • Live weather for all stores (updated every 3 hours)
       • Geo-mapped store locations with coordinates
       • Competitor analysis within 5km radius
       • Real-time AI reasoning progress
       • Date-wise weather forecasts
       • Context-aware recommendations
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    👑 ADMIN PANEL - USER MANAGEMENT
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    🔐 Admin Dashboard: http://{host}:{port}/admin/dashboard
       • Email verification & whitelist management
       • User approval workflow
       • 10-level data access control (HO → Warehouse → Zone → Store → etc.)
       • Force-stop capability for suspended users
       • Super Admins (Protected):
         - dinesh.srivastava@vmart.co.in
         - ds.250474@gmail.com
         - dineshsrivastava07@gmail.com
       • Activity logging & audit trail
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📊 STORE & ANALYTICS FEATURES
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    🗺️  Store Locator Map: http://{host}:{port}/stores/map
    📊 Analytics Dashboard: http://{host}:{port}/analytics/dashboard-ui/VM_DL_001
    📈 Store Details: http://{host}:{port}/stores/vmart
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📚 DOCUMENTATION
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    • AI Chat Guide: docs/AI_CHAT_GUIDE.md
    • Admin Panel: docs/ADMIN_PANEL_GUIDE.md
    • Store Locator: docs/STORE_LOCATOR_GUIDE.md
    • Analytics: docs/ANALYTICS_GUIDE.md
    • Quick Start: AI_CHAT_README.md
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    💡 Developed by: DSR
    ✨ Inspired by: LA
    🤖 Powered by: Gemini AI + OpenWeatherMap
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    💬 Try asking: "How will today's weather affect sales at Delhi store?"
    
    Press CTRL+C to stop the server
    """)

    app.run(host=host, port=port, debug=debug)
