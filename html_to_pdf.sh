#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║   Converting HTML files to PDF using macOS built-in tools        ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

SUCCESS=0
FAILED=0

# Find all HTML files in pdf directory
find pdf -name "*.html" -type f | sort | while read html_file; do
    pdf_file="${html_file%.html}.pdf"
    
    # Convert using cupsfilter (macOS built-in)
    if cupsfilter "$html_file" > "$pdf_file" 2>/dev/null && [ -s "$pdf_file" ]; then
        size=$(du -h "$pdf_file" | cut -f1)
        printf "✓ %-60s (%s)\n" "$(basename "$pdf_file")" "$size"
        ((SUCCESS++))
        
        # Remove HTML after successful conversion
        rm "$html_file"
    else
        printf "✗ %-60s (failed)\n" "$(basename "$html_file")"
        ((FAILED++))
    fi
done

echo ""
echo "✅ Conversion complete: $SUCCESS PDFs created"
echo ""

# List all PDFs
if [ $SUCCESS -gt 0 ]; then
    echo "📄 Generated PDF files:"
    find pdf -name "*.pdf" -type f | sort | while read pdf_file; do
        size=$(du -h "$pdf_file" | cut -f1)
        echo "   • $pdf_file ($size)"
    done
    echo ""
    
    total_size=$(du -sh pdf 2>/dev/null | cut -f1)
    echo "📦 Total size: $total_size"
fi

echo ""
echo "🚀 Ready to push to GitHub!"
echo ""
