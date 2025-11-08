"""
Google Sheets Reader
Reads data from Google Sheets including:
- All sheets (visible and hidden)
- Filters and filter views
- Hidden columns and rows
- Cell data, formulas, and formatting
- Metadata and properties
"""

import os
import pickle
import platform
import re
import subprocess
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSheetsReader:
    """Read data from Google Sheets with comprehensive extraction"""

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = credentials_path or "credentials.json"
        self.creds = None
        self.service = None
        self.spreadsheet_id = None

    def authenticate(self) -> bool:
        """Authenticate with Google Sheets API"""
        token_path = "token_sheets.pickle"

        # Load existing credentials
        if os.path.exists(token_path):
            with open(token_path, "rb") as token:
                self.creds = pickle.load(token)

        # Refresh or get new credentials
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    print(f"Credentials file not found: {self.credentials_path}")
                    return False

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            # Save credentials
            with open(token_path, "wb") as token:
                pickle.dump(self.creds, token)

        try:
            self.service = build("sheets", "v4", credentials=self.creds)
            return True
        except Exception as e:
            print(f"Error building Sheets service: {e}")
            return False

    def get_active_google_sheet_id(self) -> Optional[str]:
        """Extract spreadsheet ID from active browser window"""
        system = platform.system()

        if system == "Darwin":  # macOS
            return self._get_active_sheet_id_macos()
        elif system == "Windows":
            return self._get_active_sheet_id_windows()

        return None

    def _get_active_sheet_id_macos(self) -> Optional[str]:
        """Get active Google Sheets ID from browser on macOS"""
        try:
            # Try Chrome first
            script = """
            tell application "Google Chrome"
                if (count of windows) > 0 then
                    set activeTab to active tab of front window
                    set tabURL to URL of activeTab
                    return tabURL
                end if
            end tell
            """

            result = subprocess.run(
                ["osascript", "-e", script], capture_output=True, text=True, timeout=5
            )

            if result.returncode == 0:
                url = result.stdout.strip()
                sheet_id = self._extract_sheet_id_from_url(url)
                if sheet_id:
                    return sheet_id

            # Try Safari
            script = """
            tell application "Safari"
                if (count of windows) > 0 then
                    set currentURL to URL of current tab of front window
                    return currentURL
                end if
            end tell
            """

            result = subprocess.run(
                ["osascript", "-e", script], capture_output=True, text=True, timeout=5
            )

            if result.returncode == 0:
                url = result.stdout.strip()
                return self._extract_sheet_id_from_url(url)

        except Exception as e:
            print(f"Error getting active Google Sheet ID: {e}")

        return None

    def _get_active_sheet_id_windows(self) -> Optional[str]:
        """Get active Google Sheets ID from browser on Windows"""
        # This would require Windows-specific implementation
        return None

    def _extract_sheet_id_from_url(self, url: str) -> Optional[str]:
        """Extract spreadsheet ID from Google Sheets URL"""
        # Pattern: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit...
        pattern = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
        match = re.search(pattern, url)

        if match:
            return match.group(1)

        return None

    def set_spreadsheet_id(self, spreadsheet_id: str):
        """Set the spreadsheet ID to read from"""
        self.spreadsheet_id = spreadsheet_id

    def get_spreadsheet_metadata(
        self, spreadsheet_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get spreadsheet metadata"""
        if spreadsheet_id:
            self.spreadsheet_id = spreadsheet_id

        if not self.spreadsheet_id:
            self.spreadsheet_id = self.get_active_google_sheet_id()

        if not self.spreadsheet_id:
            return {"error": "No spreadsheet ID provided or found"}

        if not self.service:
            if not self.authenticate():
                return {"error": "Authentication failed"}

        try:
            spreadsheet = (
                self.service.spreadsheets()
                .get(spreadsheetId=self.spreadsheet_id)
                .execute()
            )

            return {
                "spreadsheet_id": spreadsheet.get("spreadsheetId"),
                "title": spreadsheet.get("properties", {}).get("title"),
                "locale": spreadsheet.get("properties", {}).get("locale"),
                "time_zone": spreadsheet.get("properties", {}).get("timeZone"),
                "sheet_count": len(spreadsheet.get("sheets", [])),
                "sheets": [
                    sheet.get("properties", {}).get("title")
                    for sheet in spreadsheet.get("sheets", [])
                ],
            }
        except HttpError as e:
            return {"error": f"HTTP error: {e}"}
        except Exception as e:
            return {"error": f"Error: {e}"}

    def get_all_sheets_info(
        self, spreadsheet_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get information about all sheets"""
        if spreadsheet_id:
            self.spreadsheet_id = spreadsheet_id

        if not self.spreadsheet_id:
            self.spreadsheet_id = self.get_active_google_sheet_id()

        if not self.spreadsheet_id or not self.service:
            return []

        try:
            spreadsheet = (
                self.service.spreadsheets()
                .get(spreadsheetId=self.spreadsheet_id)
                .execute()
            )

            sheets_info = []

            for sheet in spreadsheet.get("sheets", []):
                props = sheet.get("properties", {})
                grid_props = props.get("gridProperties", {})

                sheets_info.append(
                    {
                        "sheet_id": props.get("sheetId"),
                        "title": props.get("title"),
                        "index": props.get("index"),
                        "hidden": props.get("hidden", False),
                        "tab_color": props.get("tabColor"),
                        "row_count": grid_props.get("rowCount"),
                        "column_count": grid_props.get("columnCount"),
                        "frozen_rows": grid_props.get("frozenRowCount", 0),
                        "frozen_columns": grid_props.get("frozenColumnCount", 0),
                        "has_filters": "basicFilter" in sheet or "filterViews" in sheet,
                    }
                )

            return sheets_info
        except Exception as e:
            print(f"Error getting sheets info: {e}")
            return []

    def read_sheet_data(
        self, sheet_name: str, include_hidden: bool = True
    ) -> Dict[str, Any]:
        """Read comprehensive data from a specific sheet"""
        if not self.service or not self.spreadsheet_id:
            return {"error": "Not initialized"}

        try:
            # Get sheet metadata
            spreadsheet = (
                self.service.spreadsheets()
                .get(
                    spreadsheetId=self.spreadsheet_id,
                    includeGridData=True,
                    ranges=[sheet_name],
                )
                .execute()
            )

            sheet_data = None
            for sheet in spreadsheet.get("sheets", []):
                if sheet.get("properties", {}).get("title") == sheet_name:
                    sheet_data = sheet
                    break

            if not sheet_data:
                return {"error": f"Sheet {sheet_name} not found"}

            props = sheet_data.get("properties", {})
            grid_props = props.get("gridProperties", {})

            # Get data
            data = sheet_data.get("data", [{}])[0]
            row_data = data.get("rowData", [])

            # Process rows and columns
            processed_data = self._process_sheet_data(row_data, include_hidden)

            # Get filters
            filters = self._get_sheet_filters(sheet_data)

            # Get hidden columns and rows
            hidden_info = self._get_hidden_info(data)

            return {
                "sheet_name": sheet_name,
                "sheet_id": props.get("sheetId"),
                "hidden": props.get("hidden", False),
                "dimensions": {
                    "row_count": grid_props.get("rowCount"),
                    "column_count": grid_props.get("columnCount"),
                    "frozen_rows": grid_props.get("frozenRowCount", 0),
                    "frozen_columns": grid_props.get("frozenColumnCount", 0),
                },
                "data": processed_data,
                "filters": filters,
                "hidden_columns": hidden_info["hidden_columns"],
                "hidden_rows": hidden_info["hidden_rows"],
            }
        except Exception as e:
            return {"error": f"Error reading sheet: {e}"}

    def _process_sheet_data(
        self, row_data: List, include_hidden: bool
    ) -> List[List[Dict[str, Any]]]:
        """Process row data into structured format"""
        processed = []

        for row in row_data[:100]:  # Limit to first 100 rows
            row_values = []

            for cell in row.get("values", []):
                effective_value = cell.get("effectiveValue", {})
                user_entered_value = cell.get("userEnteredValue", {})

                # Get cell value
                value = None
                if "stringValue" in effective_value:
                    value = effective_value["stringValue"]
                elif "numberValue" in effective_value:
                    value = effective_value["numberValue"]
                elif "boolValue" in effective_value:
                    value = effective_value["boolValue"]
                elif "formulaValue" in user_entered_value:
                    value = user_entered_value["formulaValue"]

                # Get formula if present
                formula = user_entered_value.get("formulaValue")

                row_values.append(
                    {
                        "value": value,
                        "formula": formula,
                        "formatted_value": cell.get("formattedValue"),
                        "note": cell.get("note"),
                    }
                )

            processed.append(row_values)

        return processed

    def _get_sheet_filters(self, sheet_data: Dict) -> Dict[str, Any]:
        """Extract filter information from sheet"""
        filters = {"basic_filter": None, "filter_views": []}

        # Basic filter
        if "basicFilter" in sheet_data:
            basic_filter = sheet_data["basicFilter"]
            filters["basic_filter"] = {
                "range": basic_filter.get("range"),
                "sort_specs": basic_filter.get("sortSpecs", []),
                "criteria": basic_filter.get("criteria", {}),
            }

        # Filter views
        if "filterViews" in sheet_data:
            for fv in sheet_data["filterViews"]:
                filters["filter_views"].append(
                    {
                        "title": fv.get("title"),
                        "range": fv.get("range"),
                        "criteria": fv.get("criteria", {}),
                    }
                )

        return filters

    def _get_hidden_info(self, data: Dict) -> Dict[str, Any]:
        """Get information about hidden rows and columns"""
        hidden_columns = []
        hidden_rows = []

        # Column metadata
        for idx, col_meta in enumerate(data.get("columnMetadata", [])):
            if col_meta.get("hiddenByUser", False):
                hidden_columns.append(idx)

        # Row metadata
        for idx, row_meta in enumerate(data.get("rowMetadata", [])):
            if row_meta.get("hiddenByUser", False):
                hidden_rows.append(idx)

        return {"hidden_columns": hidden_columns, "hidden_rows": hidden_rows}

    def read_all_data(
        self, spreadsheet_id: Optional[str] = None, include_hidden: bool = True
    ) -> Dict[str, Any]:
        """Read all data from all sheets"""
        if spreadsheet_id:
            self.spreadsheet_id = spreadsheet_id

        if not self.spreadsheet_id:
            self.spreadsheet_id = self.get_active_google_sheet_id()

        if not self.spreadsheet_id:
            return {"error": "No spreadsheet ID provided"}

        if not self.service:
            if not self.authenticate():
                return {"error": "Authentication failed"}

        metadata = self.get_spreadsheet_metadata()
        sheets_info = self.get_all_sheets_info()

        result = {
            "metadata": metadata,
            "sheets_summary": sheets_info,
            "sheets_data": {},
        }

        for sheet_info in sheets_info:
            sheet_name = sheet_info["title"]
            result["sheets_data"][sheet_name] = self.read_sheet_data(
                sheet_name, include_hidden
            )

        return result
