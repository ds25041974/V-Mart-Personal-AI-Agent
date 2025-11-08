"""
Connector for Google Drive
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDriveConnector:
    def __init__(self, credentials: Credentials):
        """
        Initializes the Google Drive Connector.

        Args:
            credentials (Credentials): The OAuth 2.0 credentials.
        """
        self.service = build("drive", "v3", credentials=credentials)

    def list_files(self, page_size=10):
        """
        Lists files in Google Drive.
        """
        try:
            results = (
                self.service.files()
                .list(pageSize=page_size, fields="nextPageToken, files(id, name)")
                .execute()
            )
            items = results.get("files", [])
            return items
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def search_file(self, query: str, page_size=10):
        """
        Searches for a file on Google Drive.
        """
        try:
            results = (
                self.service.files()
                .list(
                    q=query, pageSize=page_size, fields="nextPageToken, files(id, name)"
                )
                .execute()
            )
            items = results.get("files", [])
            return items
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def read_file(self, file_id: str, mime_type: str) -> str:
        """
        Reads a file from Google Drive.

        Args:
            file_id (str): The ID of the file to read.
            mime_type (str): The MIME type of the file.

        Returns:
            str: The content of the file.
        """
        try:
            if "google-apps.document" in mime_type:
                request = self.service.files().export_media(
                    fileId=file_id, mimeType="text/plain"
                )
            elif "google-apps.spreadsheet" in mime_type:
                request = self.service.files().export_media(
                    fileId=file_id, mimeType="text/csv"
                )
            elif "google-apps.presentation" in mime_type:
                request = self.service.files().export_media(
                    fileId=file_id, mimeType="text/plain"
                )
            else:
                request = self.service.files().get_media(fileId=file_id)

            data = request.execute()
            return data.decode("utf-8")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
