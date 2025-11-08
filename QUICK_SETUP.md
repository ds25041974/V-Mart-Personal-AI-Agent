# Quick Setup Guide - V-Mart Personal AI Agent

## ⚡ Get Your Gemini API Key (Required for Demo Mode)

### Step 1: Get Gemini API Key
1. Go to **[Google AI Studio](https://makersuite.google.com/app/apikey)**
2. Click **"Get API Key"** or **"Create API Key"**
3. Select or create a Google Cloud project
4. Click **"Create API Key in new project"** (or use existing project)
5. **Copy the API key** (starts with `AIza...`)

### Step 2: Update .env File
Open the `.env` file and replace:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

With your actual API key:
```
GEMINI_API_KEY=AIzaSy...your_actual_key...
```

### Step 3: Restart the Server
```bash
# Stop the current server (Ctrl+C)
python3 main.py
```

## 🔐 Full OAuth Setup (For Production - All V-Mart/Limeroad Users)

If you want to enable Google OAuth login for all users from your domains:

### Step 1: Google Cloud Console Setup
1. Go to **[Google Cloud Console](https://console.cloud.google.com)**
2. Create a new project or select existing
3. Enable **Google+ API** and **Google Identity** services

### Step 2: Create OAuth Credentials
1. Navigate to **APIs & Services > Credentials**
2. Click **"Create Credentials" > "OAuth 2.0 Client ID"**
3. Configure consent screen:
   - User Type: **Internal** (for workspace users) or **External**
   - App name: **V-Mart Personal AI Agent**
   - Authorized domains: Add `vmart.co.in`, `vmartretail.com`, `limeroad.com`
4. Create OAuth Client ID:
   - Application type: **Web application**
   - Authorized redirect URIs: `http://localhost:8000/auth/authorize`
5. **Copy Client ID and Client Secret**

### Step 3: Update .env File
```env
GOOGLE_CLIENT_ID=your_actual_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_actual_client_secret
```

### Step 4: Domain Restrictions
The app is already configured to only allow users from:
- `vmart.co.in`
- `vmartretail.com`
- `limeroad.com`

Users from other domains will be rejected automatically.

## 🧪 Demo Mode (Current Setup)

**Demo mode is already enabled!** It allows you to test the interface without OAuth:
- Click **"Enter Demo Mode"** on the home page
- This bypasses authentication for testing
- You can use all features once you add the Gemini API key

## 📝 Current Configuration Status

| Setting | Status | Required For |
|---------|--------|--------------|
| GEMINI_API_KEY | ❌ Not Set | **All features - Required!** |
| GOOGLE_CLIENT_ID | ❌ Not Set | OAuth login (optional in demo mode) |
| GOOGLE_CLIENT_SECRET | ❌ Not Set | OAuth login (optional in demo mode) |
| GITHUB_TOKEN | ❌ Not Set | GitHub integration (optional) |

## 🚀 Quick Start (Minimum Setup)

**To get started right now:**
1. Get Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Update `GEMINI_API_KEY` in `.env` file
3. Restart server: `python3 main.py`
4. Open browser: http://localhost:8000
5. Click **"Enter Demo Mode"**
6. Start chatting!

## 📚 API Key Limits

**Free Tier (Gemini API):**
- 60 requests per minute
- Perfect for testing and development

**For Production:**
- Consider upgrading to paid tier for higher limits
- Set up proper OAuth for user authentication
- Add rate limiting in the application

## ❓ Troubleshooting

### "API key not valid" Error
- Make sure you copied the entire API key (starts with `AIza`)
- Check for extra spaces or quotes in `.env` file
- Verify the key is active in [Google AI Studio](https://makersuite.google.com/app/apikey)

### OAuth Login Not Working
- For now, use **Demo Mode** to test
- Full OAuth setup requires Google Cloud Console configuration
- See "Full OAuth Setup" section above

### Server Won't Start
- Check all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version: `python3 --version` (should be 3.8+)
- Check port 8000 is not in use: `lsof -i :8000`

## 🔗 Useful Links

- [Google AI Studio (Get API Key)](https://makersuite.google.com/app/apikey)
- [Google Cloud Console](https://console.cloud.google.com)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [OAuth 2.0 Setup Guide](https://developers.google.com/identity/protocols/oauth2)
