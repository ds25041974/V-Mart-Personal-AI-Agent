# PDF Documentation

This directory contains HTML versions of all V-Mart AI Agent documentation that can be easily converted to PDF.

## Available Documentation

### Main Documentation
- **README.html** - Project overview and quick start
- **QUICK_SETUP.html** - Fast setup guide
- **CUSTOM_DOMAIN_SETUP.html** - Custom domain configuration
- **DOCUMENT_SEARCH_FEATURE.html** - Document search functionality

### Detailed Guides (in `docs/` folder)
- **SETUP_GUIDE.html** - Complete installation and setup instructions
- **USER_GUIDE.html** - User manual with examples
- **API_REFERENCE.html** - API documentation and reference
- **ARCHITECTURE.html** - System architecture and design
- **ARCHITECTURE_SUMMARY.html** - Quick architecture overview
- **CHATBOT_INTERFACE_GUIDE.html** - Comprehensive UI guide (all 4 tabs)
- **GOOGLE_OAUTH_SETUP.html** - Google OAuth configuration
- **SERVICE_24x7_SETUP.html** - 24x7 service setup guide

## How to Convert HTML to PDF

### Method 1: Browser (Easiest)
1. Open any HTML file in your browser (Safari, Chrome, Firefox)
2. Press `Cmd+P` (Mac) or `Ctrl+P` (Windows/Linux)
3. Select "Save as PDF" as the destination
4. Click "Save"

### Method 2: Command Line (macOS)
```bash
# Using wkhtmltopdf (install first: brew install wkhtmltopdf)
wkhtmltopdf pdf/README.html pdf/README.pdf

# Or convert all at once
for file in pdf/*.html pdf/docs/*.html; do
    wkhtmltopdf "$file" "${file%.html}.pdf"
done
```

### Method 3: Command Line (Linux)
```bash
# Using wkhtmltopdf
wkhtmltopdf pdf/README.html pdf/README.pdf

# Or using pandoc
pandoc pdf/README.html -o pdf/README.pdf
```

### Method 4: Command Line (Windows)
```powershell
# Using wkhtmltopdf
wkhtmltopdf pdf\README.html pdf\README.pdf
```

## Features of HTML Documentation

✅ **Fully styled** - Professional formatting with syntax highlighting  
✅ **Self-contained** - No external dependencies  
✅ **Print-ready** - Optimized for PDF conversion  
✅ **Mobile-friendly** - Responsive design  
✅ **Table of Contents** - Easy navigation  
✅ **Numbered sections** - Clear structure  
✅ **Code highlighting** - Beautiful code blocks  

## File Sizes

| Document | Size | Description |
|----------|------|-------------|
| README.html | 40K | Project overview |
| QUICK_SETUP.html | 20K | Quick start |
| CUSTOM_DOMAIN_SETUP.html | 16K | Domain setup |
| DOCUMENT_SEARCH_FEATURE.html | 16K | Search feature |
| SETUP_GUIDE.html | 108K | Complete setup |
| USER_GUIDE.html | 44K | User manual |
| API_REFERENCE.html | 76K | API docs |
| ARCHITECTURE.html | 112K | Architecture |
| CHATBOT_INTERFACE_GUIDE.html | 136K | UI guide (largest) |
| GOOGLE_OAUTH_SETUP.html | 28K | OAuth setup |
| SERVICE_24x7_SETUP.html | 64K | Service setup |

**Total:** ~676KB

## Why HTML Instead of PDF?

1. **Smaller file sizes** - HTML is more compact
2. **Better for web viewing** - Can be hosted on GitHub Pages
3. **Searchable** - Full-text search in browser
4. **Accessible** - Works on all devices
5. **Easy to update** - Regenerate from markdown anytime
6. **Print to PDF** - Anyone can convert when needed

## Regenerating Documentation

To regenerate HTML files from markdown:

```bash
./convert_docs.sh
```

This will create fresh HTML files from all markdown documentation.

---

**Generated:** November 8, 2025  
**Project:** V-Mart Personal AI Agent  
**Repository:** https://github.com/ds25041974/V-Mart-Personal-AI-Agent
