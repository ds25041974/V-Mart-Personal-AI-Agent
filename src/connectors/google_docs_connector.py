"""
Connector for Google Docs
"""

from typing import Dict, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDocsConnector:
    def __init__(self, credentials: Credentials):
        """
        Initializes the Google Docs Connector.

        Args:
            credentials (Credentials): The OAuth 2.0 credentials.
        """
        self.service = build("docs", "v1", credentials=credentials)

    def read_document(self, document_id: str) -> Optional[str]:
        """
        Reads a Google Doc and returns its text content.

        Args:
            document_id (str): The ID of the document.

        Returns:
            Document text or None if an error occurs.
        """
        try:
            document = self.service.documents().get(documentId=document_id).execute()
            content = document.get("body", {}).get("content", [])

            text = ""
            for element in content:
                if "paragraph" in element:
                    for text_run in element["paragraph"].get("elements", []):
                        if "textRun" in text_run:
                            text += text_run["textRun"].get("content", "")

            return text
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def create_document(self, title: str) -> Optional[Dict]:
        """
        Creates a new Google Doc.

        Args:
            title (str): The title of the new document.

        Returns:
            Document metadata or None if an error occurs.
        """
        try:
            document = {"title": title}
            result = self.service.documents().create(body=document).execute()
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def insert_text(
        self, document_id: str, text: str, index: int = 1
    ) -> Optional[Dict]:
        """
        Inserts text into a Google Doc.

        Args:
            document_id (str): The ID of the document.
            text (str): The text to insert.
            index (int): The position to insert the text.

        Returns:
            Update response or None if an error occurs.
        """
        try:
            requests = [{"insertText": {"location": {"index": index}, "text": text}}]
            result = (
                self.service.documents()
                .batchUpdate(documentId=document_id, body={"requests": requests})
                .execute()
            )
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
