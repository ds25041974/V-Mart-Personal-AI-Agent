# 🤖 V-Mart Personal AI Agent

[![Python Application CI](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/actions/workflows/python-app.yml/badge.svg)](https://github.com/ds25041974/V-Mart-Personal-AI-Agent/actions/workflows/python-app.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/ds25041974/V-Mart-Personal-AI-Agent)

**Developed by: DSR | Inspired by: LA | Powered by: Gemini AI**

---

A comprehensive personal AI agent powered by Google's Gemini AI, featuring document search, Gmail/Drive integration, and multi-platform support.

## 📚 Documentation

**🔴 HIGH PRIORITY - START HERE:**
- ⭐ [**ARCHITECTURE.md**](docs/ARCHITECTURE.md) - Complete system architecture with flowcharts and objectives
- ⭐ [**CHATBOT_INTERFACE_GUIDE.md**](docs/CHATBOT_INTERFACE_GUIDE.md) - Detailed guide to all tabs and features
- ⭐ [**SERVICE_24x7_SETUP.md**](docs/SERVICE_24x7_SETUP.md) - 24x7 auto-start service configuration
- [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) - Complete setup instructions for Windows, macOS, and Linux
- [USER_GUIDE.md](docs/USER_GUIDE.md) - Comprehensive usage guide

**Additional Resources:**
- [GOOGLE_OAUTH_SETUP.md](docs/GOOGLE_OAUTH_SETUP.md) - Google OAuth configuration
- [API_REFERENCE.md](docs/API_REFERENCE.md) - API documentation for developers
- [QUICK_SETUP.md](QUICK_SETUP.md) - Quick start guide

## 🌟 Features

### Core Capabilities
- **💬 Intelligent Chat**: Context-aware conversations with Gemini 2.0 Flash
- **📁 Document Search**: Scan and search local files (PDF, Word, Excel, PowerPoint, text files)
- **📊 Data Analysis**: Advanced analysis for financial, sales, and inventory data
- **🎯 Decision Support**: AI-powered recommendations with pros/cons analysis
- **📧 Email Integration**: Read emails, send automated messages, and schedule bulk emails
- **📈 Google Workspace Integration**: Access Google Drive, Sheets, Docs, and Slides
- **🔄 GitHub Integration**: Manage repositories, read files, and create issues
- **⏰ Task Scheduler**: Automate recurring tasks and emails
- **🧠 Reasoning Engine**: Step-by-step analysis for complex problems

### Security & Authentication
- **🔐 Google OAuth**: Secure authentication
- **� Demo Mode**: Quick access without OAuth setup
- **🔒 Session Management**: Secure user sessions
- **🛡️ Push Protection**: GitHub secret scanning enabled

### Multi-Platform Support
- ✅ Windows 10+
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu/Debian/Fedora/Arch)

## 📋 Prerequisites

- Python 3.8 or higher
- Google Cloud account (optional, for OAuth)
- Gemini API key (free tier available)
- Gemini API key
- GitHub personal access token (optional, for GitHub features)

## 🚀 Quick Start

### Option 1: Run as 24x7 Service (Recommended for macOS)

**Auto-start on boot, restart on crash, always available:**

```bash
# Navigate to project directory
cd "/Users/dineshsrivastava/Ai Chatbot for Gemini LLM/V-Mart Personal AI Agent"

# Install and start the service
./install_service.sh

# Check service status
./check_service.sh

# Access the application
open http://localhost:5000
```

**Benefits:**
- ✅ Starts automatically on system boot
- ✅ Restarts automatically if it crashes
- ✅ Waits for network before starting
- ✅ Runs 24x7 without manual intervention
- ✅ Complete logging and monitoring

📖 **Full Documentation**: [SERVICE_24x7_SETUP.md](docs/SERVICE_24x7_SETUP.md)

---

### Option 2: Manual Start

### 1. Clone the Repository

```bash
git clone https://github.com/ds25041974/dinesh-assistant-deployment.git
cd "V-Mart Personal AI Agent"
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GEMINI_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_token
SECRET_KEY=your_random_secret_key
```

