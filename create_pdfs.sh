#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║   V-Mart AI Agent - Documentation to PDF Converter              ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Create PDF directory
mkdir -p pdf/docs

# Check if pandoc is available
if command -v pandoc &> /dev/null; then
    CONVERTER="pandoc"
    echo "✓ Using pandoc for conversion"
elif command -v textutil &> /dev/null; then
    CONVERTER="textutil"
    echo "✓ Using macOS textutil for conversion"
else
    echo "❌ No PDF converter available. Installing pandoc..."
    brew install pandoc
    CONVERTER="pandoc"
fi

echo ""
echo "Converting documentation files:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Function to convert with pandoc
convert_with_pandoc() {
    local input="$1"
    local output="$2"
    
    pandoc "$input" \
        -o "$output" \
        --pdf-engine=wkhtmltopdf \
        --variable geometry:margin=1in \
        --variable fontsize=11pt \
        --variable mainfont="Helvetica" \
        --toc \
        --metadata title="V-Mart AI Agent - $(basename "$input" .md)" \
        --metadata date="$(date '+%B %d, %Y')" \
        2>/dev/null
}

# Function to convert with HTML intermediate (fallback)
convert_via_html() {
    local input="$1"
    local output="$2"
    local html_temp="$(mktemp).html"
    
    # Create HTML with styling
    cat > "$html_temp" << 'HTMLHEAD'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            color: #333;
        }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; border-bottom: 2px solid #95a5a6; padding-bottom: 5px; }
        code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        pre { background-color: #f8f8f8; border: 1px solid #ddd; padding: 15px; border-radius: 5px; overflow-x: auto; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        table th { background-color: #3498db; color: white; padding: 12px; }
        table td { border: 1px solid #ddd; padding: 10px; }
    </style>
</head>
<body>
HTMLHEAD
    
    # Convert markdown to HTML and append
    python3 -c "import markdown2; print(markdown2.markdown(open('$input').read(), extras=['fenced-code-blocks', 'tables']))" >> "$html_temp"
    
    echo "</body></html>" >> "$html_temp"
    
    # Convert HTML to PDF using cupsfilter (macOS built-in)
    cupsfilter "$html_temp" > "$output" 2>/dev/null || \
    textutil -convert pdf -output "$output" "$html_temp" 2>/dev/null
    
    rm "$html_temp"
}

# List of files to convert
declare -a FILES=(
    "README.md:pdf/README.pdf"
    "QUICK_SETUP.md:pdf/QUICK_SETUP.pdf"
    "CUSTOM_DOMAIN_SETUP.md:pdf/CUSTOM_DOMAIN_SETUP.pdf"
    "DOCUMENT_SEARCH_FEATURE.md:pdf/DOCUMENT_SEARCH_FEATURE.pdf"
    "docs/SETUP_GUIDE.md:pdf/docs/SETUP_GUIDE.pdf"
    "docs/USER_GUIDE.md:pdf/docs/USER_GUIDE.pdf"
    "docs/API_REFERENCE.md:pdf/docs/API_REFERENCE.pdf"
    "docs/ARCHITECTURE_SUMMARY.md:pdf/docs/ARCHITECTURE_SUMMARY.pdf"
    "docs/architecture.md:pdf/docs/ARCHITECTURE.pdf"
    "docs/CHATBOT_INTERFACE_GUIDE.md:pdf/docs/CHATBOT_INTERFACE_GUIDE.pdf"
    "docs/GOOGLE_OAUTH_SETUP.md:pdf/docs/GOOGLE_OAUTH_SETUP.pdf"
    "docs/SERVICE_24x7_SETUP.md:pdf/docs/SERVICE_24x7_SETUP.pdf"
)

SUCCESS=0
FAILED=0

# Convert each file
for file_pair in "${FILES[@]}"; do
    IFS=':' read -r input output <<< "$file_pair"
    
    if [ ! -f "$input" ]; then
        printf "⚠ %-50s → Skipped (not found)\n" "$input"
        continue
    fi
    
    # Try conversion
    convert_via_html "$input" "$output"
    
    if [ -f "$output" ] && [ -s "$output" ]; then
        size=$(du -h "$output" | cut -f1)
        printf "✓ %-50s → %s (%s)\n" "$input" "$(basename "$output")" "$size"
        ((SUCCESS++))
    else
        printf "✗ %-50s → Failed\n" "$input"
        ((FAILED++))
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Conversion complete: $SUCCESS successful, $FAILED failed"
echo ""
echo "📦 PDF files created in: pdf/"
echo ""

# List all PDFs
if [ -d "pdf" ]; then
    echo "📄 Generated PDFs:"
    find pdf -name "*.pdf" -type f | while read pdf; do
        size=$(du -h "$pdf" | cut -f1)
        echo "   • $pdf ($size)"
    done
fi

echo ""
echo "🚀 Ready to commit and push to GitHub!"
echo ""
