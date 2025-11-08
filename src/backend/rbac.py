"""
Role-Based Access Control (RBAC) System
Manages users, roles, permissions, and access control for backend resources
"""

import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


class Permission(Enum):
    """System permissions"""

    # Database operations
    DB_CONNECT = "db:connect"
    DB_QUERY = "db:query"
    DB_WRITE = "db:write"
    DB_ADMIN = "db:admin"

    # Data source operations
    DATASOURCE_READ = "datasource:read"
    DATASOURCE_WRITE = "datasource:write"
    DATASOURCE_ADMIN = "datasource:admin"

    # File system operations
    FILE_READ = "file:read"
    FILE_WRITE = "file:write"
    FILE_DELETE = "file:delete"

    # AI operations
    AI_QUERY = "ai:query"
    AI_ANALYZE = "ai:analyze"
    AI_RECOMMEND = "ai:recommend"

    # User management
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"

    # Role management
    ROLE_READ = "role:read"
    ROLE_WRITE = "role:write"
    ROLE_DELETE = "role:delete"

    # System administration
    SYSTEM_CONFIG = "system:config"
    SYSTEM_ADMIN = "system:admin"


class Role:
    """User role with permissions"""

    def __init__(
        self,
        name: str,
        description: str,
        permissions: Optional[Set[Permission]] = None,
    ):
        self.name = name
        self.description = description
        self.permissions: Set[Permission] = permissions or set()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_permission(self, permission: Permission):
        """Add a permission to the role"""
        self.permissions.add(permission)
        self.updated_at = datetime.now()

    def remove_permission(self, permission: Permission):
        """Remove a permission from the role"""
        self.permissions.discard(permission)
        self.updated_at = datetime.now()

    def has_permission(self, permission: Permission) -> bool:
        """Check if role has a permission"""
        return permission in self.permissions

    def to_dict(self) -> Dict[str, Any]:
        """Convert role to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "permissions": [p.value for p in self.permissions],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class User:
    """System user with roles and permissions"""

    def __init__(
        self,
        username: str,
        email: str,
        roles: Optional[List[Role]] = None,
    ):
        self.username = username
        self.email = email
        self.roles: List[Role] = roles or []
        self.is_active = True
        self.created_at = datetime.now()
        self.last_login = None
        self.metadata: Dict[str, Any] = {}

    def add_role(self, role: Role):
        """Add a role to the user"""
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role: Role):
        """Remove a role from the user"""
        if role in self.roles:
            self.roles.remove(role)

    def has_permission(self, permission: Permission) -> bool:
        """Check if user has a permission through any role"""
        if not self.is_active:
            return False

        for role in self.roles:
            if role.has_permission(permission):
                return True

        return False

    def has_any_permission(self, permissions: List[Permission]) -> bool:
        """Check if user has any of the specified permissions"""
        for permission in permissions:
            if self.has_permission(permission):
                return True
        return False

    def has_all_permissions(self, permissions: List[Permission]) -> bool:
        """Check if user has all specified permissions"""
        for permission in permissions:
            if not self.has_permission(permission):
                return False
        return True

    def get_all_permissions(self) -> Set[Permission]:
        """Get all permissions from all roles"""
        all_permissions = set()
        for role in self.roles:
            all_permissions.update(role.permissions)
        return all_permissions

    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary"""
        return {
            "username": self.username,
            "email": self.email,
            "roles": [role.name for role in self.roles],
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "permissions": [p.value for p in self.get_all_permissions()],
        }


