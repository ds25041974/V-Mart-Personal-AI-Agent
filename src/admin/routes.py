"""
Admin Panel Routes
Handles user management, access control, and admin operations
"""

import json
from datetime import datetime

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .access_control import AccessControl, access_control
from .database import get_admin_db
from .email_service import email_service
from .models import (
    SUPER_ADMINS,
    AccessLevel,
    DataAccessRule,
    User,
    UserAccessPolicy,
    UserRole,
    UserStatus,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ============================================================================
# Authentication & Email Verification
# ============================================================================


@admin_bp.route("/register", methods=["POST"])
def register():
    """
    Register new user (creates pending account)
    Super admins don't need to register
    """
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    name = data.get("name", "").strip()

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Check if super admin
    if AccessControl.is_super_admin(email):
        return jsonify(
            {
                "success": True,
                "message": "Super admin - no registration required. Please login directly.",
                "is_super_admin": True,
            }
        ), 200

    db = get_admin_db()
    db_session = db.get_session()
    try:
        # Check if user already exists
        existing_user = db_session.query(User).filter(User.email == email).first()
        if existing_user:
            if existing_user.status == UserStatus.PENDING:
                return jsonify(
                    {"error": "Account pending email verification. Check your email."}
                ), 400
            elif existing_user.status == UserStatus.VERIFIED:
                return jsonify({"error": "Account awaiting admin approval."}), 400
            elif existing_user.status == UserStatus.REJECTED:
                return jsonify(
                    {"error": "Account was rejected. Contact administrator."}
                ), 403
            elif existing_user.status == UserStatus.DELISTED:
                return jsonify(
                    {"error": "Account has been removed. Access denied."}
                ), 403
            else:
                return jsonify({"error": "Email already registered"}), 400

        # Create new user
        user = User(
            email=email,
            name=name or email.split("@")[0],
            role=UserRole.USER,
            status=UserStatus.PENDING,
            email_verified=False,
        )
        db_session.add(user)
        db_session.commit()

        # Send verification email
        token = email_service.create_verification_token(email, request.remote_addr)
        if token:
            email_service.send_verification_email(email, token)

        # Log activity
        AccessControl.log_activity(email, "register", success=True)

        return jsonify(
            {
                "success": True,
                "message": "Registration successful! Please check your email to verify your account.",
                "email": email,
                "status": "pending_verification",
            }
        ), 201
    except Exception as e:
        db_session.rollback()
        AccessControl.log_activity(
            email, "register", success=False, error_message=str(e)
        )
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500
    finally:
        db_session.close()


@admin_bp.route("/verify-email", methods=["GET", "POST"])
def verify_email():
    """Verify email with token"""
    if request.method == "GET":
        token = request.args.get("token", "")
        # Return verification page
        return render_template("admin/verify_email.html", token=token)

    # POST method
    data = request.get_json() if request.is_json else request.form
    token = data.get("token", "")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    result = email_service.verify_token(token)

    if result["success"]:
        AccessControl.log_activity(result["email"], "email_verified", success=True)
        return jsonify(result), 200
    else:
        return jsonify(result), 400


# ============================================================================
# Admin Panel - User Management
# ============================================================================


@admin_bp.route("/dashboard")
@access_control.require_admin
def dashboard():
    """Admin dashboard"""
    return render_template("admin/dashboard.html")


@admin_bp.route("/users", methods=["GET"])
@access_control.require_admin
def list_users():
    """List all users"""
    db = get_admin_db()
    db_session = db.get_session()
    try:
        status_filter = request.args.get("status", "").lower()

        query = db_session.query(User)

        # Filter by status
        if status_filter and status_filter != "all":
            try:
                status_enum = UserStatus[status_filter.upper()]
                query = query.filter(User.status == status_enum)
            except KeyError:
                pass

        users = query.order_by(User.created_at.desc()).all()

        return jsonify(
            {"users": [user.to_dict() for user in users], "count": len(users)}
        ), 200
    finally:
        db_session.close()


@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@access_control.require_admin
def get_user(user_id):
    """Get user details"""
    db = get_admin_db()
    db_session = db.get_session()
    try:
        user = db_session.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_dict = user.to_dict()
        user_dict["access_policies"] = [p.to_dict() for p in user.access_policies]

        return jsonify(user_dict), 200
    finally:
        db_session.close()


@admin_bp.route("/users/<int:user_id>/approve", methods=["POST"])
@access_control.require_admin
def approve_user(user_id):
    """Approve user account"""
    db = get_admin_db()
    db_session = db.get_session()
    try:
        user = db_session.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.is_super_admin():
            return jsonify({"error": "Cannot modify super admin"}), 403

        if not user.email_verified:
            return jsonify({"error": "User email not verified yet"}), 400

        # Approve user
        admin_email = session.get("email", "system")
        user.status = UserStatus.APPROVED
        user.approved_by = admin_email
        user.approved_at = datetime.utcnow()
        user.force_logout = False

        db_session.commit()

        # Send approval notification
        email_service.send_approval_notification(user.email)

        # Log activity
        AccessControl.log_activity(
            admin_email, "approve_user", resource=user.email, success=True
        )

        return jsonify(
            {
                "success": True,
                "message": f"User {user.email} approved",
                "user": user.to_dict(),
            }
        ), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


@admin_bp.route("/users/<int:user_id>/reject", methods=["POST"])
@access_control.require_admin
def reject_user(user_id):
    """Reject user account"""
    data = request.get_json()
    reason = data.get("reason", "Not specified")

    db = get_admin_db()
    db_session = db.get_session()
    try:
        user = db_session.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.is_super_admin():
            return jsonify({"error": "Cannot modify super admin"}), 403

        # Reject user
        admin_email = session.get("email", "system")
        user.status = UserStatus.REJECTED
        user.rejected_by = admin_email
        user.rejected_at = datetime.utcnow()
        user.rejection_reason = reason
        user.force_logout = True

        db_session.commit()

        # Send rejection notification
        email_service.send_rejection_notification(user.email, reason)

        # Log activity
        AccessControl.log_activity(
            admin_email,
            "reject_user",
            resource=user.email,
            success=True,
            details={"reason": reason},
        )

        return jsonify(
            {
                "success": True,
                "message": f"User {user.email} rejected",
                "user": user.to_dict(),
            }
        ), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


@admin_bp.route("/users/<int:user_id>/delist", methods=["POST"])
@access_control.require_admin
def delist_user(user_id):
    """
    Delist user - permanently remove from whitelist
    Immediately forces user logout
    """
    data = request.get_json()
    reason = data.get("reason", "Not specified")

    db = get_admin_db()
    db_session = db.get_session()
    try:
        user = db_session.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.is_super_admin():
            return jsonify({"error": "Cannot delist super admin"}), 403

        # Delist user
        admin_email = session.get("email", "system")
        user.status = UserStatus.DELISTED
        user.force_logout = True  # Force immediate logout
        user.notes = f"Delisted by {admin_email} on {datetime.utcnow().isoformat()}. Reason: {reason}"

        db_session.commit()

        # Log activity
        AccessControl.log_activity(
            admin_email,
            "delist_user",
            resource=user.email,
            success=True,
            details={"reason": reason},
        )

        return jsonify(
            {
                "success": True,
                "message": f"User {user.email} delisted. Access immediately revoked.",
                "user": user.to_dict(),
            }
        ), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


@admin_bp.route("/users/<int:user_id>/suspend", methods=["POST"])
@access_control.require_admin
def suspend_user(user_id):
    """Temporarily suspend user"""
    data = request.get_json()
    reason = data.get("reason", "Not specified")

    db = get_admin_db()
    db_session = db.get_session()
    try:
        user = db_session.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.is_super_admin():
            return jsonify({"error": "Cannot suspend super admin"}), 403

        user.status = UserStatus.SUSPENDED
        user.force_logout = True
        user.notes = f"Suspended: {reason}"

        db_session.commit()

        admin_email = session.get("email", "system")
        AccessControl.log_activity(
            admin_email,
            "suspend_user",
            resource=user.email,
            success=True,
            details={"reason": reason},
        )

        return jsonify(
            {
                "success": True,
                "message": f"User {user.email} suspended",
                "user": user.to_dict(),
            }
        ), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


@admin_bp.route("/users/<int:user_id>/reactivate", methods=["POST"])
@access_control.require_admin
def reactivate_user(user_id):
    """Reactivate suspended user"""
    db = get_admin_db()
    db_session = db.get_session()
    try:
        user = db_session.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.status == UserStatus.DELISTED:
            return jsonify(
                {"error": "Cannot reactivate delisted user. Create new account."}
            ), 403

        user.status = UserStatus.APPROVED
        user.force_logout = False

        db_session.commit()

        admin_email = session.get("email", "system")
        AccessControl.log_activity(
            admin_email, "reactivate_user", resource=user.email, success=True
        )

        return jsonify(
            {
                "success": True,
                "message": f"User {user.email} reactivated",
                "user": user.to_dict(),
            }
        ), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


# ============================================================================
# Access Policies Management
# ============================================================================


@admin_bp.route("/users/<int:user_id>/policies", methods=["GET", "POST"])
@access_control.require_admin
def manage_user_policies(user_id):
    """Get or create access policies for user"""
    db = get_admin_db()
    db_session = db.get_session()

    try:
        user = db_session.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if request.method == "GET":
            # Get all policies
            policies = [p.to_dict() for p in user.access_policies]
            return jsonify({"policies": policies}), 200

        # POST - Create new policy
        data = request.get_json()

        policy = UserAccessPolicy(
            user_id=user_id,
            access_level=AccessLevel[data["access_level"].upper()],
            access_values=data["access_values"],
            can_view_data=data.get("can_view_data", True),
            can_upload_files=data.get("can_upload_files", False),
            can_use_data_catalogue=data.get("can_use_data_catalogue", False),
            can_export_data=data.get("can_export_data", False),
            can_view_analytics=data.get("can_view_analytics", True),
            valid_from=datetime.fromisoformat(data["valid_from"])
            if data.get("valid_from")
            else None,
            valid_until=datetime.fromisoformat(data["valid_until"])
            if data.get("valid_until")
            else None,
            created_by=session.get("email", "system"),
            notes=data.get("notes"),
        )

        db_session.add(policy)
        db_session.commit()

        AccessControl.log_activity(
            session.get("email", "system"),
            "create_access_policy",
            resource=user.email,
            success=True,
            details={"policy_id": policy.id},
        )

        return jsonify(
            {
                "success": True,
                "message": "Access policy created",
                "policy": policy.to_dict(),
            }
        ), 201
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


@admin_bp.route("/policies/<int:policy_id>", methods=["DELETE"])
@access_control.require_admin
def delete_policy(policy_id):
    """Delete access policy"""
    db = get_admin_db()
    db_session = db.get_session()
    try:
        policy = (
            db_session.query(UserAccessPolicy)
            .filter(UserAccessPolicy.id == policy_id)
            .first()
        )
        if not policy:
            return jsonify({"error": "Policy not found"}), 404

        user_email = policy.user.email
        db_session.delete(policy)
        db_session.commit()

        AccessControl.log_activity(
            session.get("email", "system"),
            "delete_access_policy",
            resource=user_email,
            success=True,
            details={"policy_id": policy_id},
        )

        return jsonify({"success": True, "message": "Policy deleted"}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


# ============================================================================
# Activity Logs
# ============================================================================


@admin_bp.route("/logs", methods=["GET"])
@access_control.require_admin
def get_activity_logs():
    """Get activity logs"""
    from .models import UserActivityLog

    db = get_admin_db()
    db_session = db.get_session()
    try:
        limit = int(request.args.get("limit", 100))
        user_email = request.args.get("user_email", "")
        action = request.args.get("action", "")

        query = db_session.query(UserActivityLog)

        if user_email:
            query = query.filter(UserActivityLog.user_email.like(f"%{user_email}%"))
        if action:
            query = query.filter(UserActivityLog.action == action)

        logs = query.order_by(UserActivityLog.timestamp.desc()).limit(limit).all()

        return jsonify(
            {"logs": [log.to_dict() for log in logs], "count": len(logs)}
        ), 200
    finally:
        db_session.close()


# ============================================================================
# Initialization
# ============================================================================


def init_admin_routes(app):
    """Initialize admin routes"""
    app.register_blueprint(admin_bp)
    print("✓ Admin Panel routes registered at /admin")
