"""
Email-based Authentication System for V-Mart Personal AI Agent
Handles signup, email verification, login, and password reset

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import hashlib
import os
import re
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.auth.auth_db_manager import AuthDatabaseManager
from src.auth.email_service import EmailService

email_auth_bp = Blueprint("email_auth", __name__)

# Email validation regex
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

# Password requirements
MIN_PASSWORD_LENGTH = 8
PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$"
)

# Allowed company domains (require email signup + verification)
ALLOWED_DOMAINS = [
    "vmart.co.in",
    "vmartretail.com",
    "limeroad.com",
]

# Anonymous login whitelist (no password required)
ANONYMOUS_LOGIN_EMAILS = [
    "ds.250474@gmail.com",
    "dinesh.srivastava@vmart.co.in",
    "dineshsrivastava07@gmail.com",
]


class EmailAuthManager:
    """Manages email-based authentication"""

    def __init__(self):
        """Initialize email auth manager"""
        self.email_service = EmailService()
        self.db_manager = AuthDatabaseManager()
        self._init_database()

    def _init_database(self):
        """Initialize database tables for email auth"""
        try:
            # Users table
            self.db_manager.execute_query("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    is_verified INTEGER DEFAULT 0,
                    verification_token TEXT,
                    verification_token_expires TIMESTAMP,
                    reset_token TEXT,
                    reset_token_expires TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active INTEGER DEFAULT 1,
                    role TEXT DEFAULT 'user',
                    profile_data TEXT
                )
            """)

            # Login attempts table (for security)
            self.db_manager.execute_query("""
                CREATE TABLE IF NOT EXISTS login_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    ip_address TEXT,
                    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success INTEGER DEFAULT 0
                )
            """)

            print("✅ Email authentication database tables initialized")
        except Exception as e:
            print(f"❌ Error initializing email auth database: {e}")

    def validate_email(self, email: str) -> Tuple[bool, str]:
        """
        Validate email format

        Args:
            email: Email address to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email or not email.strip():
            return False, "Email is required"

        email = email.strip().lower()

        if not EMAIL_REGEX.match(email):
            return False, "Invalid email format"

        # Extract domain from email
        domain = email.split("@")[1] if "@" in email else ""

        # Check if email is in anonymous login whitelist (allowed without restrictions)
        if email in ANONYMOUS_LOGIN_EMAILS:
            return True, ""

        # Check if domain is in allowed company domains
        if domain not in ALLOWED_DOMAINS:
            return (
                False,
                f"Only emails from {', '.join(ALLOWED_DOMAINS)} are allowed to signup.",
            )

        # Check for common disposable email domains
        disposable_domains = ["tempmail.com", "throwaway.email", "guerrillamail.com"]
        if domain in disposable_domains:
            return False, "Disposable email addresses are not allowed"

        return True, ""

    def validate_password(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password:
            return False, "Password is required"

        if len(password) < MIN_PASSWORD_LENGTH:
            return (
                False,
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters long",
            )

        if not PASSWORD_REGEX.match(password):
            return (
                False,
                "Password must contain: uppercase, lowercase, digit, and special character (@$!%*?&#)",
            )

        return True, ""

    def hash_password(self, password: str) -> str:
        """
        Hash password with salt

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        salt = os.urandom(32)
        pwdhash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return salt.hex() + pwdhash.hex()

    def verify_password(self, stored_password: str, provided_password: str) -> bool:
        """
        Verify password against stored hash

        Args:
            stored_password: Stored password hash
            provided_password: Password provided by user

        Returns:
            True if password matches, False otherwise
        """
        try:
            salt = bytes.fromhex(stored_password[:64])
            stored_hash = stored_password[64:]
            pwdhash = hashlib.pbkdf2_hmac(
                "sha256", provided_password.encode("utf-8"), salt, 100000
            )
            return pwdhash.hex() == stored_hash
        except Exception:
            return False

    def generate_verification_token(self) -> str:
        """Generate secure verification token"""
        return secrets.token_urlsafe(32)

    def signup(self, email: str, password: str, full_name: str) -> Tuple[bool, str]:
        """
        Register new user with email verification

        Args:
            email: User's email address
            password: User's password
            full_name: User's full name

        Returns:
            Tuple of (success, message)
        """
        # Validate email
        is_valid, error = self.validate_email(email)
        if not is_valid:
            return False, error

        email = email.strip().lower()

        # Validate password
        is_valid, error = self.validate_password(password)
        if not is_valid:
            return False, error

        # Validate full name
        if not full_name or len(full_name.strip()) < 2:
            return False, "Full name must be at least 2 characters"

        # Check if user already exists
        existing_user = self.db_manager.fetch_one(
            "SELECT id, is_verified FROM users WHERE email = ?", (email,)
        )

        if existing_user:
            if existing_user["is_verified"]:
                return False, "An account with this email already exists. Please login."
            else:
                # User exists but not verified - resend verification
                return self._resend_verification(email)

        # Hash password
        password_hash = self.hash_password(password)

        # Generate verification token
        verification_token = self.generate_verification_token()
        token_expires = datetime.now() + timedelta(hours=24)

        # Insert user into database
        try:
            self.db_manager.execute_query(
                """
                INSERT INTO users (email, password_hash, full_name, verification_token, verification_token_expires)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    email,
                    password_hash,
                    full_name.strip(),
                    verification_token,
                    token_expires,
                ),
            )

            # Send verification email
            verification_link = self._build_verification_link(verification_token)
            email_sent = self.email_service.send_verification_email(
                to_email=email, full_name=full_name, verification_link=verification_link
            )

            if email_sent:
                return (
                    True,
                    "Account created! Please check your email to verify your account.",
                )
            else:
                return (
                    True,
                    "Account created! However, verification email failed to send. Please contact support.",
                )

        except Exception as e:
            print(f"❌ Signup error: {e}")
            return False, "An error occurred during signup. Please try again."

    def verify_email(self, token: str) -> Tuple[bool, str]:
        """
        Verify user's email with token

        Args:
            token: Verification token

        Returns:
            Tuple of (success, message)
        """
        user = self.db_manager.fetch_one(
            "SELECT id, email, full_name, verification_token_expires FROM users WHERE verification_token = ?",
            (token,),
        )

        if not user:
            return False, "Invalid verification link"

        # Check if token expired
        if datetime.fromisoformat(user["verification_token_expires"]) < datetime.now():
            return False, "Verification link has expired. Please request a new one."

        # Update user as verified
        try:
            self.db_manager.execute_query(
                """
                UPDATE users 
                SET is_verified = 1, verification_token = NULL, verification_token_expires = NULL
                WHERE id = ?
                """,
                (user["id"],),
            )

            return True, "Email verified successfully! You can now login."
        except Exception as e:
            print(f"❌ Email verification error: {e}")
            return False, "An error occurred during verification. Please try again."

    def login(
        self,
        email: str,
        password: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Login user with email and password (or anonymous for whitelisted emails)

        Args:
            email: User's email
            password: User's password (optional for anonymous whitelisted emails)
            ip_address: User's IP address (for security logging)

        Returns:
            Tuple of (success, message, user_data)
        """
        email = email.strip().lower()

        # Check if anonymous login allowed (whitelisted emails)
        if email in ANONYMOUS_LOGIN_EMAILS:
            # Anonymous login - no password required
            user = self.db_manager.fetch_one(
                "SELECT * FROM users WHERE email = ?", (email,)
            )

            if not user:
                # Auto-create user for anonymous login emails
                try:
                    name = email.split("@")[0].replace(".", " ").title()
                    self.db_manager.execute_query(
                        """INSERT INTO users (email, password_hash, full_name, is_verified, role) 
                           VALUES (?, ?, ?, 1, 'admin')""",
                        (email, "ANONYMOUS_LOGIN", name),
                    )
                    user = self.db_manager.fetch_one(
                        "SELECT * FROM users WHERE email = ?", (email,)
                    )
                except Exception as e:
                    return False, f"Error creating anonymous user: {e}", None

            if not user:
                return False, "Failed to create anonymous user", None

            # Log successful anonymous login
            self._log_login_attempt(email, ip_address, success=True)

            # Update last login
            self.db_manager.execute_query(
                "UPDATE users SET last_login = ? WHERE id = ?",
                (datetime.now(), user["id"]),
            )

            user_data = {
                "id": user["id"],
                "email": user["email"],
                "name": user["full_name"],
                "role": user.get("role", "admin"),
                "verified": True,
                "anonymous": True,
            }

            return True, "Anonymous login successful!", user_data

        # Regular login flow (password required)
        if not password:
            return False, "Password is required", None

        # Check rate limiting (max 5 failed attempts in 15 minutes)
        recent_attempts = self.db_manager.fetch_all(
            """
            SELECT COUNT(*) as count FROM login_attempts 
            WHERE email = ? AND success = 0 AND attempt_time > datetime('now', '-15 minutes')
            """,
            (email,),
        )

        if recent_attempts and recent_attempts[0]["count"] >= 5:
            return (
                False,
                "Too many failed login attempts. Please try again in 15 minutes.",
                None,
            )

        # Fetch user
        user = self.db_manager.fetch_one(
            "SELECT * FROM users WHERE email = ?", (email,)
        )

        # Log attempt
        self._log_login_attempt(email, ip_address, success=False)

        if not user:
            return False, "Invalid email or password", None

        # Check if account is active
        if not user["is_active"]:
            return (
                False,
                "Your account has been deactivated. Please contact support.",
                None,
            )

        # Check if email is verified
        if not user["is_verified"]:
            return (
                False,
                "Please verify your email before logging in. Check your inbox for the verification link.",
                None,
            )

        # Verify password
        if not self.verify_password(user["password_hash"], password):
            return False, "Invalid email or password", None

        # Update last login
        self.db_manager.execute_query(
            "UPDATE users SET last_login = ? WHERE id = ?", (datetime.now(), user["id"])
        )

        # Log successful attempt
        self._log_login_attempt(email, ip_address, success=True)

        # Prepare user session data
        user_data = {
            "id": user["id"],
            "email": user["email"],
            "name": user["full_name"],
            "role": user["role"],
            "verified": True,
            "anonymous": False,
        }

        return True, "Login successful!", user_data

    def request_password_reset(self, email: str) -> Tuple[bool, str]:
        """
        Request password reset link

        Args:
            email: User's email

        Returns:
            Tuple of (success, message)
        """
        email = email.strip().lower()

        user = self.db_manager.fetch_one(
            "SELECT id, full_name FROM users WHERE email = ? AND is_verified = 1",
            (email,),
        )

        if not user:
            # Don't reveal if email exists or not (security)
            return (
                True,
                "If an account exists with this email, you will receive a password reset link.",
            )

        # Generate reset token
        reset_token = self.generate_verification_token()
        token_expires = datetime.now() + timedelta(hours=1)  # 1 hour expiry

        try:
            self.db_manager.execute_query(
                "UPDATE users SET reset_token = ?, reset_token_expires = ? WHERE id = ?",
                (reset_token, token_expires, user["id"]),
            )

            # Send reset email
            reset_link = self._build_reset_link(reset_token)
            self.email_service.send_password_reset_email(
                to_email=email, full_name=user["full_name"], reset_link=reset_link
            )

            return (
                True,
                "If an account exists with this email, you will receive a password reset link.",
            )
        except Exception as e:
            print(f"❌ Password reset request error: {e}")
            return False, "An error occurred. Please try again."

    def reset_password(self, token: str, new_password: str) -> Tuple[bool, str]:
        """
        Reset password with token

        Args:
            token: Reset token
            new_password: New password

        Returns:
            Tuple of (success, message)
        """
        # Validate new password
        is_valid, error = self.validate_password(new_password)
        if not is_valid:
            return False, error

        user = self.db_manager.fetch_one(
            "SELECT id, reset_token_expires FROM users WHERE reset_token = ?", (token,)
        )

        if not user:
            return False, "Invalid reset link"

        # Check if token expired
        if datetime.fromisoformat(user["reset_token_expires"]) < datetime.now():
            return False, "Reset link has expired. Please request a new one."

        # Hash new password
        password_hash = self.hash_password(new_password)

        try:
            self.db_manager.execute_query(
                """
                UPDATE users 
                SET password_hash = ?, reset_token = NULL, reset_token_expires = NULL
                WHERE id = ?
                """,
                (password_hash, user["id"]),
            )

            return (
                True,
                "Password reset successful! You can now login with your new password.",
            )
        except Exception as e:
            print(f"❌ Password reset error: {e}")
            return False, "An error occurred. Please try again."

    def _resend_verification(self, email: str) -> Tuple[bool, str]:
        """Resend verification email"""
        # Generate new token
        verification_token = self.generate_verification_token()
        token_expires = datetime.now() + timedelta(hours=24)

        user = self.db_manager.fetch_one(
            "SELECT id, full_name FROM users WHERE email = ?", (email,)
        )

        if not user:
            return False, "User not found"

        try:
            self.db_manager.execute_query(
                "UPDATE users SET verification_token = ?, verification_token_expires = ? WHERE email = ?",
                (verification_token, token_expires, email),
            )

            verification_link = self._build_verification_link(verification_token)
            self.email_service.send_verification_email(
                to_email=email,
                full_name=user["full_name"],
                verification_link=verification_link,
            )

            return True, "Verification email resent. Please check your inbox."
        except Exception as e:
            print(f"❌ Resend verification error: {e}")
            return False, "An error occurred. Please try again."

    def _log_login_attempt(self, email: str, ip_address: Optional[str], success: bool):
        """Log login attempt for security"""
        try:
            self.db_manager.execute_query(
                "INSERT INTO login_attempts (email, ip_address, success) VALUES (?, ?, ?)",
                (email, ip_address, 1 if success else 0),
            )
        except Exception as e:
            print(f"❌ Failed to log login attempt: {e}")

    def _build_verification_link(self, token: str) -> str:
        """Build email verification link"""
        base_url = os.environ.get("APP_BASE_URL", "http://localhost:8000")
        return f"{base_url}/verify-email?token={token}"

    def _build_reset_link(self, token: str) -> str:
        """Build password reset link"""
        base_url = os.environ.get("APP_BASE_URL", "http://localhost:8000")
        return f"{base_url}/reset-password?token={token}"


# Initialize manager
email_auth_manager = EmailAuthManager()


# ============================================
# FLASK ROUTES
# ============================================


@email_auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """Signup page"""
    if request.method == "GET":
        return render_template("signup.html")

    # POST request - process signup
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    confirm_password = request.form.get("confirm_password", "").strip()
    full_name = request.form.get("full_name", "").strip()

    # Validate passwords match
    if password != confirm_password:
        flash("Passwords do not match", "error")
        return render_template("signup.html"), 400

    # Process signup
    success, message = email_auth_manager.signup(email, password, full_name)

    if success:
        flash(message, "success")
        return redirect(url_for("email_auth.login"))
    else:
        flash(message, "error")
        return render_template("signup.html"), 400


@email_auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    if request.method == "GET":
        return render_template("login.html")

    # POST request - process login
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    ip_address = request.remote_addr

    success, message, user_data = email_auth_manager.login(email, password, ip_address)

    if success:
        session["user"] = user_data
        flash(message, "success")
        return redirect(url_for("index"))
    else:
        flash(message, "error")
        return render_template("login.html"), 401


@email_auth_bp.route("/verify-email")
def verify_email():
    """Email verification page"""
    token = request.args.get("token")

    if not token:
        flash("Invalid verification link", "error")
        return redirect(url_for("email_auth.login"))

    success, message = email_auth_manager.verify_email(token)

    flash(message, "success" if success else "error")
    return redirect(url_for("email_auth.login"))


@email_auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Forgot password page"""
    if request.method == "GET":
        return render_template("forgot_password.html")

    email = request.form.get("email", "").strip()
    success, message = email_auth_manager.request_password_reset(email)

    flash(message, "success" if success else "error")
    return render_template("forgot_password.html")


@email_auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    """Reset password page"""
    token = request.args.get("token")

    if not token:
        flash("Invalid reset link", "error")
        return redirect(url_for("email_auth.login"))

    if request.method == "GET":
        return render_template("reset_password.html", token=token)

    new_password = request.form.get("password", "").strip()
    confirm_password = request.form.get("confirm_password", "").strip()

    if new_password != confirm_password:
        flash("Passwords do not match", "error")
        return render_template("reset_password.html", token=token), 400

    success, message = email_auth_manager.reset_password(token, new_password)

    flash(message, "success" if success else "error")

    if success:
        return redirect(url_for("email_auth.login"))
    else:
        return render_template("reset_password.html", token=token), 400


@email_auth_bp.route("/logout")
def logout():
    """Logout user"""
    session.pop("user", None)
    flash("Logged out successfully", "success")
    return redirect(url_for("email_auth.login"))
