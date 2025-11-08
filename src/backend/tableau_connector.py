"""
Tableau Server/Online Connector
Handles connections and queries to Tableau Server and Tableau Online
"""

import logging
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class TableauConnector:
    """Tableau Server/Online API connector"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.server_url = config.get("server_url")
        self.site_id = config.get("site_id", "")
        self.api_version = config.get("api_version", "3.19")
        self.token = None
        self.site_id_from_signin = None
        self.user_id = None

    def connect(self) -> bool:
        """Authenticate with Tableau Server/Online"""
        try:
            auth_method = self.config.get("auth_method", "token")

            if auth_method == "token":
                return self._authenticate_token()
            elif auth_method == "username_password":
                return self._authenticate_username_password()
            else:
                logger.error(f"Unknown auth method: {auth_method}")
                return False

        except Exception as e:
            logger.error(f"Tableau authentication error: {str(e)}")
            return False

    def _authenticate_token(self) -> bool:
        """Authenticate using personal access token"""
        url = f"{self.server_url}/api/{self.api_version}/auth/signin"

        token_name = self.config.get("token_name")
        token_value = self.config.get("token_value")
        site_content_url = self.config.get("site_content_url", "")

        payload = {
            "credentials": {
                "personalAccessTokenName": token_name,
                "personalAccessTokenSecret": token_value,
                "site": {"contentUrl": site_content_url},
            }
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()

        data = response.json()
        self.token = data["credentials"]["token"]
        self.site_id_from_signin = data["credentials"]["site"]["id"]
        self.user_id = data["credentials"]["user"]["id"]

        logger.info("Authenticated with Tableau using token")
        return True

    def _authenticate_username_password(self) -> bool:
        """Authenticate using username and password"""
        url = f"{self.server_url}/api/{self.api_version}/auth/signin"

        username = self.config.get("username")
        password = self.config.get("password")
        site_content_url = self.config.get("site_content_url", "")

        payload = {
            "credentials": {
                "name": username,
                "password": password,
                "site": {"contentUrl": site_content_url},
            }
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()

        data = response.json()
        self.token = data["credentials"]["token"]
        self.site_id_from_signin = data["credentials"]["site"]["id"]
        self.user_id = data["credentials"]["user"]["id"]

        logger.info("Authenticated with Tableau using username/password")
        return True

    def disconnect(self) -> bool:
        """Sign out from Tableau"""
        try:
            if not self.token:
                return True

            url = f"{self.server_url}/api/{self.api_version}/auth/signout"
            headers = {"X-Tableau-Auth": self.token}

            response = requests.post(url, headers=headers)
            response.raise_for_status()

            self.token = None
            logger.info("Signed out from Tableau")
            return True

        except Exception as e:
            logger.error(f"Tableau signout error: {str(e)}")
            return False

    def get_workbooks(self) -> List[Dict[str, Any]]:
        """Get list of workbooks"""
        if not self.token:
            raise ConnectionError("Not authenticated with Tableau")

        try:
            url = f"{self.server_url}/api/{self.api_version}/sites/{self.site_id_from_signin}/workbooks"
            headers = {"X-Tableau-Auth": self.token}

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            workbooks = data.get("workbooks", {}).get("workbook", [])

            return [
                {
                    "id": wb.get("id"),
                    "name": wb.get("name"),
                    "description": wb.get("description"),
                    "createdAt": wb.get("createdAt"),
                    "updatedAt": wb.get("updatedAt"),
                    "project": wb.get("project", {}).get("name"),
                    "owner": wb.get("owner", {}).get("name"),
                    "tags": [
                        tag.get("label") for tag in wb.get("tags", {}).get("tag", [])
                    ],
                }
                for wb in workbooks
            ]

        except Exception as e:
            logger.error(f"Error getting workbooks: {str(e)}")
            raise

    def get_workbook_views(self, workbook_id: str) -> List[Dict[str, Any]]:
        """Get views in a workbook"""
        if not self.token:
            raise ConnectionError("Not authenticated with Tableau")

        try:
            url = f"{self.server_url}/api/{self.api_version}/sites/{self.site_id_from_signin}/workbooks/{workbook_id}/views"
            headers = {"X-Tableau-Auth": self.token}

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            views = data.get("views", {}).get("view", [])

            return [
                {
                    "id": view.get("id"),
                    "name": view.get("name"),
                    "contentUrl": view.get("contentUrl"),
                    "createdAt": view.get("createdAt"),
                    "updatedAt": view.get("updatedAt"),
                    "workbook": view.get("workbook", {}).get("name"),
                    "owner": view.get("owner", {}).get("name"),
                    "tags": [
                        tag.get("label") for tag in view.get("tags", {}).get("tag", [])
                    ],
                }
                for view in views
            ]

        except Exception as e:
            logger.error(f"Error getting workbook views: {str(e)}")
            raise

    def get_datasources(self) -> List[Dict[str, Any]]:
        """Get list of data sources"""
        if not self.token:
            raise ConnectionError("Not authenticated with Tableau")

        try:
            url = f"{self.server_url}/api/{self.api_version}/sites/{self.site_id_from_signin}/datasources"
            headers = {"X-Tableau-Auth": self.token}

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            datasources = data.get("datasources", {}).get("datasource", [])

            return [
                {
                    "id": ds.get("id"),
                    "name": ds.get("name"),
                    "description": ds.get("description"),
                    "type": ds.get("type"),
                    "createdAt": ds.get("createdAt"),
                    "updatedAt": ds.get("updatedAt"),
                    "project": ds.get("project", {}).get("name"),
                    "owner": ds.get("owner", {}).get("name"),
                    "isCertified": ds.get("isCertified"),
                    "tags": [
                        tag.get("label") for tag in ds.get("tags", {}).get("tag", [])
                    ],
                }
                for ds in datasources
            ]

        except Exception as e:
            logger.error(f"Error getting datasources: {str(e)}")
            raise

    def get_projects(self) -> List[Dict[str, Any]]:
        """Get list of projects"""
        if not self.token:
            raise ConnectionError("Not authenticated with Tableau")

        try:
            url = f"{self.server_url}/api/{self.api_version}/sites/{self.site_id_from_signin}/projects"
            headers = {"X-Tableau-Auth": self.token}

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            projects = data.get("projects", {}).get("project", [])

            return [
                {
                    "id": proj.get("id"),
                    "name": proj.get("name"),
                    "description": proj.get("description"),
                    "createdAt": proj.get("createdAt"),
                    "updatedAt": proj.get("updatedAt"),
                    "parentProjectId": proj.get("parentProjectId"),
                }
                for proj in projects
            ]

        except Exception as e:
            logger.error(f"Error getting projects: {str(e)}")
            raise

    def query_view_data(
        self, view_id: str, filters: Optional[Dict[str, str]] = None
    ) -> bytes:
        """Query data from a view with optional filters"""
        if not self.token:
            raise ConnectionError("Not authenticated with Tableau")

        try:
            url = f"{self.server_url}/api/{self.api_version}/sites/{self.site_id_from_signin}/views/{view_id}/data"
            headers = {"X-Tableau-Auth": self.token}

            # Add filters as query parameters
            params = {}
            if filters:
                for key, value in filters.items():
                    params[f"vf_{key}"] = value

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            # Returns CSV data
            return response.content

        except Exception as e:
            logger.error(f"Error querying view data: {str(e)}")
            raise

    def get_view_image(self, view_id: str, resolution: str = "high") -> bytes:
        """Get view as image"""
        if not self.token:
            raise ConnectionError("Not authenticated with Tableau")

        try:
            url = f"{self.server_url}/api/{self.api_version}/sites/{self.site_id_from_signin}/views/{view_id}/image"
            headers = {"X-Tableau-Auth": self.token}
            params = {"resolution": resolution}

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            return response.content

        except Exception as e:
            logger.error(f"Error getting view image: {str(e)}")
            raise

    def get_view_pdf(self, view_id: str, page_type: str = "Letter") -> bytes:
        """Get view as PDF"""
        if not self.token:
            raise ConnectionError("Not authenticated with Tableau")

        try:
            url = f"{self.server_url}/api/{self.api_version}/sites/{self.site_id_from_signin}/views/{view_id}/pdf"
            headers = {"X-Tableau-Auth": self.token}
            params = {"type": page_type}

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            return response.content

        except Exception as e:
            logger.error(f"Error getting view PDF: {str(e)}")
            raise

    def test_connection(self) -> bool:
        """Test if Tableau connection is alive"""
        try:
            if not self.token:
                return False

            url = f"{self.server_url}/api/{self.api_version}/sites/{self.site_id_from_signin}"
            headers = {"X-Tableau-Auth": self.token}

            response = requests.get(url, headers=headers)
            return response.status_code == 200

        except Exception:
            return False
