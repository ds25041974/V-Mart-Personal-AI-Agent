"""
Connector for Google Sheets
"""

from typing import List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSheetsConnector:
    def __init__(self, credentials: Credentials):
        """
        Initializes the Google Sheets Connector.

        Args:
            credentials (Credentials): The OAuth 2.0 credentials.
        """
        self.service = build("sheets", "v4", credentials=credentials)

    def read_sheet(self, spreadsheet_id: str, range_name: str) -> Optional[List[List]]:
        """
        Reads data from a Google Sheet.

        Args:
            spreadsheet_id (str): The ID of the spreadsheet.
            range_name (str): The A1 notation of the range to read.

        Returns:
            List of rows or None if an error occurs.
        """
        try:
            result = (
                self.service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=range_name)
                .execute()
            )
            values = result.get("values", [])
            return values
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def write_sheet(
        self, spreadsheet_id: str, range_name: str, values: List[List]
    ) -> Optional[Dict]:
        """
        Writes data to a Google Sheet.

        Args:
            spreadsheet_id (str): The ID of the spreadsheet.
            range_name (str): The A1 notation of the range to write.
            values (List[List]): The data to write.

        Returns:
            Update response or None if an error occurs.
        """
        try:
            body = {"values": values}
            result = (
                self.service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption="RAW",
                    body=body,
                )
                .execute()
            )
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def append_sheet(
        self, spreadsheet_id: str, range_name: str, values: List[List]
    ) -> Optional[Dict]:
        """
        Appends data to a Google Sheet.

        Args:
            spreadsheet_id (str): The ID of the spreadsheet.
            range_name (str): The A1 notation of the range to append.
            values (List[List]): The data to append.

        Returns:
            Append response or None if an error occurs.
        """
        try:
            body = {"values": values}
            result = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption="RAW",
                    body=body,
                )
                .execute()
            )
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def create_spreadsheet(self, title: str) -> Optional[Dict]:
        """
        Creates a new Google Sheet.

        Args:
            title (str): The title of the new spreadsheet.

        Returns:
            Spreadsheet metadata or None if an error occurs.
        """
        try:
            spreadsheet = {"properties": {"title": title}}
            result = (
                self.service.spreadsheets()
                .create(body=spreadsheet, fields="spreadsheetId")
                .execute()
            )
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
