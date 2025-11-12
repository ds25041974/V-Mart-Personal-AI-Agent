"""
Admin Panel Module
Provides user management, access control, and data filtering
"""

from .access_control import AccessControl, DataFilter, access_control, data_filter
from .database import get_admin_db, init_admin_database
from .email_service import EmailService, email_service
from .models import (
    SUPER_ADMINS,
    AccessLevel,
    DataAccessRule,
    EmailVerification,
    User,
    UserAccessPolicy,
    UserActivityLog,
    UserRole,
    UserStatus,
)
from .routes import admin_bp, init_admin_routes

# Create alias for consistency with app.py expectations
init_admin_db = init_admin_database

__all__ = [
    "admin_bp",
    "init_admin_db",
    "init_admin_database",
    "User",
    "UserRole",
    "UserStatus",
    "UserAccessPolicy",
    "AccessLevel",
    "DataAccessRule",
    "UserActivityLog",
    "EmailVerification",
    "SUPER_ADMINS",
    "get_admin_db",
    "AccessControl",
    "DataFilter",
    "access_control",
    "data_filter",
    "EmailService",
    "email_service",
    "init_admin_routes",
]
