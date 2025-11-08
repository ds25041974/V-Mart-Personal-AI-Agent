"""
Configuration Manager
Secure credential storage and configuration management for backend connectors
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from cryptography.fernet import Fernet
except ImportError:
    Fernet = None

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages secure storage of credentials and configurations"""

    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else Path.home() / ".vmart"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.config_file = self.config_dir / "config.json"
        self.credentials_file = self.config_dir / "credentials.enc"
        self.key_file = self.config_dir / ".key"

        self.cipher = None
        self._initialize_encryption()

        self.config: Dict[str, Any] = {}
        self.credentials: Dict[str, Dict[str, Any]] = {}

        self._load_config()
        self._load_credentials()

    def _initialize_encryption(self):
        """Initialize encryption for credentials"""
        try:
            if not Fernet:
                logger.warning(
                    "cryptography library not available. Credentials will be stored unencrypted."
                )
                return

            if self.key_file.exists():
                # Load existing key
                with open(self.key_file, "rb") as f:
                    key = f.read()
            else:
                # Generate new key
                key = Fernet.generate_key()
                with open(self.key_file, "wb") as f:
                    f.write(key)
                # Secure the key file (Unix only)
                try:
                    os.chmod(self.key_file, 0o600)
                except Exception:
                    pass

            self.cipher = Fernet(key)
            logger.info("Encryption initialized for credentials")

        except Exception as e:
            logger.error(f"Error initializing encryption: {str(e)}")
            self.cipher = None

    def _load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
                logger.info("Loaded configuration")
            else:
                self.config = self._get_default_config()
                self._save_config()

        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            self.config = self._get_default_config()

    def _save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
            logger.info("Saved configuration")

        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "database": {
                "max_connections": 20,
                "connection_timeout": 30,
                "query_timeout": 300,
            },
            "ai": {
                "model": "gemini-1.5-pro",
                "max_tokens": 8192,
                "temperature": 0.7,
            },
            "file_system": {
                "allowed_extensions": [
                    ".txt",
                    ".pdf",
                    ".doc",
                    ".docx",
                    ".xlsx",
                    ".xls",
                    ".csv",
                    ".json",
                    ".xml",
                ],
                "max_file_size_mb": 100,
            },
            "api": {"rate_limit": 100, "rate_limit_period": 3600},
        }

    def _load_credentials(self):
        """Load encrypted credentials"""
        try:
            if not self.credentials_file.exists():
                self.credentials = {}
                return

            with open(self.credentials_file, "rb") as f:
                encrypted_data = f.read()

            if self.cipher:
                # Decrypt credentials
                decrypted_data = self.cipher.decrypt(encrypted_data)
                self.credentials = json.loads(decrypted_data.decode("utf-8"))
            else:
                # No encryption available
                self.credentials = json.loads(encrypted_data.decode("utf-8"))

            logger.info(f"Loaded {len(self.credentials)} credential sets")

        except Exception as e:
            logger.error(f"Error loading credentials: {str(e)}")
            self.credentials = {}

    def _save_credentials(self):
        """Save encrypted credentials"""
        try:
            credentials_json = json.dumps(self.credentials).encode("utf-8")

            if self.cipher:
                # Encrypt credentials
                encrypted_data = self.cipher.encrypt(credentials_json)
            else:
                # No encryption available
                encrypted_data = credentials_json

            with open(self.credentials_file, "wb") as f:
                f.write(encrypted_data)

            # Secure the credentials file (Unix only)
            try:
                os.chmod(self.credentials_file, 0o600)
            except Exception:
                pass

            logger.info("Saved credentials")

        except Exception as e:
            logger.error(f"Error saving credentials: {str(e)}")

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set_config(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split(".")
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        self._save_config()
        logger.info(f"Updated config: {key}")

    def get_credentials(self, service: str) -> Optional[Dict[str, Any]]:
        """Get credentials for a service"""
        return self.credentials.get(service)

    def set_credentials(self, service: str, credentials: Dict[str, Any]):
        """Set credentials for a service"""
        self.credentials[service] = credentials
        self._save_credentials()
        logger.info(f"Updated credentials for: {service}")

    def delete_credentials(self, service: str) -> bool:
        """Delete credentials for a service"""
        if service in self.credentials:
            del self.credentials[service]
            self._save_credentials()
            logger.info(f"Deleted credentials for: {service}")
            return True

        return False

    def list_services(self) -> list:
        """List all services with stored credentials"""
        return list(self.credentials.keys())

    def add_database_connection(
        self, name: str, db_type: str, connection_params: Dict[str, Any]
    ):
        """Add database connection credentials"""
        self.set_credentials(
            f"db_{name}", {"type": db_type, "params": connection_params}
        )

    def get_database_connection(self, name: str) -> Optional[Dict[str, Any]]:
        """Get database connection credentials"""
        return self.get_credentials(f"db_{name}")

    def list_database_connections(self) -> list:
        """List all database connections"""
        return [
            svc.replace("db_", "")
            for svc in self.credentials.keys()
            if svc.startswith("db_")
        ]

    def add_api_key(
        self,
        service: str,
        api_key: str,
        additional_params: Optional[Dict[str, Any]] = None,
    ):
        """Add API key for a service"""
        params = {"api_key": api_key}
        if additional_params:
            params.update(additional_params)
        self.set_credentials(f"api_{service}", params)

    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service"""
        creds = self.get_credentials(f"api_{service}")
        return creds.get("api_key") if creds else None

    def export_config(self, file_path: str, include_credentials: bool = False):
        """Export configuration to file"""
        try:
            export_data = {"config": self.config}

            if include_credentials:
                export_data["credentials"] = self.credentials

            with open(file_path, "w") as f:
                json.dump(export_data, f, indent=2)

            logger.info(f"Exported configuration to: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error exporting config: {str(e)}")
            return False

    def import_config(self, file_path: str):
        """Import configuration from file"""
        try:
            with open(file_path, "r") as f:
                import_data = json.load(f)

            if "config" in import_data:
                self.config = import_data["config"]
                self._save_config()

            if "credentials" in import_data:
                self.credentials = import_data["credentials"]
                self._save_credentials()

            logger.info(f"Imported configuration from: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error importing config: {str(e)}")
            return False


# Global configuration manager instance
config_manager = ConfigManager()
