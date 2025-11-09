#!/usr/bin/env python3
"""
V-Mart AI Agent - Release PDF Generator
Converts release documentation to professional PDF format
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class ReleasePDFGenerator:
    def __init__(self, output_dir="pdf"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Heading1"],
                fontSize=24,
                textColor=colors.HexColor("#1a1a1a"),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
            )
        )

        # Subtitle style
        self.styles.add(
            ParagraphStyle(
                name="Subtitle",
                parent=self.styles["Normal"],
                fontSize=14,
                textColor=colors.HexColor("#666666"),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName="Helvetica-Oblique",
            )
        )

        # Section header
        self.styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=self.styles["Heading2"],
                fontSize=16,
                textColor=colors.HexColor("#2c5aa0"),
                spaceAfter=12,
                spaceBefore=20,
                fontName="Helvetica-Bold",
            )
        )

        # Subsection header
        self.styles.add(
            ParagraphStyle(
                name="SubsectionHeader",
                parent=self.styles["Heading3"],
                fontSize=14,
                textColor=colors.HexColor("#4a7cb8"),
                spaceAfter=10,
                spaceBefore=15,
                fontName="Helvetica-Bold",
            )
        )

        # Code style
        self.styles.add(
            ParagraphStyle(
                name="CustomCode",
                parent=self.styles["Normal"],
                fontSize=9,
                textColor=colors.HexColor("#333333"),
                backColor=colors.HexColor("#f5f5f5"),
                borderPadding=5,
                leftIndent=20,
                rightIndent=20,
                spaceAfter=10,
                fontName="Courier",
            )
        )

        # Bullet style
        self.styles.add(
            ParagraphStyle(
                name="CustomBullet",
                parent=self.styles["Normal"],
                fontSize=11,
                leftIndent=30,
                spaceAfter=6,
                bulletIndent=10,
            )
        )

        # Info box style
        self.styles.add(
            ParagraphStyle(
                name="InfoBox",
                parent=self.styles["Normal"],
                fontSize=10,
                textColor=colors.HexColor("#0066cc"),
                backColor=colors.HexColor("#e6f2ff"),
                borderPadding=10,
                spaceAfter=15,
            )
        )

    def _add_header_footer(self, canvas, doc, title, version):
        """Add header and footer to each page"""
        canvas.saveState()

        # Header
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawString(inch, letter[1] - 0.5 * inch, f"V-Mart AI Agent {version}")
        canvas.drawRightString(
            letter[0] - inch,
            letter[1] - 0.5 * inch,
            datetime.now().strftime("%B %d, %Y"),
        )

        # Header line
        canvas.setStrokeColor(colors.HexColor("#cccccc"))
        canvas.setLineWidth(0.5)
        canvas.line(
            inch, letter[1] - 0.6 * inch, letter[0] - inch, letter[1] - 0.6 * inch
        )

        # Footer
        canvas.setFont("Helvetica", 8)
        canvas.drawString(
            inch, 0.5 * inch, "© 2025 V-Mart AI Agent - All Rights Reserved"
        )
        canvas.drawRightString(letter[0] - inch, 0.5 * inch, f"Page {doc.page}")

        # Footer line
        canvas.line(inch, 0.7 * inch, letter[0] - inch, 0.7 * inch)

        canvas.restoreState()

    def parse_markdown(self, md_content):
        """Parse markdown content and convert to PDF elements"""
        elements = []
        lines = md_content.split("\n")
        i = 0
        in_code_block = False
        code_block_lines = []
        in_table = False
        table_lines = []

        while i < len(lines):
            line = lines[i]

            # Code block handling
            if line.strip().startswith("```"):
                if in_code_block:
                    # End code block
                    code_text = "\n".join(code_block_lines)
                    elements.append(
                        Paragraph(
                            self._escape_html(code_text), self.styles["CustomCode"]
                        )
                    )
                    elements.append(Spacer(1, 0.1 * inch))
                    code_block_lines = []
                    in_code_block = False
                else:
                    # Start code block
                    in_code_block = True
                i += 1
                continue

            if in_code_block:
                code_block_lines.append(line)
                i += 1
                continue

            # Table handling
            if "|" in line and line.strip():
                if not in_table:
                    in_table = True
                    table_lines = []
                table_lines.append(line)
                i += 1
                continue
            elif in_table and not line.strip():
                # End table
                elements.extend(self._create_table(table_lines))
                elements.append(Spacer(1, 0.2 * inch))
                table_lines = []
                in_table = False
                i += 1
                continue

            # Headers
            if line.startswith("# ") and not line.startswith("## "):
                elements.append(
                    Paragraph(
                        self._format_text(line[2:].strip()), self.styles["CustomTitle"]
                    )
                )
                elements.append(Spacer(1, 0.2 * inch))
            elif line.startswith("## "):
                elements.append(Spacer(1, 0.1 * inch))
                elements.append(
                    Paragraph(
                        self._format_text(line[3:].strip()),
                        self.styles["SectionHeader"],
                    )
                )
            elif line.startswith("### "):
                elements.append(
                    Paragraph(
                        self._format_text(line[4:].strip()),
                        self.styles["SubsectionHeader"],
                    )
                )
            elif line.startswith("#### "):
                elements.append(
                    Paragraph(
                        self._format_text(line[5:].strip()), self.styles["Heading4"]
                    )
                )
            # Horizontal rule
            elif line.strip() == "---":
                elements.append(Spacer(1, 0.1 * inch))
                elements.append(
                    Table(
                        [[""]],
                        colWidths=[6.5 * inch],
                        style=[
                            (
                                "LINEABOVE",
                                (0, 0),
                                (-1, 0),
                                1,
                                colors.HexColor("#cccccc"),
                            )
                        ],
                    )
                )
                elements.append(Spacer(1, 0.1 * inch))
            # Bullet points
            elif line.strip().startswith("- ") or line.strip().startswith("* "):
                bullet_text = line.strip()[2:]
                elements.append(
                    Paragraph(
                        f"• {self._format_text(bullet_text)}",
                        self.styles["CustomBullet"],
                    )
                )
            # Numbered lists
            elif re.match(r"^\d+\.\s", line.strip()):
                elements.append(
                    Paragraph(
                        self._format_text(line.strip()), self.styles["CustomBullet"]
                    )
                )
            # Info boxes (lines starting with special markers)
            elif line.strip().startswith("**") and line.strip().endswith("**"):
                text = line.strip()[2:-2]
                if any(
                    marker in text.upper()
                    for marker in ["NOTE:", "WARNING:", "INFO:", "TIP:"]
                ):
                    elements.append(
                        Paragraph(self._format_text(text), self.styles["InfoBox"])
                    )
                else:
                    elements.append(
                        Paragraph(self._format_text(line), self.styles["Normal"])
                    )
            # Regular paragraphs
            elif line.strip():
                elements.append(
                    Paragraph(self._format_text(line), self.styles["Normal"])
                )
                elements.append(Spacer(1, 0.05 * inch))
            # Empty lines
            else:
                elements.append(Spacer(1, 0.1 * inch))

            i += 1

        # Handle unclosed table
        if in_table and table_lines:
            elements.extend(self._create_table(table_lines))

        return elements

    def _create_table(self, table_lines):
        """Create a table from markdown table lines"""
        # Filter out separator lines
        data_lines = [
            line for line in table_lines if not re.match(r"^\|[\s\-:|]+\|$", line)
        ]

        if not data_lines:
            return []

        # Parse table data
        table_data = []
        for line in data_lines:
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            table_data.append(cells)

        if not table_data:
            return []

        # Calculate column widths
        num_cols = len(table_data[0])
        if num_cols == 0:
            return []
        col_width = 6.5 * inch / num_cols

        # Create table
        table = Table(table_data, colWidths=[col_width] * num_cols)

        # Style the table
        style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5aa0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#f5f5f5")],
                ),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )

        table.setStyle(style)
        return [Spacer(1, 0.1 * inch), table]

    def _format_text(self, text):
        """Format text with bold, italic, code, etc."""
        # Escape HTML
        text = self._escape_html(text)

        # Handle inline code FIRST (before bold/italic to avoid nesting issues)
        # Replace backticks with a placeholder to avoid conflicts
        code_segments = []

        def replace_code(match):
            code_segments.append(match.group(1))
            return f"__CODE_{len(code_segments) - 1}__"

        text = re.sub(r"`([^`]+)`", replace_code, text)

        # Bold text (using ** or __)
        text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)

        # Italic text (using * only, avoid _ to prevent filename issues)
        text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)

        # Links (simplified) - extract link text only
        text = re.sub(
            r"\[([^\]]+)\]\([^)]+\)", r'<u><font color="blue">\1</font></u>', text
        )

        # Restore code segments
        for i, code in enumerate(code_segments):
            text = text.replace(
                f"__CODE_{i}__", f'<font name="Courier" color="#d63384">{code}</font>'
            )

        # Checkmarks and symbols
        text = text.replace("✅", "✓")
        text = text.replace("❌", "✗")
        text = text.replace("⏳", "⌛")
        text = text.replace("🔄", "↻")
        text = text.replace("→", "->")

        return text

    def _escape_html(self, text):
        """Escape HTML special characters"""
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        return text

    def generate_pdf(self, md_file, output_name, title, version):
        """Generate PDF from markdown file"""
        print(f"📄 Generating PDF: {output_name}")

        # Read markdown file
        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()

        # Parse markdown
        elements = self.parse_markdown(md_content)

        # Create PDF
        pdf_path = self.output_dir / output_name
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=1.2 * inch,
            bottomMargin=1 * inch,
            title=title,
            author="V-Mart AI Agent Team",
        )

        # Build PDF with header/footer
        doc.build(
            elements,
            onFirstPage=lambda c, d: self._add_header_footer(c, d, title, version),
            onLaterPages=lambda c, d: self._add_header_footer(c, d, title, version),
        )

        print(f"✅ Created: {pdf_path}")
        return pdf_path


def main():
    """Main function to generate all release PDFs"""
    print("=" * 60)
    print("V-Mart AI Agent - Release PDF Generator")
    print("=" * 60)
    print()

    generator = ReleasePDFGenerator(output_dir="releases/pdf")

    # Define release documents to convert
    documents = [
        # v2.0 Release Documents
        {
            "file": "releases/README.md",
            "output": "V-Mart_AI_Agent_v2.0_Release_Overview.pdf",
            "title": "V-Mart AI Agent v2.0 - Release Overview",
            "version": "v2.0.0",
        },
        {
            "file": "releases/RELEASE_SUMMARY_v2.0.md",
            "output": "V-Mart_AI_Agent_v2.0_Release_Summary.pdf",
            "title": "V-Mart AI Agent v2.0 - Comprehensive Release Summary",
            "version": "v2.0.0",
        },
        {
            "file": "releases/RELEASE_DOWNLOADS_v2.0.md",
            "output": "V-Mart_AI_Agent_v2.0_Release_Downloads.pdf",
            "title": "V-Mart AI Agent v2.0 - Release Downloads Guide",
            "version": "v2.0.0",
        },
        {
            "file": "releases/QA_TESTING_REPORT_v2.0.md",
            "output": "V-Mart_AI_Agent_v2.0_QA_Testing_Report.pdf",
            "title": "V-Mart AI Agent v2.0 - QA Testing Report",
            "version": "v2.0.0",
        },
        {
            "file": "releases/QA_COMPLETION_SUMMARY.md",
            "output": "V-Mart_AI_Agent_v2.0_QA_Completion_Summary.pdf",
            "title": "V-Mart AI Agent v2.0 - QA Completion Summary",
            "version": "v2.0.0",
        },
    ]

    # Check for v1 documentation
    v1_docs = []
    if os.path.exists("README.md"):
        v1_docs.append(
            {
                "file": "README.md",
                "output": "V-Mart_AI_Agent_v1.0_Documentation.pdf",
                "title": "V-Mart AI Agent v1.0 - Documentation",
                "version": "v1.0.0",
            }
        )

    if os.path.exists("docs/DEPLOYMENT.md"):
        v1_docs.append(
            {
                "file": "docs/DEPLOYMENT.md",
                "output": "V-Mart_AI_Agent_v1.0_Deployment_Guide.pdf",
                "title": "V-Mart AI Agent v1.0 - Deployment Guide",
                "version": "v1.0.0",
            }
        )

    all_documents = documents + v1_docs

    # Generate PDFs
    generated_pdfs = []
    for doc in all_documents:
        if os.path.exists(doc["file"]):
            try:
                pdf_path = generator.generate_pdf(
                    doc["file"], doc["output"], doc["title"], doc["version"]
                )
                generated_pdfs.append(pdf_path)
            except Exception as e:
                print(f"❌ Error generating {doc['output']}: {e}")
        else:
            print(f"⚠️  File not found: {doc['file']}")

    print()
    print("=" * 60)
    print(f"✅ PDF Generation Complete!")
    print(f"📊 Generated {len(generated_pdfs)} PDF documents")
    print("=" * 60)
    print()
    print("Generated PDFs:")
    for pdf in generated_pdfs:
        size_mb = os.path.getsize(pdf) / (1024 * 1024)
        print(f"  • {pdf.name} ({size_mb:.2f} MB)")
    print()
    print(f"📂 Output directory: releases/pdf/")
    print()


if __name__ == "__main__":
    main()
