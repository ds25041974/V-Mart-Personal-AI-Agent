"""
Access Control Middleware
Enforces user access policies and data filtering
"""

from datetime import datetime
from functools import wraps

from flask import g, jsonify, redirect, request, session, url_for

from .database import get_admin_db
from .models import SUPER_ADMINS, User, UserActivityLog, UserStatus


class AccessControl:
    """Access control manager"""

    @staticmethod
    def is_super_admin(email):
        """Check if email is a super admin"""
        if not email:
            return False
        return email.lower() in [admin.lower() for admin in SUPER_ADMINS]

    @staticmethod
    def get_current_user():
        """Get current user from session"""
        email = session.get("email")
        if not email:
            return None

        # Super admins bypass database check
        if AccessControl.is_super_admin(email):
            return {
                "email": email,
                "is_super_admin": True,
                "can_access": True,
                "role": "super_admin",
                "status": "approved",
                "access_policies": [],  # No restrictions
            }

        # Get user from database
        db = get_admin_db()
        db_session = db.get_session()
        try:
            user = db_session.query(User).filter(User.email == email).first()
            if not user:
                return None

            # Check if user should be forced out
            if user.force_logout or user.status == UserStatus.DELISTED:
                return None

            return {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "is_super_admin": False,
                "can_access": user.can_access(),
                "role": user.role.value,
                "status": user.status.value,
                "access_policies": [
                    p.to_dict() for p in user.access_policies if p.is_active()
                ],
            }
        finally:
            db_session.close()

    @staticmethod
    def log_activity(
        email, action, resource=None, success=True, error_message=None, details=None
    ):
        """Log user activity"""
        db = get_admin_db()
        db_session = db.get_session()
        try:
            # Get user ID if exists
            user = db_session.query(User).filter(User.email == email).first()
            user_id = user.id if user else None

            log = UserActivityLog(
                user_id=user_id,
                user_email=email,
                action=action,
                resource=resource,
                success=success,
                error_message=error_message,
                details=details,
                ip_address=request.remote_addr if request else None,
                user_agent=request.headers.get("User-Agent") if request else None,
            )
            db_session.add(log)
            db_session.commit()
        except Exception as e:
            print(f"Error logging activity: {str(e)}")
            db_session.rollback()
        finally:
            db_session.close()

    @staticmethod
    def check_user_access(f):
        """Decorator to check if user has access"""

        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = AccessControl.get_current_user()

            # No user in session
            if not user:
                return jsonify({"error": "Unauthorized. Please login."}), 401

            # Super admin - full access
            if user.get("is_super_admin"):
                g.current_user = user
                return f(*args, **kwargs)

            # Check if user can access
            if not user.get("can_access"):
                status = user.get("status", "unknown")
                if status == "pending":
                    return jsonify(
                        {"error": "Your account is pending email verification."}
                    ), 403
                elif status == "verified":
                    return jsonify(
                        {"error": "Your account is awaiting admin approval."}
                    ), 403
                elif status == "rejected":
                    return jsonify(
                        {"error": "Your account access has been rejected."}
                    ), 403
                elif status == "suspended":
                    return jsonify({"error": "Your account has been suspended."}), 403
                elif status == "delisted":
                    return jsonify(
                        {"error": "Your account has been removed. Access denied."}
                    ), 403
                else:
                    return jsonify({"error": "Access denied."}), 403

            # Store user in g for access in routes
            g.current_user = user
            return f(*args, **kwargs)

        return decorated_function

    @staticmethod
    def require_admin(f):
        """Decorator to require admin role"""

        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = AccessControl.get_current_user()

            if not user:
                return jsonify({"error": "Unauthorized"}), 401

            # Super admin always allowed
            if user.get("is_super_admin"):
                g.current_user = user
                return f(*args, **kwargs)

            # Check role
            role = user.get("role", "")
            if role not in ["admin", "super_admin"]:
                return jsonify({"error": "Admin access required"}), 403

            g.current_user = user
            return f(*args, **kwargs)

        return decorated_function


class DataFilter:
    """Data filtering based on user access policies"""

    @staticmethod
    def get_user_stores(user):
        """Get list of stores user can access"""
        if user.get("is_super_admin"):
            return None  # Access all stores

        stores = set()
        policies = user.get("access_policies", [])

        for policy in policies:
            if not policy["can_view_data"]:
                continue

            access_level = policy["access_level"]
            access_values = policy["access_values"]

            # Direct store access
            if access_level == "store" and "stores" in access_values:
                stores.update(access_values["stores"])

            # Zone/Region/City/State level access
            # These would need to be resolved to actual stores
            # For now, we'll store the filters

        return list(stores) if stores else []

    @staticmethod
    def get_access_filters(user):
        """Get all access filters for user"""
        if user.get("is_super_admin"):
            return {"unrestricted": True}

        filters = {
            "stores": set(),
            "zones": set(),
            "regions": set(),
            "states": set(),
            "cities": set(),
            "divisions": set(),
            "departments": set(),
            "articles": set(),
            "warehouses": set(),
        }

        policies = user.get("access_policies", [])

        for policy in policies:
            if not policy["can_view_data"]:
                continue

            access_values = policy["access_values"]

            # Merge all access values
            for key in filters.keys():
                if key in access_values:
                    filters[key].update(access_values[key])

        # Convert sets to lists
        return {k: list(v) if v else [] for k, v in filters.items()}

    @staticmethod
    def filter_stores_query(query, user):
        """Filter SQLAlchemy query for stores based on user access"""
        if user.get("is_super_admin"):
            return query

        filters = DataFilter.get_access_filters(user)

        # If user has no store access, return empty
        if not any(filters.values()):
            return query.filter(False)  # Returns empty result

        # Apply filters (this is a simplified version)
        # In production, you'd need to join with proper tables
        if filters.get("stores"):
            query = query.filter_by(store_id__in=filters["stores"])

        return query

    @staticmethod
    def filter_data_dict(data, user, data_type="store"):
        """Filter data dictionary based on user access"""
        if user.get("is_super_admin"):
            return data

        filters = DataFilter.get_access_filters(user)

        # Apply filtering based on data type
        if data_type == "store":
            if "store_id" in data and filters.get("stores"):
                if data["store_id"] not in filters["stores"]:
                    return None

        return data

    @staticmethod
    def can_user_perform_action(user, action):
        """Check if user can perform specific action"""
        if user.get("is_super_admin"):
            return True

        policies = user.get("access_policies", [])

        # Map actions to policy permissions
        permission_map = {
            "upload_files": "can_upload_files",
            "use_data_catalogue": "can_use_data_catalogue",
            "export_data": "can_export_data",
            "view_analytics": "can_view_analytics",
        }

        permission_field = permission_map.get(action, "can_view_data")

        # Check if any policy grants this permission
        for policy in policies:
            if policy.get(permission_field, False):
                return True

        return False


# Global access control instance
access_control = AccessControl()
data_filter = DataFilter()
