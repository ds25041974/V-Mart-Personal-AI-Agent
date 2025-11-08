#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║   V-Mart AI Agent - Documentation to HTML/PDF Converter         ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "Note: Creating standalone HTML files that can be printed to PDF"
echo ""

# Create output directory
mkdir -p pdf/docs

echo "Converting documentation files:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# List of files to convert
declare -a FILES=(
    "README.md:pdf/README.html"
    "QUICK_SETUP.md:pdf/QUICK_SETUP.html"
    "CUSTOM_DOMAIN_SETUP.md:pdf/CUSTOM_DOMAIN_SETUP.html"
    "DOCUMENT_SEARCH_FEATURE.md:pdf/DOCUMENT_SEARCH_FEATURE.html"
    "docs/SETUP_GUIDE.md:pdf/docs/SETUP_GUIDE.html"
    "docs/USER_GUIDE.md:pdf/docs/USER_GUIDE.html"
    "docs/API_REFERENCE.md:pdf/docs/API_REFERENCE.html"
    "docs/ARCHITECTURE_SUMMARY.md:pdf/docs/ARCHITECTURE_SUMMARY.html"
    "docs/architecture.md:pdf/docs/ARCHITECTURE.html"
    "docs/CHATBOT_INTERFACE_GUIDE.md:pdf/docs/CHATBOT_INTERFACE_GUIDE.html"
    "docs/GOOGLE_OAUTH_SETUP.md:pdf/docs/GOOGLE_OAUTH_SETUP.html"
    "docs/SERVICE_24x7_SETUP.md:pdf/docs/SERVICE_24x7_SETUP.html"
)

SUCCESS=0
FAILED=0

# Convert each file to HTML
for file_pair in "${FILES[@]}"; do
    IFS=':' read -r input output <<< "$file_pair"
    
    if [ ! -f "$input" ]; then
        printf "⚠ %-50s → Skipped (not found)\n" "$input"
        continue
    fi
    
    # Get title from filename
    title=$(basename "$input" .md | tr '_-' '  ' | sed 's/\b\(.\)/\u\1/g')
    
    # Convert with Pandoc to standalone HTML with CSS
    pandoc "$input" \
        -o "$output" \
        --from=markdown \
        --to=html5 \
        --standalone \
        --self-contained \
        --toc \
        --toc-depth=3 \
        --number-sections \
        --highlight-style=tango \
        --css=<(echo '
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                line-height: 1.6;
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
                color: #333;
            }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            h2 { color: #34495e; border-bottom: 2px solid #95a5a6; padding-bottom: 5px; margin-top: 30px; }
            h3 { color: #555; margin-top: 20px; }
            code {
                background-color: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: "Monaco", "Courier New", monospace;
            }
            pre {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }
            pre code { background-color: transparent; padding: 0; }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }
            table th {
                background-color: #3498db;
                color: white;
                padding: 12px;
                text-align: left;
            }
            table td {
                border: 1px solid #ddd;
                padding: 10px;
            }
            table tr:nth-child(even) { background-color: #f9f9f9; }
            blockquote {
                border-left: 4px solid #3498db;
                padding-left: 20px;
                margin: 20px 0;
                color: #555;
            }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .header {
                text-align: center;
                margin-bottom: 40px;
                padding-bottom: 20px;
                border-bottom: 3px solid #3498db;
            }
            @media print {
                body { margin: 0; padding: 20px; }
                a { color: #000; }
            }
        ') \
        --metadata title="V-Mart AI Agent: $title" \
        --metadata date="$(date '+%B %d, %Y')" \
        2>/dev/null
    
    if [ -f "$output" ] && [ -s "$output" ]; then
        # Now convert HTML to PDF using macOS print function
        pdf_output="${output%.html}.pdf"
        
        # Try using Pandoc with prince or weasyprint if available
        # Otherwise, keep HTML for manual conversion
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
echo "✅ Conversion complete: $SUCCESS HTML files created, $FAILED failed"
echo ""

if [ $SUCCESS -gt 0 ]; then
    echo "📄 Generated HTML files (ready for PDF conversion):"
    find pdf -name "*.html" -type f | sort | while read html_file; do
        size=$(du -h "$html_file" | cut -f1)
        echo "   • $html_file ($size)"
    done
    echo ""
    
    total_size=$(du -sh pdf 2>/dev/null | cut -f1)
    echo "📦 Total size: $total_size"
    echo ""
    
    echo "📝 To convert HTML to PDF:"
    echo "   1. Open each HTML file in Safari/Chrome"
    echo "   2. Press Cmd+P (Print)"
    echo "   3. Click 'Save as PDF'"
    echo ""
    echo "   OR use this automated script:"
    echo "   ./html_to_pdf.sh"
    echo ""
fi

echo "🚀 HTML files ready to commit and push to GitHub!"
echo ""
