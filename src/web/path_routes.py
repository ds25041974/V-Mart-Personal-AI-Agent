"""
Path Manager API Routes
Flask blueprint for managing local file/folder paths for AI access

Developed by: DSR
"""

import os

from flask import Blueprint, jsonify, request

from src.utils.path_manager import PathManager

# Create blueprint
path_bp = Blueprint("paths", __name__, url_prefix="/api/paths")

# Initialize PathManager
path_manager = PathManager()


@path_bp.route("/", methods=["GET"])
def get_all_paths():
    """Get all configured paths"""
    try:
        paths = path_manager.get_all_paths()
        return jsonify({"success": True, "paths": paths})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@path_bp.route("/add", methods=["POST"])
def add_path():
    """
    Add a new path configuration

    Request body:
    {
        "name": "Path name",
        "location": "/absolute/path/to/folder",
        "description": "Optional description"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        name = data.get("name", "").strip()
        location = data.get("location", "").strip()
        description = data.get("description", "").strip()

        # Validate inputs
        if not name:
            return jsonify({"success": False, "error": "Please provide path name"}), 400

        if not location:
            return jsonify(
                {"success": False, "error": "Please provide path location"}
            ), 400

        # Expand user home directory if present
        location = os.path.expanduser(location)

        # Validate path exists
        if not os.path.exists(location):
            return jsonify(
                {"success": False, "error": f"Path does not exist: {location}"}
            ), 400

        # Add path
        path_config = path_manager.add_path(name, location, description)

        return jsonify(
            {"success": True, "message": "Path added successfully", "path": path_config}
        )

    except ValueError as e:
        return jsonify(
            {"success": False, "error": f"Error validating path: {str(e)}"}
        ), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Error adding path: {str(e)}"}), 500


@path_bp.route("/<int:path_id>", methods=["DELETE"])
def remove_path(path_id):
    """Remove a path configuration"""
    try:
        success = path_manager.remove_path(path_id)

        if success:
            return jsonify({"success": True, "message": "Path removed successfully"})
        else:
            return jsonify({"success": False, "error": "Failed to remove path"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@path_bp.route("/<int:path_id>", methods=["GET"])
def get_path(path_id):
    """Get a specific path configuration"""
    try:
        path = path_manager.get_path(path_id)

        if path:
            return jsonify({"success": True, "path": path})
        else:
            return jsonify({"success": False, "error": "Path not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@path_bp.route("/<int:path_id>/scan", methods=["POST"])
def scan_path(path_id):
    """
    Scan a path and get file statistics

    Returns file count, types, and total size
    """
    try:
        result = path_manager.scan_path(path_id)

        return jsonify({"success": True, "scan_result": result})

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@path_bp.route("/<int:path_id>/files", methods=["GET"])
def get_files(path_id):
    """
    Get list of files from a path

    Query parameters:
    - limit: Maximum number of files (default: 100)
    - extensions: Comma-separated list of extensions (e.g., .pdf,.xlsx)
    """
    try:
        limit = request.args.get("limit", 100, type=int)
        extensions_str = request.args.get("extensions", "")

        # Parse extensions
        file_extensions = None
        if extensions_str:
            file_extensions = [ext.strip() for ext in extensions_str.split(",")]

        files = path_manager.get_files_from_path(
            path_id, limit=limit, file_extensions=file_extensions
        )

        return jsonify({"success": True, "files": files, "count": len(files)})

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@path_bp.route("/search", methods=["GET"])
def search_files():
    """
    Search for files across all configured paths

    Query parameters:
    - q: Search query (required)
    - limit: Maximum number of results (default: 50)
    - path_ids: Comma-separated path IDs to search in (optional)
    """
    try:
        query = request.args.get("q", "")

        if not query:
            return jsonify(
                {"success": False, "error": "Search query (q) is required"}
            ), 400

        limit = request.args.get("limit", 50, type=int)
        path_ids_str = request.args.get("path_ids", "")

        # Parse path IDs
        path_ids = None
        if path_ids_str:
            try:
                path_ids = [int(pid) for pid in path_ids_str.split(",")]
            except ValueError:
                return jsonify(
                    {"success": False, "error": "Invalid path_ids format"}
                ), 400

        results = path_manager.search_files(query, path_ids=path_ids, limit=limit)

        return jsonify(
            {"success": True, "results": results, "count": len(results), "query": query}
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@path_bp.route("/stats", methods=["GET"])
def get_stats():
    """Get overall statistics for all configured paths"""
    try:
        paths = path_manager.get_all_paths()

        total_paths = len(paths)
        total_files = sum(p.get("file_count", 0) for p in paths)
        total_size = sum(p.get("total_size", 0) for p in paths)

        # Get file type distribution
        all_file_types = {}
        for path in paths:
            file_types = path.get("file_types", {})
            for ext, count in file_types.items():
                all_file_types[ext] = all_file_types.get(ext, 0) + count

        return jsonify(
            {
                "success": True,
                "stats": {
                    "total_paths": total_paths,
                    "total_files": total_files,
                    "total_size": total_size,
                    "file_types": all_file_types,
                    "paths": [
                        {
                            "id": p.get("id"),
                            "name": p.get("name"),
                            "type": p.get("type"),
                            "file_count": p.get("file_count", 0),
                            "last_scanned": p.get("last_scanned"),
                        }
                        for p in paths
                    ],
                },
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@path_bp.route("/validate", methods=["POST"])
def validate_path():
    """
    Validate a path without adding it

    Request body:
    {
        "location": "/path/to/validate"
    }
    """
    try:
        data = request.get_json()

        if not data or "location" not in data:
            return jsonify({"success": False, "error": "Location is required"}), 400

        location = os.path.expanduser(data["location"])

        if not os.path.exists(location):
            return jsonify(
                {"success": False, "valid": False, "error": "Path does not exist"}
            )

        # Get path info
        is_file = os.path.isfile(location)

        info = {
            "valid": True,
            "exists": True,
            "type": "file" if is_file else "folder",
            "readable": os.access(location, os.R_OK),
            "writable": os.access(location, os.W_OK),
        }

        if is_file:
            info["size"] = os.path.getsize(location)
        else:
            # Quick count of files in directory
            try:
                file_count = sum(1 for _ in os.scandir(location) if _.is_file())
                info["file_count"] = file_count
            except Exception:
                info["file_count"] = 0

        return jsonify({"success": True, "path_info": info})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
