"""
Connector for Local Files
"""

import os
from typing import List, Optional


class LocalFilesConnector:
    def __init__(self, base_path: str):
        """
        Initializes the Local Files Connector.

        Args:
            base_path (str): The base path to search for files.
        """
        self.base_path = base_path

    def list_files(self, extension: Optional[str] = None) -> List[str]:
        """
        Lists files in the base path.

        Args:
            extension (str): Optional file extension filter (e.g., '.txt', '.pdf')
        """
        files = []
        for dirpath, _, filenames in os.walk(self.base_path):
            for f in filenames:
                if extension is None or f.endswith(extension):
                    files.append(os.path.join(dirpath, f))
        return files

    def search_files(self, query: str) -> List[str]:
        """
        Searches for files containing the query in their name.

        Args:
            query (str): The search query.

        Returns:
            List of matching file paths.
        """
        matching_files = []
        for dirpath, _, filenames in os.walk(self.base_path):
            for f in filenames:
                if query.lower() in f.lower():
                    matching_files.append(os.path.join(dirpath, f))
        return matching_files

    def read_file(self, file_path: str) -> Optional[str]:
        """
        Reads a local file.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The content of the file or None if an error occurs.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    def write_file(self, file_path: str, content: str) -> bool:
        """
        Writes content to a local file.

        Args:
            file_path (str): The path to the file.
            content (str): The content to write.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
            return False
