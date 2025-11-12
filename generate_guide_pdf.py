#!/usr/bin/env python3
"""Generate professional PDF from V-Mart AI Agent Guide"""

import os

import markdown
from weasyprint import HTML


def generate_pdf():
    """Convert markdown guide to professional PDF"""

    # Read markdown content
    md_file = "V-MART_AI_AGENT_COMPLETE_GUIDE.md"
    pdf_file = "V-Mart_Retail_Personal_AI_Agent_Complete_Guide.pdf"

    print(f"📖 Reading {md_file}...")
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert markdown to HTML
    print("🔄 Converting to HTML...")
    html_body = markdown.markdown(
        md_content, extensions=["extra", "toc", "tables", "fenced_code", "nl2br"]
    )

    # Create styled HTML
    print("🎨 Applying professional styling...")
    html_document = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>V-Mart Retail Personal AI Agent - Complete Guide</title>
    <style>
        @page {{
            size: A4;
            margin: 2.5cm 2cm;
            @top-right {{
                content: "V-Mart AI Agent Guide";
                font-size: 9pt;
                color: #666;
                font-family: Arial, sans-serif;
            }}
            @bottom-center {{
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #666;
                font-family: Arial, sans-serif;
            }}
        }}
        
        @page :first {{
            @top-right {{
                content: none;
            }}
            @bottom-center {{
                content: none;
            }}
        }}
        
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.7;
            color: #2c3e50;
            font-size: 11pt;
            background: white;
        }}
        
        h1 {{
            color: #1a237e;
            font-family: 'Arial', sans-serif;
            font-size: 28pt;
            font-weight: bold;
            border-bottom: 4px solid #1a237e;
            padding-bottom: 12px;
            margin-top: 40px;
            margin-bottom: 20px;
            page-break-before: always;
        }}
        
        h1:first-of-type {{
            page-break-before: avoid;
            font-size: 36pt;
            text-align: center;
            border-bottom: none;
            margin-top: 60px;
            margin-bottom: 10px;
        }}
        
        h2 {{
            color: #283593;
            font-family: 'Arial', sans-serif;
            font-size: 20pt;
            font-weight: bold;
            border-bottom: 3px solid #3949ab;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 15px;
            page-break-after: avoid;
        }}
        
        h3 {{
            color: #3949ab;
            font-family: 'Arial', sans-serif;
            font-size: 16pt;
            font-weight: bold;
            margin-top: 25px;
            margin-bottom: 12px;
            page-break-after: avoid;
        }}
        
        h4 {{
            color: #5c6bc0;
            font-family: 'Arial', sans-serif;
            font-size: 13pt;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            page-break-after: avoid;
        }}
        
        p {{
            margin: 12px 0;
            text-align: justify;
            orphans: 3;
            widows: 3;
        }}
        
        ul, ol {{
            margin: 12px 0 12px 25px;
            line-height: 1.8;
        }}
        
        li {{
            margin: 8px 0;
            orphans: 2;
            widows: 2;
        }}
        
        strong {{
            color: #1a237e;
            font-weight: bold;
        }}
        
        em {{
            color: #3949ab;
            font-style: italic;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #e0e0e0;
            margin: 25px 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }}
        
        th {{
            background-color: #1a237e;
            color: white;
            padding: 12px 10px;
            text-align: left;
            font-weight: bold;
            font-family: Arial, sans-serif;
        }}
        
        td {{
            border: 1px solid #ddd;
            padding: 10px;
            vertical-align: top;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        blockquote {{
            border-left: 5px solid #1a237e;
            padding-left: 20px;
            margin: 20px 0;
            color: #555;
            font-style: italic;
            background-color: #f5f5f5;
            padding: 15px 20px;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            color: #c7254e;
        }}
        
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-left: 4px solid #1a237e;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            line-height: 1.4;
            margin: 15px 0;
        }}
        
        .toc {{
            background-color: #f8f9fa;
            padding: 20px;
            border: 2px solid #1a237e;
            margin: 30px 0;
            page-break-inside: avoid;
        }}
        
        .cover-info {{
            text-align: center;
            color: #666;
            font-size: 12pt;
            margin: 20px 0;
            line-height: 2;
        }}
        
        .footer-info {{
            text-align: center;
            color: #888;
            font-size: 9pt;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }}
        
        /* Prevent orphaned headers */
        h1, h2, h3, h4, h5, h6 {{
            page-break-after: avoid;
        }}
        
        /* Keep content together when possible */
        .keep-together {{
            page-break-inside: avoid;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

    # Generate PDF
    print("📄 Generating PDF...")
    HTML(string=html_document).write_pdf(pdf_file)

    # Check file size
    file_size = os.path.getsize(pdf_file) / (1024 * 1024)  # Convert to MB

    print(f"\n✅ PDF generated successfully!")
    print(f"📁 File: {pdf_file}")
    print(f"📊 Size: {file_size:.2f} MB")
    print(f"📍 Location: {os.path.abspath(pdf_file)}")

    return pdf_file


if __name__ == "__main__":
    try:
        pdf_path = generate_pdf()
        print(f"\n🎉 Success! You can now open the PDF:")
        print(f"   open '{pdf_path}'")
    except Exception as e:
        print(f"\n❌ Error generating PDF: {e}")
        import traceback

        traceback.print_exc()
