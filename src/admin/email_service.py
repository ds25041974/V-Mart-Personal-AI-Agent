"""
Email Verification Service
Handles email verification tokens and sending verification emails
"""

import os
import secrets
import smtplib
import string
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .database import get_admin_db
from .models import EmailVerification, User, UserStatus


class EmailService:
    """Email service for verification and notifications"""

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@vmart.co.in")
        self.base_url = os.getenv("BASE_URL", "http://localhost:8000")

    def generate_verification_token(self):
        """Generate secure verification token"""
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(64))

    def create_verification_token(self, email, ip_address=None):
        """Create verification token for email"""
        db = get_admin_db()
        session = db.get_session()
        try:
            # Generate token
            token = self.generate_verification_token()

            # Create verification record
            verification = EmailVerification(
                email=email,
                token=token,
                expires_at=datetime.utcnow() + timedelta(hours=24),
                ip_address=ip_address,
            )
            session.add(verification)
            session.commit()

            return token
        except Exception as e:
            session.rollback()
            print(f"Error creating verification token: {str(e)}")
            return None
        finally:
            session.close()

    def verify_token(self, token):
        """Verify email token"""
        db = get_admin_db()
        session = db.get_session()
        try:
            verification = (
                session.query(EmailVerification)
                .filter(EmailVerification.token == token)
                .first()
            )

            if not verification:
                return {"success": False, "error": "Invalid token"}

            if verification.verified:
                return {"success": False, "error": "Token already used"}

            if verification.is_expired():
                return {"success": False, "error": "Token expired"}

            # Mark as verified
            verification.verified = True
            verification.verified_at = datetime.utcnow()

            # Update user status
            user = session.query(User).filter(User.email == verification.email).first()
            if user:
                user.email_verified = True
                user.verified_at = datetime.utcnow()
                if user.status == UserStatus.PENDING:
                    user.status = UserStatus.VERIFIED

            session.commit()

            return {
                "success": True,
                "email": verification.email,
                "message": "Email verified successfully. Awaiting admin approval.",
            }
        except Exception as e:
            session.rollback()
            return {"success": False, "error": str(e)}
        finally:
            session.close()

    def send_verification_email(self, email, token):
        """Send verification email"""
        if not self.smtp_user or not self.smtp_password:
            print("⚠️ SMTP not configured. Verification email not sent.")
            print(
                f"Verification link: {self.base_url}/admin/verify-email?token={token}"
            )
            return False

        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "V-Mart AI Agent - Verify Your Email"
            msg["From"] = self.from_email
            msg["To"] = email

            verification_link = f"{self.base_url}/admin/verify-email?token={token}"

            # HTML content
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2563eb;">V-Mart Personal AI Agent</h2>
                        <h3>Email Verification Required</h3>
                        <p>Thank you for registering with V-Mart AI Agent.</p>
                        <p>Please click the button below to verify your email address:</p>
                        <div style="margin: 30px 0;">
                            <a href="{verification_link}" 
                               style="background-color: #2563eb; 
                                      color: white; 
                                      padding: 12px 30px; 
                                      text-decoration: none; 
                                      border-radius: 5px;
                                      display: inline-block;">
                                Verify Email
                            </a>
                        </div>
                        <p>Or copy and paste this link in your browser:</p>
                        <p style="background-color: #f3f4f6; padding: 10px; border-radius: 5px; word-break: break-all;">
                            {verification_link}
                        </p>
                        <p><strong>Note:</strong> This link will expire in 24 hours.</p>
                        <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">
                        <p style="color: #6b7280; font-size: 12px;">
                            If you didn't request this verification, please ignore this email.
                        </p>
                    </div>
                </body>
            </html>
            """

            # Plain text fallback
            text = f"""
            V-Mart Personal AI Agent
            
            Email Verification Required
            
            Thank you for registering with V-Mart AI Agent.
            
            Please verify your email by clicking this link:
            {verification_link}
            
            This link will expire in 24 hours.
            
            If you didn't request this verification, please ignore this email.
            """

            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            msg.attach(part1)
            msg.attach(part2)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.from_email, email, msg.as_string())

            print(f"✓ Verification email sent to {email}")
            return True
        except Exception as e:
            print(f"❌ Error sending verification email: {str(e)}")
            return False

    def send_approval_notification(self, email):
        """Send email when account is approved"""
        if not self.smtp_user:
            print(f"Account approved for {email}. Login at: {self.base_url}")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "V-Mart AI Agent - Account Approved"
            msg["From"] = self.from_email
            msg["To"] = email

            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #10b981;">Account Approved!</h2>
                        <p>Great news! Your V-Mart AI Agent account has been approved.</p>
                        <p>You can now login and start using the AI chatbot:</p>
                        <div style="margin: 30px 0;">
                            <a href="{self.base_url}" 
                               style="background-color: #10b981; 
                                      color: white; 
                                      padding: 12px 30px; 
                                      text-decoration: none; 
                                      border-radius: 5px;
                                      display: inline-block;">
                                Login Now
                            </a>
                        </div>
                    </div>
                </body>
            </html>
            """

            msg.attach(MIMEText(html, "html"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.from_email, email, msg.as_string())

            print(f"✓ Approval notification sent to {email}")
            return True
        except Exception as e:
            print(f"❌ Error sending approval notification: {str(e)}")
            return False

    def send_rejection_notification(self, email, reason=None):
        """Send email when account is rejected"""
        if not self.smtp_user:
            print(f"Account rejected for {email}. Reason: {reason}")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "V-Mart AI Agent - Account Status"
            msg["From"] = self.from_email
            msg["To"] = email

            reason_text = f"<p><strong>Reason:</strong> {reason}</p>" if reason else ""

            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #dc2626;">Account Status Update</h2>
                        <p>We regret to inform you that your V-Mart AI Agent account request has been declined.</p>
                        {reason_text}
                        <p>If you believe this is an error, please contact your administrator.</p>
                    </div>
                </body>
            </html>
            """

            msg.attach(MIMEText(html, "html"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.from_email, email, msg.as_string())

            print(f"✓ Rejection notification sent to {email}")
            return True
        except Exception as e:
            print(f"❌ Error sending rejection notification: {str(e)}")
            return False


# Global email service instance
email_service = EmailService()
