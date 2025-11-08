#!/usr/bin/env python3
"""
Convert all markdown documentation to PDF format
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import markdown2
from weasyprint import CSS, HTML

# Configuration
PROJECT_ROOT = Path(__file__).parent
DOCS_DIR = PROJECT_ROOT / "docs"
PDF_DIR = PROJECT_ROOT / "pdf"

# Markdown files to convert
MD_FILES = [
    "README.md",
    "QUICK_SETUP.md",
    "CUSTOM_DOMAIN_SETUP.md",
    "DOCUMENT_SEARCH_FEATURE.md",
    "docs/SETUP_GUIDE.md",
    "docs/USER_GUIDE.md",
    "docs/API_REFERENCE.md",
    "docs/ARCHITECTURE_SUMMARY.md",
    "docs/architecture.md",
    "docs/CHATBOT_INTERFACE_GUIDE.md",
    "docs/GOOGLE_OAUTH_SETUP.md",
    "docs/SERVICE_24x7_SETUP.md",
]

# CSS for PDF styling
PDF_CSS = """
@page {
    size: A4;
    margin: 2cm;
    @bottom-right {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 9pt;
        color: #666;
    }
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    font-size: 11pt;
}

h1 {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
    margin-top: 30px;
    page-break-after: avoid;
}

h2 {
    color: #34495e;
    border-bottom: 2px solid #95a5a6;
    padding-bottom: 5px;
    margin-top: 25px;
    page-break-after: avoid;
}

h3 {
    color: #555;
    margin-top: 20px;
    page-break-after: avoid;
}

code {
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Monaco', 'Courier New', monospace;
    font-size: 10pt;
}

pre {
    background-color: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 15px;
    overflow-x: auto;
    page-break-inside: avoid;
}

pre code {
    background-color: transparent;
    padding: 0;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
    page-break-inside: avoid;
}

table th {
    background-color: #3498db;
    color: white;
    padding: 12px;
    text-align: left;
    font-weight: bold;
}

table td {
    border: 1px solid #ddd;
    padding: 10px;
}

table tr:nth-child(even) {
    background-color: #f9f9f9;
}

blockquote {
    border-left: 4px solid #3498db;
    padding-left: 20px;
    margin: 20px 0;
    color: #555;
    font-style: italic;
}

ul, ol {
    margin: 15px 0;
    padding-left: 30px;
}

li {
    margin: 8px 0;
}

a {
    color: #3498db;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.header {
    text-align: center;
    margin-bottom: 40px;
    padding-bottom: 20px;
    border-bottom: 3px solid #3498db;
}

.header h1 {
    color: #2c3e50;
    margin: 10px 0;
    border: none;
}

.header p {
    color: #7f8c8d;
    font-size: 10pt;
}

.toc {
    background-color: #f8f9fa;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 20px;
    margin: 30px 0;
    page-break-inside: avoid;
}

.toc h2 {
    margin-top: 0;
    border: none;
}

img {
    max-width: 100%;
    height: auto;
}

hr {
    border: none;
    border-top: 2px solid #ddd;
    margin: 30px 0;
}
"""


def create_pdf_header(title: str) -> str:
    """Create a nice header for the PDF"""
    return f"""
    <div class="header">
        <h1>V-Mart Personal AI Agent</h1>
        <h1>{title}</h1>
        <p>Generated: {datetime.now().strftime("%B %d, %Y")}</p>
        <p>https://github.com/ds25041974/V-Mart-Personal-AI-Agent</p>
    </div>
    """


def convert_md_to_pdf(md_file: Path, output_dir: Path) -> bool:
    """Convert a markdown file to PDF"""
    try:
        # Read markdown content
        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()

        # Convert markdown to HTML
        html_content = markdown2.markdown(
            md_content,
            extras=[
                "fenced-code-blocks",
                "tables",
                "header-ids",
                "toc",
                "metadata",
                "code-friendly",
                "strike",
                "task_list",
            ],
        )

        # Create title from filename
        title = md_file.stem.replace("_", " ").replace("-", " ").title()

        # Create full HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
        </head>
        <body>
            {create_pdf_header(title)}
            {html_content}
        </body>
        </html>
        """

        # Generate PDF filename
        pdf_filename = md_file.stem + ".pdf"

        # Preserve directory structure
        if "docs" in str(md_file):
            pdf_output = output_dir / "docs" / pdf_filename
            pdf_output.parent.mkdir(parents=True, exist_ok=True)
        else:
            pdf_output = output_dir / pdf_filename

        # Convert to PDF
        HTML(string=full_html).write_pdf(pdf_output, stylesheets=[CSS(string=PDF_CSS)])

        # Get file size
        size_kb = pdf_output.stat().st_size / 1024

        print(f"✓ {md_file.name:45s} → {pdf_output.name:45s} ({size_kb:.1f} KB)")
        return True

    except Exception as e:
        print(f"✗ {md_file.name:45s} → Error: {str(e)}")
        return False


def main():
    """Main conversion function"""
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║   V-Mart AI Agent - Documentation to PDF Converter              ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    # Create PDF directory
    PDF_DIR.mkdir(exist_ok=True)
    (PDF_DIR / "docs").mkdir(exist_ok=True)

    print(f"📁 Output directory: {PDF_DIR}")
    print()
    print("Converting documentation files:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    success_count = 0
    fail_count = 0

    # Convert each markdown file
    for md_file_path in MD_FILES:
        md_file = PROJECT_ROOT / md_file_path

        if not md_file.exists():
            print(f"⚠ {md_file_path:45s} → File not found (skipped)")
            continue

        if convert_md_to_pdf(md_file, PDF_DIR):
            success_count += 1
        else:
            fail_count += 1

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print(f"✅ Conversion complete: {success_count} successful, {fail_count} failed")
    print()
    print("📦 PDF files created in:")
    print(f"   {PDF_DIR}/")
    print()

    # List all created PDFs
    pdf_files = sorted(PDF_DIR.rglob("*.pdf"))
    if pdf_files:
        print("📄 Generated PDFs:")
        for pdf_file in pdf_files:
            rel_path = pdf_file.relative_to(PROJECT_ROOT)
            size_kb = pdf_file.stat().st_size / 1024
            print(f"   • {rel_path} ({size_kb:.1f} KB)")

    print()
    print("🚀 Ready to commit and push to GitHub!")
    print()


if __name__ == "__main__":
    main()
