"""
Export Utility for V-Mart Personal AI Agent
Generates Excel and PDF exports with formatted data, insights, and recommendations

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import io
import re
from datetime import datetime
from typing import Any, Dict, List

try:
    import xlsxwriter
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    EXPORT_AVAILABLE = True
except ImportError:
    EXPORT_AVAILABLE = False


class ExportGenerator:
    """Generates Excel and PDF exports with AI insights and recommendations"""

    def __init__(self):
        if not EXPORT_AVAILABLE:
            raise ImportError(
                "Export libraries not available. Install reportlab and xlsxwriter."
            )

    def generate_excel(self, data: Dict[str, Any]) -> io.BytesIO:
        """
        Generate Excel file with formatted data, insights, and recommendations

        Args:
            data: Dictionary containing:
                - title: Report title
                - analysis: AI-generated analysis text
                - insights: List of insights or text
                - recommendations: List of recommendations or text
                - data_table: Optional list of dictionaries for tabular data
                - metadata: Optional metadata (user, date, etc.)

        Returns:
            BytesIO: Excel file in memory
        """
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})

        # Define formats
        title_format = workbook.add_format(
            {
                "bold": True,
                "font_size": 16,
                "font_color": "#667eea",
                "align": "left",
                "valign": "vcenter",
            }
        )

        header_format = workbook.add_format(
            {
                "bold": True,
                "font_size": 12,
                "bg_color": "#667eea",
                "font_color": "white",
                "align": "left",
                "valign": "vcenter",
                "border": 1,
            }
        )

        subheader_format = workbook.add_format(
            {
                "bold": True,
                "font_size": 11,
                "font_color": "#667eea",
                "align": "left",
                "valign": "vcenter",
            }
        )

        text_format = workbook.add_format(
            {"font_size": 10, "align": "left", "valign": "top", "text_wrap": True}
        )

        insight_format = workbook.add_format(
            {
                "font_size": 10,
                "align": "left",
                "valign": "top",
                "text_wrap": True,
                "bg_color": "#f0f4ff",
            }
        )

        recommendation_format = workbook.add_format(
            {
                "font_size": 10,
                "align": "left",
                "valign": "top",
                "text_wrap": True,
                "bg_color": "#fff4e6",
            }
        )

        table_header_format = workbook.add_format(
            {
                "bold": True,
                "bg_color": "#667eea",
                "font_color": "white",
                "border": 1,
                "align": "center",
            }
        )

        table_cell_format = workbook.add_format(
            {"border": 1, "align": "left", "valign": "vcenter"}
        )

        # Create Summary worksheet
        worksheet = workbook.add_worksheet("Analysis Summary")
        worksheet.set_column("A:A", 20)
        worksheet.set_column("B:B", 80)

        row = 0

        # Title
        worksheet.merge_range(
            row, 0, row, 1, data.get("title", "AI Analysis Report"), title_format
        )
        row += 2

        # Metadata
        if "metadata" in data:
            metadata = data["metadata"]
            worksheet.write(row, 0, "Generated:", subheader_format)
            worksheet.write(
                row,
                1,
                metadata.get("date", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                text_format,
            )
            row += 1

            if "user" in metadata:
                worksheet.write(row, 0, "User:", subheader_format)
                worksheet.write(row, 1, metadata["user"], text_format)
                row += 1

            if "source" in metadata:
                worksheet.write(row, 0, "Source:", subheader_format)
                worksheet.write(row, 1, metadata["source"], text_format)
                row += 1

            row += 1

        # Analysis Section
        if "analysis" in data and data["analysis"]:
            worksheet.write(row, 0, "Analysis:", header_format)
            row += 1

            analysis_text = self._clean_html(data["analysis"])
            worksheet.write(row, 1, analysis_text, text_format)
            worksheet.set_row(row, None)  # Auto height
            row += 2

        # Insights Section
        if "insights" in data and data["insights"]:
            worksheet.write(row, 0, "Key Insights:", header_format)
            row += 1

            insights = data["insights"]
            if isinstance(insights, str):
                insights = self._extract_list_items(insights)

            for i, insight in enumerate(insights, 1):
                worksheet.write(row, 0, f"Insight {i}:", subheader_format)
                worksheet.write(row, 1, self._clean_html(insight), insight_format)
                row += 1

            row += 1

        # Recommendations Section
        if "recommendations" in data and data["recommendations"]:
            worksheet.write(row, 0, "Recommendations:", header_format)
            row += 1

            recommendations = data["recommendations"]
            if isinstance(recommendations, str):
                recommendations = self._extract_list_items(recommendations)

            for i, rec in enumerate(recommendations, 1):
                worksheet.write(row, 0, f"Action {i}:", subheader_format)
                worksheet.write(row, 1, self._clean_html(rec), recommendation_format)
                row += 1

            row += 1

        # Data Table Section
        if "data_table" in data and data["data_table"]:
            data_table = data["data_table"]

            if isinstance(data_table, list) and len(data_table) > 0:
                # Create Data worksheet
                data_worksheet = workbook.add_worksheet("Data")

                # Get headers
                headers = list(data_table[0].keys())

                # Write headers
                for col, header in enumerate(headers):
                    data_worksheet.write(0, col, header, table_header_format)

                # Write data
                for row_idx, row_data in enumerate(data_table, 1):
                    for col_idx, header in enumerate(headers):
                        value = row_data.get(header, "")
                        data_worksheet.write(row_idx, col_idx, value, table_cell_format)

                # Auto-fit columns
                for col_idx in range(len(headers)):
                    data_worksheet.set_column(col_idx, col_idx, 15)

        workbook.close()
        output.seek(0)
        return output

    def generate_pdf(self, data: Dict[str, Any]) -> io.BytesIO:
        """
        Generate PDF file with formatted data, insights, and recommendations

        Args:
            data: Dictionary containing:
                - title: Report title
                - analysis: AI-generated analysis text
                - insights: List of insights or text
                - recommendations: List of recommendations or text
                - data_table: Optional list of dictionaries for tabular data
                - metadata: Optional metadata

        Returns:
            BytesIO: PDF file in memory
        """
        output = io.BytesIO()
        doc = SimpleDocTemplate(
            output,
            pagesize=letter,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            rightMargin=0.75 * inch,
        )

        # Container for PDF elements
        story = []

        # Define styles
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=18,
            textColor=colors.HexColor("#667eea"),
            spaceAfter=20,
            alignment=TA_LEFT,
        )

        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#667eea"),
            spaceAfter=12,
            spaceBefore=12,
            alignment=TA_LEFT,
        )

        body_style = ParagraphStyle(
            "CustomBody",
            parent=styles["BodyText"],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
        )

        insight_style = ParagraphStyle(
            "InsightStyle",
            parent=styles["BodyText"],
            fontSize=10,
            leftIndent=20,
            backColor=colors.HexColor("#f0f4ff"),
            borderPadding=8,
            spaceAfter=8,
        )

        recommendation_style = ParagraphStyle(
            "RecommendationStyle",
            parent=styles["BodyText"],
            fontSize=10,
            leftIndent=20,
            backColor=colors.HexColor("#fff4e6"),
            borderPadding=8,
            spaceAfter=8,
        )

        # Title
        title = Paragraph(data.get("title", "AI Analysis Report"), title_style)
        story.append(title)
        story.append(Spacer(1, 0.2 * inch))

        # Metadata
        if "metadata" in data:
            metadata = data["metadata"]
            meta_text = f"<b>Generated:</b> {metadata.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}"

            if "user" in metadata:
                meta_text += f"<br/><b>User:</b> {metadata['user']}"

            if "source" in metadata:
                meta_text += f"<br/><b>Source:</b> {metadata['source']}"

            story.append(Paragraph(meta_text, body_style))
            story.append(Spacer(1, 0.2 * inch))

        # Analysis Section
        if "analysis" in data and data["analysis"]:
            story.append(Paragraph("Analysis", heading_style))
            analysis_text = self._clean_html_for_pdf(data["analysis"])
            story.append(Paragraph(analysis_text, body_style))
            story.append(Spacer(1, 0.15 * inch))

        # Insights Section
        if "insights" in data and data["insights"]:
            story.append(Paragraph("Key Insights", heading_style))

            insights = data["insights"]
            if isinstance(insights, str):
                insights = self._extract_list_items(insights)

            for i, insight in enumerate(insights, 1):
                insight_text = f"<b>{i}.</b> {self._clean_html_for_pdf(insight)}"
                story.append(Paragraph(insight_text, insight_style))

            story.append(Spacer(1, 0.15 * inch))

        # Recommendations Section
        if "recommendations" in data and data["recommendations"]:
            story.append(Paragraph("Recommendations", heading_style))

            recommendations = data["recommendations"]
            if isinstance(recommendations, str):
                recommendations = self._extract_list_items(recommendations)

            for i, rec in enumerate(recommendations, 1):
                rec_text = f"<b>Action {i}:</b> {self._clean_html_for_pdf(rec)}"
                story.append(Paragraph(rec_text, recommendation_style))

            story.append(Spacer(1, 0.15 * inch))

        # Data Table Section
        if "data_table" in data and data["data_table"]:
            data_table = data["data_table"]

            if isinstance(data_table, list) and len(data_table) > 0:
                story.append(PageBreak())
                story.append(Paragraph("Data", heading_style))

                # Prepare table data
                headers = list(data_table[0].keys())
                table_data = [headers]

                for row in data_table[:50]:  # Limit to 50 rows for PDF
                    table_data.append([str(row.get(h, "")) for h in headers])

                # Create table
                t = Table(table_data)
                t.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#667eea")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, 0), 10),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                            ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ]
                    )
                )

                story.append(t)

        # Build PDF
        doc.build(story)
        output.seek(0)
        return output

    def _clean_html(self, text: str) -> str:
        """Remove HTML tags for Excel export"""
        if not text:
            return ""

        # Remove HTML tags
        text = re.sub(r"<[^>]+>", "", text)

        # Decode HTML entities
        text = text.replace("&nbsp;", " ")
        text = text.replace("&amp;", "&")
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        text = text.replace("&quot;", '"')

        # Clean up whitespace
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        return text

    def _clean_html_for_pdf(self, text: str) -> str:
        """Clean HTML but keep basic formatting for PDF"""
        if not text:
            return ""

        # Convert common HTML tags to ReportLab equivalents
        text = text.replace("<strong>", "<b>")
        text = text.replace("</strong>", "</b>")
        text = text.replace("<em>", "<i>")
        text = text.replace("</em>", "</i>")

        # Remove complex HTML tags
        text = re.sub(r"<h[1-6][^>]*>", "<b>", text)
        text = re.sub(r"</h[1-6]>", "</b><br/>", text)
        text = re.sub(r"<p[^>]*>", "", text)
        text = re.sub(r"</p>", "<br/>", text)
        text = re.sub(r"<div[^>]*>", "", text)
        text = re.sub(r"</div>", "<br/>", text)
        text = re.sub(
            r"<table[^>]*>.*?</table>", "[Table omitted]", text, flags=re.DOTALL
        )

        # Decode HTML entities
        text = text.replace("&nbsp;", " ")
        text = text.replace("&amp;", "&amp;")
        text = text.replace("&lt;", "&lt;")
        text = text.replace("&gt;", "&gt;")

        # Clean up excessive line breaks
        text = re.sub(r"(<br/>){3,}", "<br/><br/>", text)

        return text.strip()

    def _extract_list_items(self, text: str) -> List[str]:
        """Extract list items from text (numbered or bulleted)"""
        if not text:
            return []

        # Clean HTML first
        text = self._clean_html(text)

        # Split by numbered list (1. 2. 3.)
        items = re.split(r"\d+\.\s+", text)
        items = [item.strip() for item in items if item.strip()]

        # If no numbered list, split by bullet points or line breaks
        if len(items) <= 1:
            items = re.split(r"[•\-\*]\s+|\n", text)
            items = [item.strip() for item in items if item.strip() and len(item) > 10]

        return items if items else [text]
