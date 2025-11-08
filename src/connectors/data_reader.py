"""
Data Reader Connector
Unified interface for reading data from multiple sources:
- Excel files
- Google Sheets
- PowerPoint presentations
- Email (Gmail)
- Active screen detection
"""

import json
from datetime import datetime
from typing import Any, Dict, Optional

from .email_reader import EmailReader
from .excel_reader import ExcelReader
from .google_sheets_reader import GoogleSheetsReader
from .powerpoint_reader import PowerPointReader
from .screen_reader import ScreenReader


class DataReaderConnector:
    """Unified connector for reading data from various sources"""

    def __init__(self):
        self.screen_reader = ScreenReader()
        self.excel_reader = ExcelReader()
        self.sheets_reader = GoogleSheetsReader()
        self.ppt_reader = PowerPointReader()
        self.email_reader = EmailReader()

    def detect_active_application(self) -> Dict[str, Any]:
        """Detect which application is currently active"""
        window_info = self.screen_reader.get_active_window_info()

        return {
            "application": window_info.get("application", "Unknown"),
            "window_title": window_info.get("window_title", ""),
            "app_type": window_info.get("app_type", "unknown"),
            "timestamp": window_info.get("timestamp", datetime.now().isoformat()),
        }

    def read_active_screen_data(self, include_hidden: bool = True) -> Dict[str, Any]:
        """Read data from the currently active application"""
        app_info = self.detect_active_application()
        app_type = app_info.get("app_type")

        result = {
            "source": "active_screen",
            "application_info": app_info,
            "data": None,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
        }

        try:
            if app_type == "excel":
                result["data"] = self.read_excel_data(include_hidden=include_hidden)
                result["data_type"] = "excel"

            elif app_type == "google_sheets":
                result["data"] = self.read_google_sheets_data(
                    include_hidden=include_hidden
                )
                result["data_type"] = "google_sheets"

            elif app_type == "powerpoint":
                result["data"] = self.read_powerpoint_data()
                result["data_type"] = "powerpoint"

            elif app_type == "email":
                result["data"] = self.read_email_data(max_results=5)
                result["data_type"] = "email"

            else:
                result["status"] = "unsupported"
                result["message"] = (
                    f'Application type "{app_type}" is not supported for data reading'
                )

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)

        return result

    def read_excel_data(
        self, file_path: Optional[str] = None, include_hidden: bool = True
    ) -> Dict[str, Any]:
        """Read data from Excel file"""
        try:
            if file_path:
                self.excel_reader.file_path = file_path

            if not self.excel_reader.load_file():
                return {"error": "Failed to load Excel file"}

            return self.excel_reader.read_all_data(include_hidden=include_hidden)
        except Exception as e:
            return {"error": f"Error reading Excel data: {str(e)}"}

    def read_excel_active_sheet(
        self, file_path: Optional[str] = None, include_hidden: bool = True
    ) -> Dict[str, Any]:
        """Read data from active Excel sheet only"""
        try:
            if file_path:
                self.excel_reader.file_path = file_path

            if not self.excel_reader.load_file():
                return {"error": "Failed to load Excel file"}

            return self.excel_reader.get_active_sheet_data(
                include_hidden=include_hidden
            )
        except Exception as e:
            return {"error": f"Error reading Excel active sheet: {str(e)}"}

    def read_google_sheets_data(
        self, spreadsheet_id: Optional[str] = None, include_hidden: bool = True
    ) -> Dict[str, Any]:
        """Read data from Google Sheets"""
        try:
            return self.sheets_reader.read_all_data(
                spreadsheet_id=spreadsheet_id, include_hidden=include_hidden
            )
        except Exception as e:
            return {"error": f"Error reading Google Sheets data: {str(e)}"}

    def read_powerpoint_data(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Read data from PowerPoint presentation"""
        try:
            if file_path:
                self.ppt_reader.file_path = file_path

            if not self.ppt_reader.load_file():
                return {"error": "Failed to load PowerPoint file"}

            return self.ppt_reader.read_all_slides()
        except Exception as e:
            return {"error": f"Error reading PowerPoint data: {str(e)}"}

    def read_email_data(self, max_results: int = 10, query: str = "") -> Dict[str, Any]:
        """Read email data from Gmail"""
        try:
            emails = self.email_reader.get_recent_emails(
                max_results=max_results, query=query
            )
            labels = self.email_reader.get_labels()

            return {"emails": emails, "labels": labels, "count": len(emails)}
        except Exception as e:
            return {"error": f"Error reading email data: {str(e)}"}

    def get_data_summary(self, data: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the data"""
        if "error" in data:
            return f"Error: {data['error']}"

        summary_lines = []

        # Excel data summary
        if "metadata" in data and "filename" in data.get("metadata", {}):
            metadata = data["metadata"]
            summary_lines.append(f"📊 **Excel File: {metadata.get('filename')}**")
            summary_lines.append(f"- Sheets: {metadata.get('sheet_count', 0)}")
            summary_lines.append(f"- Author: {metadata.get('author', 'Unknown')}")

            if "sheets_data" in data:
                for sheet_name, sheet_data in data["sheets_data"].items():
                    summary_lines.append(f"\n**Sheet: {sheet_name}**")
                    dims = sheet_data.get("dimensions", {})
                    summary_lines.append(f"- Rows: {dims.get('max_row', 0)}")
                    summary_lines.append(f"- Columns: {dims.get('max_column', 0)}")

                    if sheet_data.get("filters", {}).get("has_auto_filter"):
                        summary_lines.append("- Has filters applied")

                    if sheet_data.get("pivot_tables"):
                        summary_lines.append(
                            f"- Pivot tables: {len(sheet_data['pivot_tables'])}"
                        )

        # Google Sheets summary
        elif "spreadsheet_id" in data.get("metadata", {}):
            metadata = data["metadata"]
            summary_lines.append(f"📑 **Google Sheet: {metadata.get('title')}**")
            summary_lines.append(f"- Sheets: {metadata.get('sheet_count', 0)}")

            if "sheets_data" in data:
                for sheet_name, sheet_data in data["sheets_data"].items():
                    if "error" not in sheet_data:
                        summary_lines.append(f"\n**Sheet: {sheet_name}**")
                        dims = sheet_data.get("dimensions", {})
                        summary_lines.append(f"- Rows: {dims.get('row_count', 0)}")
                        summary_lines.append(
                            f"- Columns: {dims.get('column_count', 0)}"
                        )

        # PowerPoint summary
        elif "slide_count" in data.get("metadata", {}):
            metadata = data["metadata"]
            summary_lines.append(f"📽️ **PowerPoint: {metadata.get('filename')}**")
            summary_lines.append(f"- Slides: {metadata.get('slide_count', 0)}")
            summary_lines.append(f"- Author: {metadata.get('author', 'Unknown')}")

            if "slides_data" in data:
                for slide in data["slides_data"][:5]:  # First 5 slides
                    summary_lines.append(f"\n**Slide {slide.get('slide_number')}**")
                    summary_lines.append(
                        f"- Layout: {slide.get('layout_name', 'Unknown')}"
                    )
                    summary_lines.append(
                        f"- Text elements: {len(slide.get('text_content', []))}"
                    )
                    summary_lines.append(f"- Tables: {len(slide.get('tables', []))}")
                    summary_lines.append(f"- Charts: {len(slide.get('charts', []))}")

        # Email summary
        elif "emails" in data:
            summary_lines.append(f"📧 **Emails: {data.get('count', 0)} messages**")

            for email_data in data["emails"][:5]:  # First 5 emails
                summary_lines.append(
                    f"\n**Subject: {email_data.get('subject', 'No subject')}**"
                )
                summary_lines.append(f"- From: {email_data.get('from', 'Unknown')}")
                summary_lines.append(f"- Date: {email_data.get('date', 'Unknown')}")
                summary_lines.append(
                    f"- Attachments: {len(email_data.get('attachments', []))}"
                )

        return "\n".join(summary_lines) if summary_lines else "No data available"

    def format_for_chatbot(self, data: Dict[str, Any]) -> str:
        """Format data in a chatbot-friendly way"""
        if "error" in data:
            return f"❌ {data['error']}"

        # Generate summary
        summary = self.get_data_summary(data)

        # Add data statistics
        stats = self._calculate_statistics(data)

        response = f"{summary}\n\n"

        if stats:
            response += "**📈 Data Statistics:**\n"
            for key, value in stats.items():
                response += f"- {key}: {value}\n"

        return response

    def _calculate_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate statistics from the data"""
        stats = {}

        # Excel/Sheets statistics
        if "sheets_data" in data:
            total_rows = 0
            total_columns = 0
            total_formulas = 0

            for sheet_data in data["sheets_data"].values():
                if "error" not in sheet_data:
                    dims = sheet_data.get("dimensions", {})
                    total_rows += dims.get("max_row", 0) or dims.get("row_count", 0)
                    total_columns += dims.get("max_column", 0) or dims.get(
                        "column_count", 0
                    )
                    total_formulas += len(sheet_data.get("formulas", []))

            stats["Total Rows"] = total_rows
            stats["Total Columns"] = total_columns
            if total_formulas > 0:
                stats["Formulas"] = total_formulas

        # PowerPoint statistics
        elif "slides_data" in data:
            total_text_elements = sum(
                len(slide.get("text_content", [])) for slide in data["slides_data"]
            )
            total_tables = sum(
                len(slide.get("tables", [])) for slide in data["slides_data"]
            )
            total_charts = sum(
                len(slide.get("charts", [])) for slide in data["slides_data"]
            )

            stats["Text Elements"] = total_text_elements
            if total_tables > 0:
                stats["Tables"] = total_tables
            if total_charts > 0:
                stats["Charts"] = total_charts

        # Email statistics
        elif "emails" in data:
            unread = sum(
                1 for email in data["emails"] if "UNREAD" in email.get("labels", [])
            )
            with_attachments = sum(
                1 for email in data["emails"] if email.get("attachments")
            )

            if unread > 0:
                stats["Unread"] = unread
            if with_attachments > 0:
                stats["With Attachments"] = with_attachments

        return stats

    def export_to_json(self, data: Dict[str, Any], filename: str) -> bool:
        """Export data to JSON file"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
