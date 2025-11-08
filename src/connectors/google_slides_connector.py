"""
Connector for Google Slides
"""

from typing import Dict, List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSlidesConnector:
    def __init__(self, credentials: Credentials):
        """
        Initializes the Google Slides Connector.

        Args:
            credentials (Credentials): The OAuth 2.0 credentials.
        """
        self.service = build("slides", "v1", credentials=credentials)

    def read_presentation(self, presentation_id: str) -> Optional[str]:
        """
        Reads a Google Slides presentation and returns its text content.

        Args:
            presentation_id (str): The ID of the presentation.

        Returns:
            Presentation text or None if an error occurs.
        """
        try:
            presentation = (
                self.service.presentations()
                .get(presentationId=presentation_id)
                .execute()
            )

            slides = presentation.get("slides", [])
            text = ""

            for slide in slides:
                for element in slide.get("pageElements", []):
                    if "shape" in element:
                        shape = element["shape"]
                        if "text" in shape:
                            for text_element in shape["text"].get("textElements", []):
                                if "textRun" in text_element:
                                    text += text_element["textRun"].get("content", "")

            return text
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def create_presentation(self, title: str) -> Optional[Dict]:
        """
        Creates a new Google Slides presentation.

        Args:
            title (str): The title of the new presentation.

        Returns:
            Presentation metadata or None if an error occurs.
        """
        try:
            presentation = {"title": title}
            result = self.service.presentations().create(body=presentation).execute()
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def add_slide(self, presentation_id: str, layout: str = "BLANK") -> Optional[Dict]:
        """
        Adds a slide to a presentation.

        Args:
            presentation_id (str): The ID of the presentation.
            layout (str): The layout of the slide.

        Returns:
            Update response or None if an error occurs.
        """
        try:
            requests = [
                {"createSlide": {"slideLayoutReference": {"predefinedLayout": layout}}}
            ]
            result = (
                self.service.presentations()
                .batchUpdate(
                    presentationId=presentation_id, body={"requests": requests}
                )
                .execute()
            )
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