class RBACManager:
    """RBAC system manager"""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.roles: Dict[str, Role] = {}
        self._initialize_default_roles()

    def _initialize_default_roles(self):
        """Initialize default system roles"""
        # Admin role - full access
        admin_role = Role(
            "admin",
            "System administrator with full access",
            {
                Permission.DB_ADMIN,
                Permission.DATASOURCE_ADMIN,
                Permission.FILE_DELETE,
                Permission.AI_QUERY,
                Permission.AI_ANALYZE,
                Permission.AI_RECOMMEND,
                Permission.USER_WRITE,
                Permission.USER_DELETE,
                Permission.ROLE_WRITE,
                Permission.ROLE_DELETE,
                Permission.SYSTEM_ADMIN,
                Permission.SYSTEM_CONFIG,
            },
        )

        # Analyst role - data access and AI
        analyst_role = Role(
            "analyst",
            "Data analyst with read access and AI capabilities",
            {
                Permission.DB_CONNECT,
                Permission.DB_QUERY,
                Permission.DATASOURCE_READ,
                Permission.FILE_READ,
                Permission.AI_QUERY,
                Permission.AI_ANALYZE,
                Permission.AI_RECOMMEND,
                Permission.USER_READ,
                Permission.ROLE_READ,
            },
        )

        # Viewer role - read-only access
        viewer_role = Role(
            "viewer",
            "Read-only access to data and reports",
            {
                Permission.DB_CONNECT,
                Permission.DB_QUERY,
                Permission.DATASOURCE_READ,
                Permission.FILE_READ,
                Permission.AI_QUERY,
            },
        )

        # Developer role - read/write access, no admin
        developer_role = Role(
            "developer",
            "Developer with read/write access to data sources",
            {
                Permission.DB_CONNECT,
                Permission.DB_QUERY,
                Permission.DB_WRITE,
                Permission.DATASOURCE_READ,
                Permission.DATASOURCE_WRITE,
                Permission.FILE_READ,
                Permission.FILE_WRITE,
                Permission.AI_QUERY,
                Permission.AI_ANALYZE,
            },
        )

        self.roles["admin"] = admin_role
        self.roles["analyst"] = analyst_role
        self.roles["viewer"] = viewer_role
        self.roles["developer"] = developer_role

        logger.info("Initialized default RBAC roles")

    def create_user(
        self, username: str, email: str, role_names: Optional[List[str]] = None
    ) -> Optional[User]:
        """Create a new user"""
        try:
            if username in self.users:
                logger.warning(f"User already exists: {username}")
                return None

            # Get roles
            roles = []
            if role_names:
                for role_name in role_names:
                    if role_name in self.roles:
                        roles.append(self.roles[role_name])
                    else:
                        logger.warning(f"Role not found: {role_name}")

            user = User(username, email, roles)
            self.users[username] = user

            logger.info(f"Created user: {username} with roles: {role_names}")
            return user

        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return None

    def get_user(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.users.get(username)

    def delete_user(self, username: str) -> bool:
        """Delete a user"""
        try:
            if username in self.users:
                del self.users[username]
                logger.info(f"Deleted user: {username}")
                return True

            logger.warning(f"User not found: {username}")
            return False

        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return False

    def update_user_roles(self, username: str, role_names: List[str]) -> bool:
        """Update user's roles"""
        try:
            user = self.get_user(username)
            if not user:
                logger.warning(f"User not found: {username}")
                return False

            # Clear existing roles
            user.roles = []

            # Add new roles
            for role_name in role_names:
                if role_name in self.roles:
                    user.add_role(self.roles[role_name])
                else:
                    logger.warning(f"Role not found: {role_name}")

            logger.info(f"Updated roles for user {username}: {role_names}")
            return True

        except Exception as e:
            logger.error(f"Error updating user roles: {str(e)}")
            return False

    def create_role(
        self, name: str, description: str, permissions: Optional[List[str]] = None
    ) -> Optional[Role]:
        """Create a custom role"""
        try:
            if name in self.roles:
                logger.warning(f"Role already exists: {name}")
                return None

            # Parse permissions
            role_permissions = set()
            if permissions:
                for perm_str in permissions:
                    try:
                        permission = Permission(perm_str)
                        role_permissions.add(permission)
                    except ValueError:
                        logger.warning(f"Invalid permission: {perm_str}")

            role = Role(name, description, role_permissions)
            self.roles[name] = role

            logger.info(f"Created role: {name}")
            return role

        except Exception as e:
            logger.error(f"Error creating role: {str(e)}")
            return None

    def get_role(self, name: str) -> Optional[Role]:
        """Get role by name"""
        return self.roles.get(name)

    def delete_role(self, name: str) -> bool:
        """Delete a role"""
        try:
            # Don't delete default roles
            if name in ["admin", "analyst", "viewer", "developer"]:
                logger.warning(f"Cannot delete default role: {name}")
                return False

            if name in self.roles:
                # Remove role from all users
                for user in self.users.values():
                    role = self.roles[name]
                    user.remove_role(role)

                del self.roles[name]
                logger.info(f"Deleted role: {name}")
                return True

            logger.warning(f"Role not found: {name}")
            return False

        except Exception as e:
            logger.error(f"Error deleting role: {str(e)}")
            return False

    def check_permission(self, username: str, permission: Permission) -> bool:
        """Check if user has permission"""
        user = self.get_user(username)
        if not user:
            return False

        return user.has_permission(permission)

    def list_users(self) -> List[Dict[str, Any]]:
        """List all users"""
        return [user.to_dict() for user in self.users.values()]

    def list_roles(self) -> List[Dict[str, Any]]:
        """List all roles"""
        return [role.to_dict() for role in self.roles.values()]

    def get_user_permissions(self, username: str) -> List[str]:
        """Get all permissions for a user"""
        user = self.get_user(username)
        if not user:
            return []

        return [p.value for p in user.get_all_permissions()]


# Global RBAC manager instance
rbac_manager = RBACManager()
