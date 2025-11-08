"""
File System Connector
Handles reading files from local and network file systems
"""

import logging
import mimetypes
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class FileSystemConnector:
    """Local and network file system connector"""

    def __init__(self, base_path: Optional[str] = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.allowed_extensions = [
            # Documents
            ".txt",
            ".pdf",
            ".doc",
            ".docx",
            ".odt",
            # Spreadsheets
            ".csv",
            ".xlsx",
            ".xls",
            ".ods",
            # Presentations
            ".pptx",
            ".ppt",
            ".odp",
            # Data files
            ".json",
            ".xml",
            ".yaml",
            ".yml",
            # Logs
            ".log",
            # Markdown
            ".md",
            ".markdown",
        ]

    def set_base_path(self, path: str) -> bool:
        """Set the base path for file operations"""
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                logger.error(f"Path does not exist: {path}")
                return False

            if not path_obj.is_dir():
                logger.error(f"Path is not a directory: {path}")
                return False

            self.base_path = path_obj
            logger.info(f"Base path set to: {path}")
            return True

        except Exception as e:
            logger.error(f"Error setting base path: {str(e)}")
            return False

    def list_files(
        self,
        path: Optional[str] = None,
        recursive: bool = False,
        filter_extensions: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """List files in a directory"""
        try:
            search_path = Path(path) if path else self.base_path

            if not search_path.exists():
                logger.error(f"Path does not exist: {search_path}")
                return []

            files = []

            if recursive:
                pattern = "**/*"
            else:
                pattern = "*"

            for file_path in search_path.glob(pattern):
                if file_path.is_file():
                    # Filter by extension
                    if filter_extensions:
                        if file_path.suffix.lower() not in filter_extensions:
                            continue
                    elif file_path.suffix.lower() not in self.allowed_extensions:
                        continue

                    file_info = self._get_file_info(file_path)
                    files.append(file_info)

            logger.info(f"Found {len(files)} files in {search_path}")
            return files

        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return []

    def _get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get metadata for a file"""
        try:
            stat = file_path.stat()
            mime_type, _ = mimetypes.guess_type(str(file_path))

            return {
                "name": file_path.name,
                "path": str(file_path.absolute()),
                "extension": file_path.suffix,
                "size": stat.st_size,
                "created_time": stat.st_ctime,
                "modified_time": stat.st_mtime,
                "accessed_time": stat.st_atime,
                "is_readonly": not os.access(file_path, os.W_OK),
                "mime_type": mime_type,
            }

        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {str(e)}")
            return {"name": file_path.name, "path": str(file_path), "error": str(e)}

    def read_file(self, file_path: str, encoding: str = "utf-8") -> Optional[str]:
        """Read text file content"""
        try:
            path = Path(file_path)

            if not path.exists():
                logger.error(f"File does not exist: {file_path}")
                return None

            if not path.is_file():
                logger.error(f"Path is not a file: {file_path}")
                return None

            with open(path, "r", encoding=encoding) as f:
                content = f.read()

            logger.info(f"Read file: {file_path} ({len(content)} characters)")
            return content

        except UnicodeDecodeError:
            logger.warning(
                f"Unicode decode error, trying with latin-1 encoding: {file_path}"
            )
            try:
                with open(path, "r", encoding="latin-1") as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error reading file with latin-1: {str(e)}")
                return None

        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return None

    def read_binary_file(self, file_path: str) -> Optional[bytes]:
        """Read binary file content"""
        try:
            path = Path(file_path)

            if not path.exists():
                logger.error(f"File does not exist: {file_path}")
                return None

            if not path.is_file():
                logger.error(f"Path is not a file: {file_path}")
                return None

            with open(path, "rb") as f:
                content = f.read()

            logger.info(f"Read binary file: {file_path} ({len(content)} bytes)")
            return content

        except Exception as e:
            logger.error(f"Error reading binary file {file_path}: {str(e)}")
            return None

    def search_files(
        self,
        pattern: str,
        path: Optional[str] = None,
        recursive: bool = True,
    ) -> List[Dict[str, Any]]:
        """Search for files matching a pattern"""
        try:
            search_path = Path(path) if path else self.base_path

            if not search_path.exists():
                logger.error(f"Path does not exist: {search_path}")
                return []

            files = []

            if recursive:
                glob_pattern = f"**/{pattern}"
            else:
                glob_pattern = pattern

            for file_path in search_path.glob(glob_pattern):
                if file_path.is_file():
                    file_info = self._get_file_info(file_path)
                    files.append(file_info)

            logger.info(f"Found {len(files)} files matching pattern: {pattern}")
            return files

        except Exception as e:
            logger.error(f"Error searching files: {str(e)}")
            return []

    def get_directory_tree(
        self, path: Optional[str] = None, max_depth: int = 3
    ) -> Dict[str, Any]:
        """Get directory tree structure"""
        try:
            root_path = Path(path) if path else self.base_path

            if not root_path.exists():
                logger.error(f"Path does not exist: {root_path}")
                return {}

            def build_tree(current_path: Path, depth: int = 0) -> Dict[str, Any]:
                if depth >= max_depth:
                    return {"truncated": True}

                tree = {
                    "name": current_path.name,
                    "path": str(current_path.absolute()),
                    "is_dir": current_path.is_dir(),
                }

                if current_path.is_dir():
                    children = []
                    try:
                        for child in sorted(current_path.iterdir()):
                            # Skip hidden files and system folders
                            if child.name.startswith("."):
                                continue

                            child_tree = build_tree(child, depth + 1)
                            children.append(child_tree)

                        tree["children"] = children
                        tree["file_count"] = sum(
                            1 for c in children if not c.get("is_dir")
                        )
                        tree["dir_count"] = sum(1 for c in children if c.get("is_dir"))

                    except PermissionError:
                        tree["error"] = "Permission denied"

                else:
                    tree.update(self._get_file_info(current_path))

                return tree

            return build_tree(root_path)

        except Exception as e:
            logger.error(f"Error getting directory tree: {str(e)}")
            return {"error": str(e)}

    def get_file_metadata(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get detailed metadata for a file"""
        try:
            path = Path(file_path)

            if not path.exists():
                logger.error(f"File does not exist: {file_path}")
                return None

            return self._get_file_info(path)

        except Exception as e:
            logger.error(f"Error getting file metadata: {str(e)}")
            return None

    def list_directories(
        self, path: Optional[str] = None, recursive: bool = False
    ) -> List[Dict[str, Any]]:
        """List directories"""
        try:
            search_path = Path(path) if path else self.base_path

            if not search_path.exists():
                logger.error(f"Path does not exist: {search_path}")
                return []

            directories = []

            if recursive:
                pattern = "**/*"
            else:
                pattern = "*"

            for dir_path in search_path.glob(pattern):
                if dir_path.is_dir() and not dir_path.name.startswith("."):
                    dir_info = {
                        "name": dir_path.name,
                        "path": str(dir_path.absolute()),
                        "modified_time": dir_path.stat().st_mtime,
                    }
                    directories.append(dir_info)

            logger.info(f"Found {len(directories)} directories in {search_path}")
            return directories

        except Exception as e:
            logger.error(f"Error listing directories: {str(e)}")
            return []
