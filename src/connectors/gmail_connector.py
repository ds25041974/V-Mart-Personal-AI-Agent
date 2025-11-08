"""
Connector for Gmail - Read and Send Emails
"""

import base64
from email.mime.text import MIMEText
from typing import Dict, List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GmailConnector:
    def __init__(self, credentials: Credentials):
        """
        Initializes the Gmail Connector.

        Args:
            credentials (Credentials): The OAuth 2.0 credentials.
        """
        self.service = build("gmail", "v1", credentials=credentials)

    def list_messages(
        self, query: str = "", max_results: int = 10
    ) -> Optional[List[Dict]]:
        """
        Lists messages in the user's mailbox.

        Args:
            query (str): Query string to filter messages.
            max_results (int): Maximum number of messages to return.

        Returns:
            List of messages or None if an error occurs.
        """
        try:
            results = (
                self.service.users()
                .messages()
                .list(userId="me", q=query, maxResults=max_results)
                .execute()
            )
            messages = results.get("messages", [])
            return messages
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def read_message(self, message_id: str) -> Optional[Dict]:
        """
        Reads a specific message.

        Args:
            message_id (str): The ID of the message to read.

        Returns:
            Message content or None if an error occurs.
        """
        try:
            message = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="full")
                .execute()
            )

            payload = message.get("payload", {})
            headers = payload.get("headers", [])

            # Extract subject and sender
            subject = next(
                (h["value"] for h in headers if h["name"] == "Subject"), "No Subject"
            )
            sender = next(
                (h["value"] for h in headers if h["name"] == "From"), "Unknown"
            )

            # Extract body
            body = ""
            if "parts" in payload:
                for part in payload["parts"]:
                    if part["mimeType"] == "text/plain":
                        body = base64.urlsafe_b64decode(part["body"]["data"]).decode(
                            "utf-8"
                        )
                        break
            else:
                body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")

            return {
                "subject": subject,
                "sender": sender,
                "body": body,
                "snippet": message.get("snippet", ""),
            }
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def send_message(self, to: str, subject: str, body: str) -> Optional[Dict]:
        """
        Sends an email message.

        Args:
            to (str): Recipient email address.
            subject (str): Email subject.
            body (str): Email body.

        Returns:
            Sent message or None if an error occurs.
        """
        try:
            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = {"raw": raw_message}

            result = (
                self.service.users()
                .messages()
                .send(userId="me", body=send_message)
                .execute()
            )

            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def get_attachments(self, message_id: str) -> Optional[List[Dict]]:
        """
        Gets attachments from a message.

        Args:
            message_id (str): The ID of the message.

        Returns:
            List of attachments or None if an error occurs.
        """
        try:
            message = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="full")
                .execute()
            )

            attachments = []
            payload = message.get("payload", {})

            if "parts" in payload:
                for part in payload["parts"]:
                    if part.get("filename"):
                        attachment = {
                            "filename": part["filename"],
                            "mimeType": part["mimeType"],
                            "attachmentId": part["body"].get("attachmentId"),
                        }
                        attachments.append(attachment)

            return attachments
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
