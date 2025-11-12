"""
Admin Panel Database Models
Handles user management, whitelist, access control, and data policies
"""

import enum
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Super admin emails - bypass all rules
SUPER_ADMINS = [
    "dinesh.srivastava@vmart.co.in",
    "ds.250474@gmail.com",
    "dineshsrivastava07@gmail.com",
]


class UserRole(enum.Enum):
    """User roles in the system"""

    SUPER_ADMIN = "super_admin"  # Full access, no restrictions
    ADMIN = "admin"  # Can manage users and policies
    MANAGER = "manager"  # Limited admin access
    USER = "user"  # Regular user with assigned policies
    VIEWER = "viewer"  # Read-only access


class UserStatus(enum.Enum):
    """User account status"""

    PENDING = "pending"  # Awaiting email verification
    VERIFIED = "verified"  # Email verified, awaiting admin approval
    APPROVED = "approved"  # Approved by admin, active
    REJECTED = "rejected"  # Rejected by admin
    SUSPENDED = "suspended"  # Temporarily suspended
    DELISTED = "delisted"  # Permanently removed from whitelist


class User(Base):
    """
    User account with whitelist and approval workflow
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING, nullable=False)

    # Email verification
    email_verified = Column(Boolean, default=False, nullable=False)
    verification_token = Column(String(255), nullable=True)
    verification_sent_at = Column(DateTime, nullable=True)
    verified_at = Column(DateTime, nullable=True)

    # Approval workflow
    approved_by = Column(String(255), nullable=True)  # Admin who approved
    approved_at = Column(DateTime, nullable=True)
    rejected_by = Column(String(255), nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    # Account management
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    last_login = Column(DateTime, nullable=True)
    login_count = Column(Integer, default=0)

    # Session management
    current_session_token = Column(String(255), nullable=True)
    force_logout = Column(Boolean, default=False)  # Set to True to force logout

    # Notes
    notes = Column(Text, nullable=True)  # Admin notes about user

    # Relationships
    access_policies = relationship(
        "UserAccessPolicy", back_populates="user", cascade="all, delete-orphan"
    )
    activity_logs = relationship(
        "UserActivityLog", back_populates="user", cascade="all, delete-orphan"
    )

    def is_super_admin(self):
        """Check if user is a super admin (bypasses all rules)"""
        return self.email.lower() in [email.lower() for email in SUPER_ADMINS]

    def can_access(self):
        """Check if user can access the system"""
        if self.is_super_admin():
            return True
        return self.status == UserStatus.APPROVED and self.email_verified

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role.value,
            "status": self.status.value,
            "email_verified": self.email_verified,
            "is_super_admin": self.is_super_admin(),
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "login_count": self.login_count,
        }


class AccessLevel(enum.Enum):
    """Hierarchical access levels"""

    HO = "ho"  # Head Office - full access
    WAREHOUSE = "warehouse"
    ZONE = "zone"
    REGION = "region"
    STATE = "state"
    CITY = "city"
    STORE = "store"
    DIVISION = "division"
    DEPARTMENT = "department"
    ARTICLE = "article"


class UserAccessPolicy(Base):
    """
    Granular access control policies for users
    Defines what data a user can access at various hierarchical levels
    """

    __tablename__ = "user_access_policies"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Access level
    access_level = Column(Enum(AccessLevel), nullable=False)

    # Access values (JSON array for multiple values)
    # Example: {"stores": ["VM_DL_001", "VM_DL_002"], "zones": ["North"]}
    access_values = Column(JSON, nullable=False)

    # Permissions
    can_view_data = Column(Boolean, default=True)
    can_upload_files = Column(Boolean, default=False)
    can_use_data_catalogue = Column(Boolean, default=False)
    can_export_data = Column(Boolean, default=False)
    can_view_analytics = Column(Boolean, default=True)

    # Time restrictions
    valid_from = Column(DateTime, nullable=True)
    valid_until = Column(DateTime, nullable=True)

    # Metadata
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="access_policies")

    def is_active(self):
        """Check if policy is currently active"""
        now = datetime.utcnow()
        if self.valid_from and now < self.valid_from:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        return True

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "access_level": self.access_level.value,
            "access_values": self.access_values,
            "can_view_data": self.can_view_data,
            "can_upload_files": self.can_upload_files,
            "can_use_data_catalogue": self.can_use_data_catalogue,
            "can_export_data": self.can_export_data,
            "can_view_analytics": self.can_view_analytics,
            "valid_from": self.valid_from.isoformat() if self.valid_from else None,
            "valid_until": self.valid_until.isoformat() if self.valid_until else None,
            "is_active": self.is_active(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class DataAccessRule(Base):
    """
    Global data access rules (templates)
    Admins can create reusable access rule templates
    """

    __tablename__ = "data_access_rules"

    id = Column(Integer, primary_key=True)
    rule_name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    # Rule definition (JSON)
    # Example: {"type": "zone", "zones": ["North", "South"], "permissions": {...}}
    rule_definition = Column(JSON, nullable=False)

    # Metadata
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "rule_name": self.rule_name,
            "description": self.description,
            "rule_definition": self.rule_definition,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class UserActivityLog(Base):
    """
    Audit log for user activities
    Tracks all user actions for security and compliance
    """

    __tablename__ = "user_activity_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_email = Column(String(255), nullable=False, index=True)

    # Activity details
    action = Column(
        String(100), nullable=False
    )  # login, logout, upload_file, query_data, etc.
    resource = Column(String(255), nullable=True)  # What resource was accessed
    details = Column(JSON, nullable=True)  # Additional details

    # Result
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)

    # Context
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)

    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="activity_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "user_email": self.user_email,
            "action": self.action,
            "resource": self.resource,
            "details": self.details,
            "success": self.success,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


class EmailVerification(Base):
    """
    Email verification tokens and history
    """

    __tablename__ = "email_verifications"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, index=True)
    token = Column(String(255), nullable=False, unique=True, index=True)

    # Status
    verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)  # Token expiry (24 hours)

    # Metadata
    ip_address = Column(String(50), nullable=True)
    attempts = Column(Integer, default=0)  # Failed verification attempts

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "verified": self.verified,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_expired": self.is_expired(),
        }
