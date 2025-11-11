"""
Curated Response Formatter for V-Mart AI Agent
Formats AI responses with precise data, citations, and structured output

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional


class ResponseFormatter:
    """Formats AI responses with data-driven curation, citations, and structure"""

    def __init__(self):
        """Initialize response formatter"""
        self.citation_counter = 0

    def format_curated_response(
        self,
        ai_response: str,
        data_sources: Optional[List[Dict[str, Any]]] = None,
        analytics_data: Optional[Dict[str, Any]] = None,
        file_references: Optional[List[Dict[str, str]]] = None,
        include_citations: bool = True,
    ) -> Dict[str, Any]:
        """
        Create a curated, precise response with proper formatting and citations

        Args:
            ai_response: Raw AI response text
            data_sources: List of data sources used (store, weather, competition, etc.)
            analytics_data: Analytics results (sales, inventory, etc.)
            file_references: List of files analyzed with their content
            include_citations: Whether to add citation references

        Returns:
            Dict with formatted response, citations, data references, and metadata
        """
        # Parse and structure the response
        structured = self._structure_response(ai_response)

        # Add data citations if available
        citations = []
        if include_citations and data_sources:
            citations = self._generate_citations(
                data_sources, analytics_data, file_references
            )

        # Extract key insights
        insights = self._extract_key_insights(ai_response, analytics_data)

        # Extract recommendations
        recommendations = self._extract_recommendations(ai_response)

        # Extract data points mentioned
        data_points = self._extract_data_points(ai_response, analytics_data)

        return {
            "response": ai_response,
            "structured": structured,
            "insights": insights,
            "recommendations": recommendations,
            "data_points": data_points,
            "citations": citations,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "sources_count": len(data_sources) if data_sources else 0,
                "files_analyzed": len(file_references) if file_references else 0,
                "has_analytics": analytics_data is not None,
            },
        }

    def _structure_response(self, text: str) -> Dict[str, Any]:
        """Structure response into sections"""
        sections = {
            "summary": "",
            "analysis": "",
            "recommendations": [],
            "data_insights": [],
        }

        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        if paragraphs:
            sections["summary"] = paragraphs[0]

            # Look for analysis section
            for i, para in enumerate(paragraphs[1:]):
                if any(
                    keyword in para.lower()
                    for keyword in ["analysis", "based on", "looking at"]
                ):
                    sections["analysis"] = para
                    break

        return sections

    def _generate_citations(
        self,
        data_sources: List[Dict[str, Any]],
        analytics_data: Optional[Dict[str, Any]],
        file_references: Optional[List[Dict[str, str]]],
    ) -> List[Dict[str, str]]:
        """Generate citations for data sources"""
        citations = []

        # Store/weather/competition data
        if data_sources:
            for source in data_sources:
                if source.get("type") == "store":
                    citations.append(
                        {
                            "id": len(citations) + 1,
                            "type": "Store Data",
                            "source": f"V-Mart Store {source.get('store_id', 'N/A')}",
                            "location": source.get("location", "N/A"),
                            "timestamp": source.get(
                                "timestamp", datetime.now().isoformat()
                            ),
                        }
                    )
                elif source.get("type") == "weather":
                    citations.append(
                        {
                            "id": len(citations) + 1,
                            "type": "Weather Data",
                            "source": "OpenWeather API",
                            "location": source.get("location", "N/A"),
                            "timestamp": source.get(
                                "timestamp", datetime.now().isoformat()
                            ),
                        }
                    )
                elif source.get("type") == "competition":
                    citations.append(
                        {
                            "id": len(citations) + 1,
                            "type": "Competition Analysis",
                            "source": "V-Mart Store Database",
                            "competitors_count": source.get("count", 0),
                            "timestamp": source.get(
                                "timestamp", datetime.now().isoformat()
                            ),
                        }
                    )

        # Analytics data
        if analytics_data:
            citations.append(
                {
                    "id": len(citations) + 1,
                    "type": "Analytics Data",
                    "source": analytics_data.get("source", "V-Mart Analytics Engine"),
                    "period": analytics_data.get("period", "N/A"),
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # File references
        if file_references:
            for file_ref in file_references:
                citations.append(
                    {
                        "id": len(citations) + 1,
                        "type": "File Analysis",
                        "source": file_ref.get("name", "Unknown File"),
                        "format": file_ref.get("format", "N/A"),
                        "size": file_ref.get("size", "N/A"),
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        return citations

    def _extract_key_insights(
        self, text: str, analytics_data: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Extract key insights from response"""
        insights = []

        # Look for numbered lists
        numbered_pattern = r"^\d+[\.\)]\s*(.+)$"
        for line in text.split("\n"):
            match = re.match(numbered_pattern, line.strip())
            if match:
                insight = match.group(1).strip()
                if len(insight) > 20:  # Meaningful insights
                    insights.append(insight)

        # Look for bullet points
        bullet_pattern = r"^[•\-\*]\s*(.+)$"
        for line in text.split("\n"):
            match = re.match(bullet_pattern, line.strip())
            if match:
                insight = match.group(1).strip()
                if len(insight) > 20:
                    insights.append(insight)

        # Extract from analytics data if available
        if analytics_data:
            if "top_category" in analytics_data:
                insights.append(
                    f"Top performing category: {analytics_data['top_category']}"
                )
            if "growth_rate" in analytics_data:
                insights.append(f"Growth rate: {analytics_data['growth_rate']}")

        return insights[:5]  # Top 5 insights

    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract actionable recommendations"""
        recommendations = []

        # Keywords that indicate recommendations
        rec_keywords = [
            "recommend",
            "suggest",
            "should",
            "consider",
            "advise",
            "propose",
            "encourage",
            "action",
            "implement",
            "focus on",
        ]

        sentences = re.split(r"[.!?]", text)
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in rec_keywords):
                if len(sentence) > 30:  # Meaningful recommendations
                    recommendations.append(sentence + ".")

        return recommendations[:5]  # Top 5 recommendations

    def _extract_data_points(
        self, text: str, analytics_data: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract specific data points mentioned in response"""
        data_points = []

        # Extract INR amounts
        inr_pattern = r"₹\s*[\d,]+(?:\.\d{2})?"
        inr_matches = re.finditer(inr_pattern, text)
        for match in inr_matches:
            data_points.append(
                {
                    "type": "currency",
                    "value": match.group(0),
                    "context": self._get_context_around(
                        text, match.start(), match.end()
                    ),
                }
            )

        # Extract percentages
        percent_pattern = r"\d+(?:\.\d+)?%"
        percent_matches = re.finditer(percent_pattern, text)
        for match in percent_matches:
            data_points.append(
                {
                    "type": "percentage",
                    "value": match.group(0),
                    "context": self._get_context_around(
                        text, match.start(), match.end()
                    ),
                }
            )

        # Extract numbers with units
        number_pattern = r"\d+(?:\.\d+)?\s*(?:km|stores|items|units|pieces|kg|liters)"
        number_matches = re.finditer(number_pattern, text, re.IGNORECASE)
        for match in number_matches:
            data_points.append(
                {
                    "type": "quantity",
                    "value": match.group(0),
                    "context": self._get_context_around(
                        text, match.start(), match.end()
                    ),
                }
            )

        # Add analytics data points if available
        if analytics_data:
            if "total_sales" in analytics_data:
                data_points.append(
                    {
                        "type": "analytics",
                        "metric": "total_sales",
                        "value": analytics_data["total_sales"],
                    }
                )
            if "category_breakdown" in analytics_data:
                for cat, data in analytics_data.get("category_breakdown", {}).items():
                    data_points.append(
                        {
                            "type": "analytics",
                            "metric": f"{cat}_sales",
                            "value": data.get("sales", "N/A"),
                        }
                    )

        return data_points

    def _get_context_around(
        self, text: str, start: int, end: int, window: int = 50
    ) -> str:
        """Get context around a match"""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        context = text[context_start:context_end].strip()
        return context

    def format_multi_file_analysis(
        self, files: List[Dict[str, str]], cross_references: List[Dict[str, Any]]
    ) -> str:
        """Format multi-file analysis with cross-references"""
        sections = ["=== MULTI-FILE ANALYSIS ===\n", f"Files Analyzed: {len(files)}\n"]

        # List files
        for i, file in enumerate(files, 1):
            sections.append(
                f"{i}. {file.get('name', 'Unknown')} ({file.get('format', 'N/A')})"
            )

        sections.append("\n=== CROSS-REFERENCES FOUND ===\n")

        # Add cross-references
        if cross_references:
            for ref in cross_references:
                sections.append(
                    f"• {ref.get('type', 'Data')}: "
                    f"{ref.get('file1', 'File 1')} ↔ {ref.get('file2', 'File 2')}"
                )
                if ref.get("details"):
                    sections.append(f"  Details: {ref['details']}")
        else:
            sections.append("No cross-references detected between files.")

        sections.append("\n=== END MULTI-FILE ANALYSIS ===\n")

        return "\n".join(sections)

    def format_with_inr(self, text: str, inr_values: Dict[str, float]) -> str:
        """Format text with INR currency values"""
        formatted = text

        for key, value in inr_values.items():
            # Format as Indian currency
            formatted_value = self._format_inr_currency(value)
            # Replace placeholder with formatted value
            formatted = formatted.replace(f"{{{key}}}", formatted_value)

        return formatted

    def _format_inr_currency(self, amount: float) -> str:
        """Format number as Indian currency (₹)"""
        if amount >= 10000000:  # 1 Crore
            cr_value = amount / 10000000
            formatted = f"{cr_value:.2f}".rstrip("0").rstrip(".")
            return f"₹{formatted} Cr"
        elif amount >= 100000:  # 1 Lakh
            l_value = amount / 100000
            formatted = f"{l_value:.2f}".rstrip("0").rstrip(".")
            return f"₹{formatted} L"
        else:
            return f"₹{amount:,.2f}"

    def create_data_table(
        self, headers: List[str], rows: List[List[Any]], title: Optional[str] = None
    ) -> str:
        """Create formatted data table"""
        lines = []

        if title:
            lines.append(f"\n=== {title.upper()} ===\n")

        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        # Create header
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        lines.append(header_line)
        lines.append("-" * len(header_line))

        # Create rows
        for row in rows:
            row_line = " | ".join(
                str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)
            )
            lines.append(row_line)

        lines.append("")  # Empty line at end

        return "\n".join(lines)
