# Custom Domain Setup: vmartai

## Quick Setup

To access your V-Mart AI Agent at `http://vmartai:5000` instead of `http://localhost:5000`, follow these simple steps:

### Option 1: Automatic Setup (Recommended)

Run this command and enter your password when prompted:

```bash
echo "127.0.0.1       vmartai" | sudo tee -a /etc/hosts
```

### Option 2: Manual Setup

1. Open Terminal
2. Edit the hosts file:
   ```bash
   sudo nano /etc/hosts
   ```

3. Add this line at the end of the file:
   ```
   127.0.0.1       vmartai
   ```

4. Save and exit:
   - Press `Ctrl + O` (to save)
   - Press `Enter` (to confirm)
   - Press `Ctrl + X` (to exit)

### Verify Setup

Test that vmartai is working:

```bash
# Test the domain
curl http://vmartai:5000/health

# Or open in browser
open http://vmartai:5000
```

## Access URLs

After setup, you can use either:

- **Custom Domain:** `http://vmartai:5000`
- **Standard:** `http://localhost:5000`

Both URLs point to the same V-Mart AI Agent application.

## What This Does

The hosts file tells your Mac that when you type `vmartai`, it should connect to `127.0.0.1` (localhost). This is:

- ✅ **Local only** - Works only on your Mac
- ✅ **No internet required** - Completely offline
- ✅ **Secure** - No external access
- ✅ **Simple** - Just a name alias

## Remove Custom Domain (Optional)

If you want to remove the vmartai domain later:

```bash
sudo sed -i '' '/vmartai/d' /etc/hosts
```

## Troubleshooting

### Domain not working?

1. **Verify hosts entry:**
   ```bash
   cat /etc/hosts | grep vmartai
   ```
   
   Should show: `127.0.0.1       vmartai`

2. **Flush DNS cache:**
   ```bash
   sudo dscacheutil -flushcache
   sudo killall -HUP mDNSResponder
   ```

3. **Test with ping:**
   ```bash
   ping vmartai
   ```
   
   Should show: `PING vmartai (127.0.0.1)`

### Permission denied?

You need administrator privileges. Make sure to use `sudo` and enter your Mac password.

## Benefits

- 🎯 **Easier to remember:** `vmartai` vs `localhost:5000`
- 🚀 **Professional:** Looks cleaner in browser bookmarks
- 💼 **Branded:** Uses your V-Mart AI branding
- 🔧 **Flexible:** Can change port without updating URL

---

**Note:** This is a local-only setup. The vmartai domain will only work on your Mac.
