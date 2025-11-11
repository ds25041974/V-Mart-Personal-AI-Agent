"""
Path Manager - Manage configured local paths for AI file access

Developed by: DSR
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class PathManager:
    """Manage configured local file/folder paths"""
    
    def __init__(self, config_file: str = "data/path_config.json"):
        self.config_file = config_file
        self.paths: List[Dict[str, Any]] = []
        self.load_paths()
    
    def load_paths(self):
        """Load configured paths from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.paths = data.get('paths', [])
        except Exception as e:
            print(f"Warning: Could not load path config: {e}")
            self.paths = []
    
    def save_paths(self):
        """Save configured paths to JSON file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump({'paths': self.paths, 'updated_at': datetime.now().isoformat()}, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving path config: {e}")
            return False
    
    def add_path(self, name: str, location: str, description: str = "") -> Dict[str, Any]:
        """
        Add a new path configuration
        
        Args:
            name: Human-readable name for the path
            location: Absolute path to file or folder
            description: Optional description
            
        Returns:
            Dictionary with path information
        """
        # Validate path exists
        path_obj = Path(location).expanduser()
        
        if not path_obj.exists():
            raise ValueError(f"Path does not exist: {location}")
        
        # Determine type
        path_type = "file" if path_obj.is_file() else "folder"
        
        # Generate ID
        path_id = len(self.paths)
        
        path_config = {
            "id": path_id,
            "name": name,
            "location": str(path_obj.absolute()),
            "description": description,
            "type": path_type,
            "added_at": datetime.now().isoformat(),
            "file_count": 0,
            "last_scanned": None
        }
        
        self.paths.append(path_config)
        self.save_paths()
        
        return path_config
    
    def remove_path(self, path_id: int) -> bool:
        """Remove a path configuration by ID"""
        try:
            self.paths = [p for p in self.paths if p.get('id') != path_id]
            # Re-index IDs
            for idx, path in enumerate(self.paths):
                path['id'] = idx
            self.save_paths()
            return True
        except Exception as e:
            print(f"Error removing path: {e}")
            return False
    
    def get_all_paths(self) -> List[Dict[str, Any]]:
        """Get all configured paths"""
        return self.paths
    
    def get_path(self, path_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific path by ID"""
        for path in self.paths:
            if path.get('id') == path_id:
                return path
        return None
    
    def scan_path(self, path_id: int) -> Dict[str, Any]:
        """
        Scan a configured path and count files
        
        Returns:
            Dictionary with scan results
        """
        path_config = self.get_path(path_id)
        
        if not path_config:
            raise ValueError(f"Path ID {path_id} not found")
        
        location = Path(path_config['location'])
        
        if not location.exists():
            raise ValueError(f"Path no longer exists: {location}")
        
        file_count = 0
        file_types = {}
        total_size = 0
        
        if location.is_file():
            file_count = 1
            ext = location.suffix.lower()
            file_types[ext] = 1
            total_size = location.stat().st_size
        else:
            # Scan folder recursively
            for file_path in location.rglob('*'):
                if file_path.is_file():
                    file_count += 1
                    ext = file_path.suffix.lower()
                    file_types[ext] = file_types.get(ext, 0) + 1
                    try:
                        total_size += file_path.stat().st_size
                    except:
                        pass
        
        # Update path config
        path_config['file_count'] = file_count
        path_config['file_types'] = file_types
        path_config['total_size'] = total_size
        path_config['last_scanned'] = datetime.now().isoformat()
        self.save_paths()
        
        return {
            "file_count": file_count,
            "file_types": file_types,
            "total_size": total_size,
            "scan_time": datetime.now().isoformat()
        }
    
    def get_files_from_path(self, path_id: int, limit: int = 100, file_extensions: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Get list of files from a configured path
        
        Args:
            path_id: Path configuration ID
            limit: Maximum number of files to return
            file_extensions: Optional filter by file extensions (e.g., ['.pdf', '.xlsx'])
            
        Returns:
            List of file information dictionaries
        """
        path_config = self.get_path(path_id)
        
        if not path_config:
            raise ValueError(f"Path ID {path_id} not found")
        
        location = Path(path_config['location'])
        
        if not location.exists():
            raise ValueError(f"Path no longer exists: {location}")
        
        files = []
        
        if location.is_file():
            # Single file
            if not file_extensions or location.suffix.lower() in file_extensions:
                files.append({
                    "name": location.name,
                    "path": str(location.absolute()),
                    "size": location.stat().st_size,
                    "extension": location.suffix.lower(),
                    "modified": datetime.fromtimestamp(location.stat().st_mtime).isoformat()
                })
        else:
            # Folder - scan for files
            for file_path in location.rglob('*'):
                if file_path.is_file():
                    if file_extensions and file_path.suffix.lower() not in file_extensions:
                        continue
                    
                    try:
                        files.append({
                            "name": file_path.name,
                            "path": str(file_path.absolute()),
                            "size": file_path.stat().st_size,
                            "extension": file_path.suffix.lower(),
                            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                            "relative_path": str(file_path.relative_to(location))
                        })
                        
                        if len(files) >= limit:
                            break
                    except Exception as e:
                        print(f"Warning: Could not process {file_path}: {e}")
                        continue
        
        # Sort by modified date (newest first)
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return files[:limit]
    
    def search_files(self, query: str, path_ids: Optional[List[int]] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for files matching query across configured paths
        
        Args:
            query: Search query (filename contains)
            path_ids: Optional list of path IDs to search in (None = all paths)
            limit: Maximum number of results
            
        Returns:
            List of matching files
        """
        search_paths = self.paths if path_ids is None else [p for p in self.paths if p['id'] in path_ids]
        
        results = []
        query_lower = query.lower()
        
        for path_config in search_paths:
            location = Path(path_config['location'])
            
            if not location.exists():
                continue
            
            if location.is_file():
                if query_lower in location.name.lower():
                    results.append({
                        "name": location.name,
                        "path": str(location.absolute()),
                        "size": location.stat().st_size,
                        "extension": location.suffix.lower(),
                        "source_path": path_config['name']
                    })
            else:
                for file_path in location.rglob('*'):
                    if file_path.is_file() and query_lower in file_path.name.lower():
                        try:
                            results.append({
                                "name": file_path.name,
                                "path": str(file_path.absolute()),
                                "size": file_path.stat().st_size,
                                "extension": file_path.suffix.lower(),
                                "source_path": path_config['name'],
                                "relative_path": str(file_path.relative_to(location))
                            })
                            
                            if len(results) >= limit:
                                break
                        except:
                            continue
            
            if len(results) >= limit:
                break
        
        return results[:limit]


# Global instance
path_manager = PathManager()
