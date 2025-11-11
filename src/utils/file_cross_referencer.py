"""
File Cross-Referencer for V-Mart AI Agent
Analyzes multiple files to find correlations, data matches, and cross-references

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd


class FileCrossReferencer:
    """Analyzes multiple files to find correlations and data matches"""

    def __init__(self):
        """Initialize cross-referencer"""
        self.common_data_patterns = {
            "store_id": r"VM[_\-]?[A-Z]{2}[_\-]?\d{3,4}",
            "product_id": r"(?:PRD|PROD)[_\-]?\d{4,6}",
            "employee_id": r"(?:EMP|E)[_\-]?\d{4,6}",
            "order_id": r"(?:ORD|ORDER)[_\-]?\d{6,8}",
            "invoice": r"(?:INV|INVOICE)[_\-]?\d{6,8}",
            "date": r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
            "amount": r"₹\s*[\d,]+(?:\.\d{2})?",
            "percentage": r"\d+(?:\.\d+)?%",
            "phone": r"\+?91[- ]?\d{10}",
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        }

    def analyze_multiple_files(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze multiple files for cross-references and correlations

        Args:
            files: List of dicts with 'name', 'content', 'format' keys

        Returns:
            Dict with cross-references, correlations, and insights
        """
        if len(files) < 2:
            return {
                "success": False,
                "message": "Need at least 2 files for cross-reference analysis",
                "cross_references": [],
            }

        # Extract data patterns from all files
        file_patterns = {}
        for file in files:
            file_name = file.get("name", "Unknown")
            content = file.get("content", "")

            file_patterns[file_name] = self._extract_patterns(content)

        # Find cross-references between files
        cross_refs = self._find_cross_references(file_patterns, files)

        # Find data correlations
        correlations = self._find_correlations(files)

        # Generate insights
        insights = self._generate_cross_file_insights(cross_refs, correlations)

        return {
            "success": True,
            "files_analyzed": len(files),
            "cross_references": cross_refs,
            "correlations": correlations,
            "insights": insights,
            "timestamp": datetime.now().isoformat(),
        }

    def _extract_patterns(self, content: str) -> Dict[str, List[str]]:
        """Extract common data patterns from file content"""
        patterns = {}

        for pattern_name, pattern_regex in self.common_data_patterns.items():
            matches = re.findall(pattern_regex, content, re.IGNORECASE)
            if matches:
                # Deduplicate and clean matches
                unique_matches = list(set([m.strip() for m in matches]))
                patterns[pattern_name] = unique_matches[:50]  # Limit to 50 per pattern

        return patterns

    def _find_cross_references(
        self,
        file_patterns: Dict[str, Dict[str, List[str]]],
        files: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Find cross-references between files based on common data"""
        cross_refs = []

        file_names = list(file_patterns.keys())

        # Compare each pair of files
        for i in range(len(file_names)):
            for j in range(i + 1, len(file_names)):
                file1 = file_names[i]
                file2 = file_names[j]

                patterns1 = file_patterns[file1]
                patterns2 = file_patterns[file2]

                # Find common data patterns
                for pattern_name in patterns1:
                    if pattern_name in patterns2:
                        # Find overlapping values
                        values1 = set(patterns1[pattern_name])
                        values2 = set(patterns2[pattern_name])
                        common_values = values1.intersection(values2)

                        if common_values:
                            cross_refs.append(
                                {
                                    "type": pattern_name,
                                    "file1": file1,
                                    "file2": file2,
                                    "common_values": list(common_values)[
                                        :10
                                    ],  # Limit to 10
                                    "count": len(common_values),
                                    "details": f"Found {len(common_values)} common {pattern_name} values",
                                }
                            )

        return cross_refs

    def _find_correlations(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find data correlations between files"""
        correlations = []

        # Try to detect CSV/Excel data for correlation analysis
        structured_files = []

        for file in files:
            content = file.get("content", "")
            file_format = file.get("format", "")

            # Check if it looks like tabular data
            if (
                "," in content
                or "\t" in content
                or file_format in ["csv", "excel", "xlsx"]
            ):
                # Try to parse as CSV
                try:
                    # Simple CSV parsing
                    lines = content.split("\n")
                    if len(lines) > 1:
                        # Check if first line has column headers
                        first_line = lines[0]
                        if "," in first_line or "\t" in first_line:
                            structured_files.append(
                                {
                                    "name": file.get("name"),
                                    "content": content,
                                    "format": file_format,
                                }
                            )
                except Exception:
                    pass

        # Analyze structured files for correlations
        if len(structured_files) >= 2:
            correlations.append(
                {
                    "type": "structured_data",
                    "files": [f["name"] for f in structured_files],
                    "details": f"Detected {len(structured_files)} files with structured tabular data",
                    "suggestion": "These files may contain related data that can be joined or compared",
                }
            )

        return correlations

    def _generate_cross_file_insights(
        self, cross_refs: List[Dict[str, Any]], correlations: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate insights from cross-file analysis"""
        insights = []

        if cross_refs:
            # Count total cross-references
            total_refs = len(cross_refs)
            insights.append(f"Found {total_refs} cross-reference(s) between files")

            # Identify most connected files
            file_connections = {}
            for ref in cross_refs:
                file1 = ref["file1"]
                file2 = ref["file2"]
                file_connections[file1] = file_connections.get(file1, 0) + 1
                file_connections[file2] = file_connections.get(file2, 0) + 1

            if file_connections:
                most_connected = max(file_connections.items(), key=lambda x: x[1])
                insights.append(
                    f"Most connected file: {most_connected[0]} "
                    f"({most_connected[1]} cross-references)"
                )

            # Identify most common data type
            data_types = {}
            for ref in cross_refs:
                data_type = ref["type"]
                data_types[data_type] = data_types.get(data_type, 0) + 1

            if data_types:
                most_common = max(data_types.items(), key=lambda x: x[1])
                insights.append(
                    f"Most common cross-reference type: {most_common[0]} "
                    f"({most_common[1]} occurrences)"
                )
        else:
            insights.append("No direct cross-references found between files")

        if correlations:
            insights.append(
                f"Detected {len(correlations)} potential correlation(s) for deeper analysis"
            )

        return insights

    def format_cross_reference_report(self, analysis_result: Dict[str, Any]) -> str:
        """Format cross-reference analysis as readable text"""
        lines = [
            "=== MULTI-FILE CROSS-REFERENCE ANALYSIS ===\n",
            f"Files Analyzed: {analysis_result.get('files_analyzed', 0)}",
            f"Analysis Time: {analysis_result.get('timestamp', 'N/A')}\n",
        ]

        # Add insights
        insights = analysis_result.get("insights", [])
        if insights:
            lines.append("\n🔍 KEY INSIGHTS:")
            for insight in insights:
                lines.append(f"  • {insight}")

        # Add cross-references
        cross_refs = analysis_result.get("cross_references", [])
        if cross_refs:
            lines.append(f"\n🔗 CROSS-REFERENCES FOUND: {len(cross_refs)}\n")

            for i, ref in enumerate(cross_refs, 1):
                lines.append(f"{i}. {ref.get('type', 'Unknown').upper()} Match:")
                lines.append(f"   Files: {ref.get('file1')} ↔ {ref.get('file2')}")
                lines.append(f"   Common values: {ref.get('count', 0)}")

                # Show sample values
                common_values = ref.get("common_values", [])
                if common_values:
                    sample = common_values[:3]  # Show up to 3 samples
                    lines.append(f"   Examples: {', '.join(sample)}")
                    if len(common_values) > 3:
                        lines.append(f"   ... and {len(common_values) - 3} more")
                lines.append("")
        else:
            lines.append("\n🔗 CROSS-REFERENCES: None found")

        # Add correlations
        correlations = analysis_result.get("correlations", [])
        if correlations:
            lines.append(f"\n📊 POTENTIAL CORRELATIONS: {len(correlations)}\n")
            for corr in correlations:
                lines.append(f"  • {corr.get('details', 'N/A')}")
                if corr.get("suggestion"):
                    lines.append(f"    💡 {corr.get('suggestion')}")

        lines.append("\n=== END CROSS-REFERENCE ANALYSIS ===\n")

        return "\n".join(lines)

    def find_data_in_files(
        self, search_value: str, files: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Search for specific data across multiple files

        Args:
            search_value: Value to search for (ID, name, etc.)
            files: List of files to search

        Returns:
            List of matches with file name and context
        """
        matches = []

        for file in files:
            content = file.get("content", "")
            file_name = file.get("name", "Unknown")

            # Search for exact match (case-insensitive)
            if search_value.lower() in content.lower():
                # Find context around match
                context = self._get_context_around_match(content, search_value)

                matches.append(
                    {
                        "file": file_name,
                        "found": True,
                        "context": context,
                        "occurrences": content.lower().count(search_value.lower()),
                    }
                )

        return matches

    def _get_context_around_match(
        self, text: str, search_value: str, context_chars: int = 150
    ) -> str:
        """Get context around first match"""
        try:
            index = text.lower().find(search_value.lower())
            if index == -1:
                return ""

            start = max(0, index - context_chars)
            end = min(len(text), index + len(search_value) + context_chars)

            context = text[start:end].strip()

            # Add ellipsis if truncated
            if start > 0:
                context = "..." + context
            if end < len(text):
                context = context + "..."

            return context
        except Exception:
            return ""