### 4. Set Up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Google Drive API
   - Gmail API
   - Google Sheets API
   - Google Docs API
   - Google Slides API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:5000/authorize`
   - `http://127.0.0.1:5000/authorize`
6. Copy the Client ID and Client Secret to your `.env` file

### 5. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Copy it to your `.env` file

### 6. Run the Application

```bash
python main.py
```

Visit `http://localhost:5000` in your browser.

## 📚 Project Structure

```
V-Mart Personal AI Agent/
├── src/
│   ├── agent/              # Core AI agent logic
│   │   └── gemini_agent.py # Gemini LLM integration
│   ├── auth/               # Authentication handling
│   │   └── google_auth.py  # Google OAuth
│   ├── connectors/         # External service connectors
│   │   ├── google_drive.py
│   │   ├── gmail_connector.py
│   │   ├── google_sheets_connector.py
│   │   ├── google_docs_connector.py
│   │   ├── google_slides_connector.py
│   │   ├── github_connector.py
│   │   └── local_files.py
│   ├── scheduler/          # Task automation
│   │   ├── task_scheduler.py
│   │   └── auto_emailer.py
│   └── web/                # Flask web application
│       ├── app.py          # Main Flask app
│       ├── templates/      # HTML templates
│       └── static/         # CSS and assets
├── tests/                  # Unit tests
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🎯 Usage Guide

### Chat Interface

The chat interface provides context-aware conversations with the AI agent. Simply type your question and get intelligent responses.

**Example queries:**
- "Analyze our Q4 sales performance"
- "What factors should I consider for inventory planning?"
- "Summarize this document"

### Data Analysis

Upload or paste data in various formats (CSV, JSON, text) and select the analysis type:
- **General**: Overall insights and patterns
- **Financial**: Profitability, trends, financial health
- **Sales**: Sales patterns, trends, forecasts
- **Inventory**: Stock levels, turnover analysis

### File Management

- Browse local files
- Search files by name
- Read file contents
- Analyze documents with AI

### Decision Support

Get AI-powered recommendations for business decisions:
1. Enter the decision title
2. Provide context and background
3. List possible options
4. Get detailed pros/cons analysis with recommendations

## 🔧 Advanced Configuration

### Auto-Start on System Boot

#### macOS (LaunchAgent)

Create a plist file at `~/Library/LaunchAgents/com.vmart.agent.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vmart.agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/V-Mart Personal AI Agent/main.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load it with:
```bash
launchctl load ~/Library/LaunchAgents/com.vmart.agent.plist
```

#### Linux (systemd)

Create `/etc/systemd/system/vmart-agent.service`:

```ini
[Unit]
Description=V-Mart Personal AI Agent
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/V-Mart Personal AI Agent
ExecStart=/usr/bin/python3 /path/to/V-Mart Personal AI Agent/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable vmart-agent
sudo systemctl start vmart-agent
```

#### Windows (Task Scheduler)

Use the Windows Task Scheduler to run `main.py` on system startup.

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 🤝 Contributing

This is a private project for V-Mart Retail. For feature requests or issues, contact the development team.

## 📝 License

Proprietary - V-Mart Retail Ltd.

## 🆘 Support

For support, contact:
- Email: support@vmartretail.com
- Internal Slack: #ai-agent-support

## 🔄 Updates

The agent automatically stays updated with the latest Gemini AI capabilities. Regular dependency updates are recommended:

```bash
pip install --upgrade -r requirements.txt
```

## ⚠️ Important Notes

1. **Security**: Never commit your `.env` file to version control
2. **API Limits**: Be mindful of Google API quotas
3. **Costs**: Gemini API usage may incur costs - monitor your usage
4. **Data Privacy**: Ensure sensitive data is handled according to company policies

## 🎉 Acknowledgments

- Google Gemini AI team for the powerful LLM
- Google Cloud team for excellent APIs
- V-Mart IT team for support and testing
