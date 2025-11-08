#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║   V-Mart AI Agent - Documentation to PDF Converter              ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Create PDF directory
mkdir -p pdf/docs

echo "Converting documentation files using Pandoc:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

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
    
    # Get title from filename
    title=$(basename "$input" .md | tr '_-' '  ' | sed 's/\b\(.\)/\u\1/g')
    
    # Convert with Pandoc
    pandoc "$input" \
        -o "$output" \
        --from=markdown \
        --to=pdf \
        --pdf-engine=pdflatex \
        --variable geometry:margin=1in \
        --variable fontsize=11pt \
        --variable colorlinks=true \
        --variable linkcolor=blue \
        --variable urlcolor=blue \
        --toc \
        --toc-depth=3 \
        --number-sections \
        --highlight-style=tango \
        --metadata title="V-Mart AI Agent: $title" \
        --metadata date="$(date '+%B %d, %Y')" \
        --metadata author="V-Mart Personal AI Agent" \
        2>/dev/null
    
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

# List all PDFs with sizes
if [ $SUCCESS -gt 0 ]; then
    echo "📄 Generated PDFs:"
    find pdf -name "*.pdf" -type f -size +0 | sort | while read pdf_file; do
        size=$(du -h "$pdf_file" | cut -f1)
        echo "   • $pdf_file ($size)"
    done
    echo ""
    
    total_size=$(du -sh pdf 2>/dev/null | cut -f1)
    echo "📦 Total size: $total_size"
    echo ""
fi

echo "🚀 Ready to commit and push to GitHub!"
echo ""
