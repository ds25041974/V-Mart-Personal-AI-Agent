"""
Google Drive Connector
Handles connections and file operations with Google Drive
"""

import io
import logging
import os
import pickle
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

logger = logging.getLogger(__name__)


class GoogleDriveConnector:
    """Google Drive API connector"""

    SCOPES = [
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/drive.metadata.readonly",
    ]

    def __init__(self, credentials_file: str = "credentials.json"):
        self.credentials_file = credentials_file
        self.token_file = "token_drive.pickle"
        self.service = None
        self.creds = None

    def connect(self) -> bool:
        """Authenticate with Google Drive"""
        try:
            # Load saved credentials
            if os.path.exists(self.token_file):
                with open(self.token_file, "rb") as token:
                    self.creds = pickle.load(token)

            # Refresh or get new credentials
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)

                # Save credentials
                with open(self.token_file, "wb") as token:
                    pickle.dump(self.creds, token)

            # Build service
            self.service = build("drive", "v3", credentials=self.creds)
            logger.info("Connected to Google Drive")
            return True

        except Exception as e:
            logger.error(f"Google Drive authentication error: {str(e)}")
            return False

    def disconnect(self) -> bool:
        """Disconnect from Google Drive"""
        self.service = None
        self.creds = None
        logger.info("Disconnected from Google Drive")
        return True

    def list_files(
        self,
        folder_id: Optional[str] = None,
        query: Optional[str] = None,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """List files in Google Drive"""
        if not self.service:
            raise ConnectionError("Not connected to Google Drive")

        try:
            # Build query
            if folder_id:
                q = f"'{folder_id}' in parents"
            elif query:
                q = query
            else:
                q = "trashed=false"

            results = (
                self.service.files()
                .list(
                    q=q,
                    pageSize=max_results,
                    fields="files(id, name, mimeType, size, createdTime, modifiedTime, owners, parents, webViewLink, iconLink)",
                )
                .execute()
            )

            files = results.get("files", [])

            return [
                {
                    "id": file.get("id"),
                    "name": file.get("name"),
                    "mimeType": file.get("mimeType"),
                    "size": file.get("size"),
                    "createdTime": file.get("createdTime"),
                    "modifiedTime": file.get("modifiedTime"),
                    "owners": [
                        owner.get("emailAddress") for owner in file.get("owners", [])
                    ],
                    "parents": file.get("parents", []),
                    "webViewLink": file.get("webViewLink"),
                    "iconLink": file.get("iconLink"),
                }
                for file in files
            ]

        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            raise

    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """Get detailed metadata for a file"""
        if not self.service:
            raise ConnectionError("Not connected to Google Drive")

        try:
            file = (
                self.service.files()
                .get(
                    fileId=file_id,
                    fields="*",
                )
                .execute()
            )

            return {
                "id": file.get("id"),
                "name": file.get("name"),
                "mimeType": file.get("mimeType"),
                "description": file.get("description"),
                "size": file.get("size"),
                "createdTime": file.get("createdTime"),
                "modifiedTime": file.get("modifiedTime"),
                "viewedByMeTime": file.get("viewedByMeTime"),
                "owners": [
                    owner.get("emailAddress") for owner in file.get("owners", [])
                ],
                "lastModifyingUser": file.get("lastModifyingUser", {}).get(
                    "emailAddress"
                ),
                "shared": file.get("shared"),
                "parents": file.get("parents", []),
                "webViewLink": file.get("webViewLink"),
                "webContentLink": file.get("webContentLink"),
                "iconLink": file.get("iconLink"),
                "thumbnailLink": file.get("thumbnailLink"),
                "version": file.get("version"),
            }

        except Exception as e:
            logger.error(f"Error getting file metadata: {str(e)}")
            raise

    def download_file(self, file_id: str, destination_path: str) -> bool:
        """Download a file from Google Drive"""
        if not self.service:
            raise ConnectionError("Not connected to Google Drive")

        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                logger.info(f"Download {int(status.progress() * 100)}%")

            # Write to file
            with open(destination_path, "wb") as f:
                f.write(fh.getvalue())

            logger.info(f"Downloaded file to {destination_path}")
            return True

        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            return False

    def read_file_content(self, file_id: str) -> bytes:
        """Read file content directly"""
        if not self.service:
            raise ConnectionError("Not connected to Google Drive")

        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            return fh.getvalue()

        except Exception as e:
            logger.error(f"Error reading file content: {str(e)}")
            raise

    def search_files(
        self,
        name_contains: Optional[str] = None,
        mime_type: Optional[str] = None,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """Search for files in Google Drive"""
        if not self.service:
            raise ConnectionError("Not connected to Google Drive")

        try:
            query_parts = ["trashed=false"]

            if name_contains:
                query_parts.append(f"name contains '{name_contains}'")

            if mime_type:
                query_parts.append(f"mimeType='{mime_type}'")

            q = " and ".join(query_parts)

            return self.list_files(query=q, max_results=max_results)

        except Exception as e:
            logger.error(f"Error searching files: {str(e)}")
            raise

    def list_folders(
        self, parent_folder_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List folders in Google Drive"""
        if not self.service:
            raise ConnectionError("Not connected to Google Drive")

        try:
            query_parts = [
                "mimeType='application/vnd.google-apps.folder'",
                "trashed=false",
            ]

            if parent_folder_id:
                query_parts.append(f"'{parent_folder_id}' in parents")

            q = " and ".join(query_parts)

            return self.list_files(query=q)

        except Exception as e:
            logger.error(f"Error listing folders: {str(e)}")
            raise

    def get_shared_with_me(self, max_results: int = 100) -> List[Dict[str, Any]]:
        """Get files shared with the user"""
        if not self.service:
            raise ConnectionError("Not connected to Google Drive")

        try:
            q = "sharedWithMe=true and trashed=false"
            return self.list_files(query=q, max_results=max_results)

        except Exception as e:
            logger.error(f"Error getting shared files: {str(e)}")
            raise

    def test_connection(self) -> bool:
        """Test if Google Drive connection is alive"""
        try:
            if not self.service:
                return False

            # Try to get user info
            self.service.about().get(fields="user").execute()
            return True

        except Exception:
            return False
