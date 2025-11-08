# 🔐 Google OAuth Setup Guide

## Complete Guide to Get Google OAuth Credentials

This guide will help you set up Google OAuth authentication for the V-Mart AI Agent to access Gmail, Google Drive, Google Docs, Sheets, and Slides.

---

## 📋 Prerequisites

- A Google Account (Gmail)
- Access to [Google Cloud Console](https://console.cloud.google.com)
- Your project: `gen-lang-client-0157247224`

---

## 🚀 Step-by-Step Setup

### Step 1: Access Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Sign in with your Google account
3. Click on the project dropdown at the top
4. Select your project: **gen-lang-client-0157247224**

   If you don't see it, click "Select a project" → Find `gen-lang-client-0157247224`

---

### Step 2: Enable Required APIs

You need to enable these APIs for the AI agent to work:

1. In the left sidebar, go to **"APIs & Services"** → **"Library"**

2. Search for and enable each of these APIs:

   **Essential APIs:**
   - ✅ **Gmail API** - For reading/sending emails
   - ✅ **Google Drive API** - For accessing Drive files
   - ✅ **Google Docs API** - For reading Google Docs
   - ✅ **Google Sheets API** - For reading spreadsheets
   - ✅ **Google Slides API** - For reading presentations
   - ✅ **Google People API** - For user info

   **How to Enable:**
   - Click on each API name
   - Click the blue **"ENABLE"** button
   - Wait for it to activate (usually takes a few seconds)
   - Repeat for all APIs above

---

### Step 3: Configure OAuth Consent Screen

This is what users see when they authorize your app.

1. Go to **"APIs & Services"** → **"OAuth consent screen"**

2. Choose User Type:
   - Select **"External"** (for testing with any Google account)
   - Click **"CREATE"**

3. Fill in App Information:
   ```
   App name: V-Mart AI Agent
   User support email: [Your email]
   App logo: (Optional - skip for now)
   ```

4. App Domain (Optional for testing):
   ```
   Application home page: http://localhost:8000
   Application privacy policy link: (skip for testing)
   Application terms of service link: (skip for testing)
   ```

5. Developer Contact Information:
   ```
   Email addresses: [Your email]
   ```

6. Click **"SAVE AND CONTINUE"**

7. **Scopes Screen** - Add these scopes:
   
   Click **"ADD OR REMOVE SCOPES"**
   
   Search for and select:
   - ✅ `https://www.googleapis.com/auth/gmail.readonly` - Read Gmail
   - ✅ `https://www.googleapis.com/auth/gmail.send` - Send Gmail
   - ✅ `https://www.googleapis.com/auth/drive.readonly` - Read Drive files
   - ✅ `https://www.googleapis.com/auth/documents.readonly` - Read Google Docs
   - ✅ `https://www.googleapis.com/auth/spreadsheets.readonly` - Read Sheets
   - ✅ `https://www.googleapis.com/auth/presentations.readonly` - Read Slides
   - ✅ `https://www.googleapis.com/auth/userinfo.profile` - User profile
   - ✅ `https://www.googleapis.com/auth/userinfo.email` - User email

   Click **"UPDATE"** → **"SAVE AND CONTINUE"**

8. **Test Users** (Important for External apps):
   
   Click **"ADD USERS"**
   
   Add your Gmail address (the one you'll use to test)
   
   Click **"ADD"** → **"SAVE AND CONTINUE"**

9. Review and click **"BACK TO DASHBOARD"**

---

### Step 4: Create OAuth Client ID

Now create the actual credentials:

1. Go to **"APIs & Services"** → **"Credentials"**

2. Click **"+ CREATE CREDENTIALS"** at the top

3. Select **"OAuth client ID"**

4. Configure the OAuth client:
   ```
   Application type: Web application
   Name: V-Mart AI Agent Web Client
   ```

5. **Authorized JavaScript origins:**
   
   Click **"+ ADD URI"** and add:
   ```
   http://localhost:8000
   http://127.0.0.1:8000
   ```

6. **Authorized redirect URIs:**
   
   Click **"+ ADD URI"** and add:
   ```
   http://localhost:8000/auth/callback
   http://127.0.0.1:8000/auth/callback
   ```

7. Click **"CREATE"**

---

### Step 5: Download Credentials

After creating, you'll see a popup with your credentials:

1. **Copy Your Client ID:**
   ```
   Example: YOUR_CLIENT_ID.apps.googleusercontent.com
   ```

2. **Copy Your Client Secret:**
   ```
   Example: GOCSPX-YourSecretHere
   ```

3. Click **"DOWNLOAD JSON"** - This downloads `client_secret_xxxxx.json`

4. **Optional:** Click "OK" to close the popup

---

### Step 6: Add Credentials to Your App

Now update your `.env` file:

1. Open the file in your editor:
   ```bash
   cd "/Users/dineshsrivastava/Ai Chatbot for Gemini LLM/V-Mart Personal AI Agent"
   nano .env
   ```

2. Add these lines (replace with YOUR actual values):
   ```env
   # Google OAuth Credentials
   GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
   GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
   ```

3. Example with your values:
   ```env
   # Google OAuth Credentials
   GOOGLE_CLIENT_ID=123456789012-abc123xyz789.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=GOCSPX-AbCdEfGhIjKlMnOpQrStUv
   GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
   
   # Gemini API Key (already configured)
   GEMINI_API_KEY=AIzaSyCZ-XAV_EoRgs-KX429Z5UuKs87XBh1cFw
   
   # Server Config
   HOST=0.0.0.0
   PORT=8000
   SECRET_KEY=37d53f13221533b6d33b4f16dba8bc8b4e1a938759d20980439099b914efe80
   FLASK_DEBUG=True
   ```

4. Save the file:
   - Press `Ctrl + O` (save)
   - Press `Enter` (confirm)
   - Press `Ctrl + X` (exit)

---

### Step 7: Test OAuth Login

1. **Restart the server:**
   ```bash
   cd "/Users/dineshsrivastava/Ai Chatbot for Gemini LLM/V-Mart Personal AI Agent"
   python3 main.py
   ```

2. **Open the app:**
   - Go to http://localhost:8000
   - Click "Login with Google"
   - You'll see a Google consent screen

3. **Authorize the app:**
   - Google may show a warning "This app isn't verified" - this is normal for testing
   - Click **"Advanced"** → **"Go to V-Mart AI Agent (unsafe)"**
   - Review the permissions
   - Click **"Allow"**
   - You'll be redirected back to the app

4. **You're logged in!**
   - Now the chatbot can access your Gmail, Drive, Docs, Sheets, and Slides
   - Try asking: "Show me my recent emails" or "Search my Google Drive"

---

## 🔍 Quick Reference

### Your Project Details:
```
Project ID: gen-lang-client-0157247224
Gemini API Key: AIzaSyCZ-XAV_EoRgs-KX429Z5UuKs87XBh1cFw (already working)
```

### Google Cloud Console Links:
- **Main Console:** https://console.cloud.google.com
- **API Library:** https://console.cloud.google.com/apis/library
- **OAuth Consent:** https://console.cloud.google.com/apis/credentials/consent
- **Credentials:** https://console.cloud.google.com/apis/credentials

### Required Scopes:
```
gmail.readonly
gmail.send
drive.readonly
documents.readonly
spreadsheets.readonly
presentations.readonly
userinfo.profile
userinfo.email
```

---

## ⚠️ Important Notes

### Testing Phase:
- Your OAuth app is in "Testing" mode by default
- Only test users you add can log in
- Maximum 100 test users
- Perfect for development

### Publishing (Optional - for production):
- When ready for public use, go to OAuth consent screen
- Click "PUBLISH APP"
- Google may review your app (can take days/weeks)
- Not needed for personal use

### Security Tips:
- ✅ Never share your Client Secret publicly
- ✅ Keep your `.env` file private (it's in `.gitignore`)
- ✅ Use localhost URIs for development
- ✅ Add production domains when deploying

---

## 🐛 Troubleshooting

### Error: "redirect_uri_mismatch"
**Solution:** Make sure the redirect URI in `.env` exactly matches one in Google Console:
```
http://localhost:8000/auth/callback
```

### Error: "Access blocked: This app's request is invalid"
**Solution:** Enable all required APIs in Step 2

### Error: "This app isn't verified"
**Solution:** This is normal for testing. Click "Advanced" → "Go to V-Mart AI Agent"

### Can't see the project
**Solution:** Make sure you're signed in with the correct Google account

### OAuth consent screen missing scopes
**Solution:** Go back to OAuth consent screen → Scopes → Add the missing scopes

---

## ✅ Verification Checklist

Before testing, verify:

- [ ] All 6 APIs are enabled (Gmail, Drive, Docs, Sheets, Slides, People)
- [ ] OAuth consent screen is configured
- [ ] Your email is added as a test user
- [ ] OAuth Client ID is created (Web application type)
- [ ] Redirect URIs include `http://localhost:8000/auth/callback`
- [ ] `.env` file has GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
- [ ] Server is restarted after updating `.env`

---

## 📞 Need Help?

If you encounter issues:

1. Check the browser console for errors (F12 → Console tab)
2. Check the terminal where the server is running for error messages
3. Verify all credentials are copied correctly (no extra spaces)
4. Make sure you're using the same Google account you added as a test user

---

**Developed by: DSR | Inspired by: LA | Powered by: Gemini AI**
