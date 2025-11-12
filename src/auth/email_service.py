"""
Email Service for V-Mart Personal AI Agent
Sends verification, password reset, and notification emails

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional


class EmailService:
    """Handles sending emails for authentication and notifications"""

    def __init__(self):
        """Initialize email service with SMTP configuration"""
        # SMTP Configuration from environment variables
        self.smtp_server = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("EMAIL_PORT", "587"))
        self.smtp_username = os.environ.get("EMAIL_USERNAME", "")
        self.smtp_password = os.environ.get("EMAIL_PASSWORD", "")
        self.from_email = os.environ.get("EMAIL_FROM_ADDRESS", self.smtp_username)
        self.from_name = os.environ.get("EMAIL_FROM_NAME", "V-Mart AI Agent")

        # Check if email is configured
        self.is_configured = bool(self.smtp_username and self.smtp_password)

        if not self.is_configured:
            print(
                "⚠️  Email service not configured. Set SMTP_USERNAME and SMTP_PASSWORD in environment variables."
            )

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
    ) -> bool:
        """
        Send an email

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_body: HTML email body
            text_body: Plain text email body (fallback)

        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.is_configured:
            print("❌ Email service not configured")
            return False

        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email
            msg["Subject"] = subject

            # Add text and HTML parts
            if text_body:
                part1 = MIMEText(text_body, "plain")
                msg.attach(part1)

            part2 = MIMEText(html_body, "html")
            msg.attach(part2)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            print(f"✅ Email sent successfully to {to_email}")
            return True

        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
            return False

    def send_verification_email(
        self, to_email: str, full_name: str, verification_link: str
    ) -> bool:
        """
        Send email verification link

        Args:
            to_email: User's email
            full_name: User's full name
            verification_link: Verification URL

        Returns:
            True if sent successfully
        """
        subject = "Verify Your V-Mart AI Agent Account"

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .button {{
                    display: inline-block;
                    padding: 15px 30px;
                    background: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 12px;
                }}
                .warning {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏪 V-Mart Personal AI Agent</h1>
                    <p>Welcome to Your AI-Powered Retail Intelligence Platform</p>
                </div>
                <div class="content">
                    <h2>Hi {full_name}!</h2>
                    <p>Thank you for signing up for V-Mart Personal AI Agent. To complete your registration and start accessing our AI-powered retail intelligence features, please verify your email address.</p>
                    
                    <p style="text-align: center;">
                        <a href="{verification_link}" class="button">Verify Email Address</a>
                    </p>
                    
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #667eea;">{verification_link}</p>
                    
                    <div class="warning">
                        <strong>⚠️ Security Note:</strong> This verification link will expire in 24 hours. If you didn't create an account with V-Mart AI Agent, please ignore this email.
                    </div>
                    
                    <h3>What You Can Do With V-Mart AI Agent:</h3>
                    <ul>
                        <li>📊 Real-time sales analytics and insights</li>
                        <li>📈 Inventory planning and forecasting</li>
                        <li>👥 Customer behavior analysis</li>
                        <li>🎯 Personalized business recommendations</li>
                        <li>🌤️ Weather-based demand predictions</li>
                        <li>🎉 Festival and seasonal planning</li>
                        <li>📁 Multi-file data analysis</li>
                    </ul>
                    
                    <p>If you have any questions, our support team is here to help!</p>
                    
                    <p>Best regards,<br>
                    <strong>V-Mart AI Agent Team</strong></p>
                </div>
                <div class="footer">
                    <p>Developed by DSR | Inspired by LA | Powered by Gemini AI</p>
                    <p>This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_body = f"""
        Hi {full_name}!
        
        Thank you for signing up for V-Mart Personal AI Agent.
        
        Please verify your email address by clicking this link:
        {verification_link}
        
        This link will expire in 24 hours.
        
        If you didn't create an account, please ignore this email.
        
        Best regards,
        V-Mart AI Agent Team
        """

        return self.send_email(to_email, subject, html_body, text_body)

    def send_password_reset_email(
        self, to_email: str, full_name: str, reset_link: str
    ) -> bool:
        """
        Send password reset link

        Args:
            to_email: User's email
            full_name: User's full name
            reset_link: Password reset URL

        Returns:
            True if sent successfully
        """
        subject = "Reset Your V-Mart AI Agent Password"

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .button {{
                    display: inline-block;
                    padding: 15px 30px;
                    background: #dc3545;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 12px;
                }}
                .warning {{
                    background: #f8d7da;
                    border-left: 4px solid #dc3545;
                    padding: 15px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Password Reset Request</h1>
                    <p>V-Mart Personal AI Agent</p>
                </div>
                <div class="content">
                    <h2>Hi {full_name}!</h2>
                    <p>We received a request to reset your password for your V-Mart AI Agent account. Click the button below to set a new password:</p>
                    
                    <p style="text-align: center;">
                        <a href="{reset_link}" class="button">Reset Password</a>
                    </p>
                    
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #dc3545;">{reset_link}</p>
                    
                    <div class="warning">
                        <strong>⚠️ Security Alert:</strong>
                        <ul>
                            <li>This password reset link will expire in 1 hour</li>
                            <li>If you didn't request this reset, please ignore this email and your password will remain unchanged</li>
                            <li>Never share your password with anyone</li>
                            <li>V-Mart will never ask you for your password via email</li>
                        </ul>
                    </div>
                    
                    <p>If you continue to have issues accessing your account, please contact our support team.</p>
                    
                    <p>Best regards,<br>
                    <strong>V-Mart AI Agent Team</strong></p>
                </div>
                <div class="footer">
                    <p>Developed by DSR | Inspired by LA | Powered by Gemini AI</p>
                    <p>This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_body = f"""
        Hi {full_name}!
        
        We received a request to reset your password for your V-Mart AI Agent account.
        
        Click this link to reset your password:
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you didn't request this reset, please ignore this email.
        
        Best regards,
        V-Mart AI Agent Team
        """

        return self.send_email(to_email, subject, html_body, text_body)

    def send_welcome_email(self, to_email: str, full_name: str) -> bool:
        """
        Send welcome email after successful verification

        Args:
            to_email: User's email
            full_name: User's full name

        Returns:
            True if sent successfully
        """
        subject = "Welcome to V-Mart Personal AI Agent!"

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .feature {{
                    background: white;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid #667eea;
                    border-radius: 5px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Welcome to V-Mart AI Agent!</h1>
                    <p>Your AI-Powered Retail Intelligence Platform</p>
                </div>
                <div class="content">
                    <h2>Hi {full_name}!</h2>
                    <p>Your account has been successfully verified! You're now ready to harness the power of AI-driven retail intelligence.</p>
                    
                    <h3>🚀 Getting Started:</h3>
                    
                    <div class="feature">
                        <h4>💬 Chat with Your AI Assistant</h4>
                        <p>Ask questions about sales, inventory, customer trends, or get personalized business recommendations.</p>
                    </div>
                    
                    <div class="feature">
                        <h4>📊 Upload & Analyze Data</h4>
                        <p>Upload CSV files, Excel sheets, or PDFs for instant AI-powered insights and cross-reference analysis.</p>
                    </div>
                    
                    <div class="feature">
                        <h4>🗂️ Configure Data Paths</h4>
                        <p>Set up local file paths for automatic data access and real-time analysis.</p>
                    </div>
                    
                    <div class="feature">
                        <h4>🎯 Decision Support</h4>
                        <p>Get AI-driven recommendations for inventory planning, pricing strategies, and promotional activities.</p>
                    </div>
                    
                    <h3>📚 Quick Tips:</h3>
                    <ul>
                        <li>Start with simple questions to understand your data</li>
                        <li>Upload multiple related files for cross-reference insights</li>
                        <li>Use the export feature to save your analysis</li>
                        <li>Explore all tabs to discover powerful features</li>
                    </ul>
                    
                    <p><strong>Need Help?</strong> Check our documentation or contact support anytime!</p>
                    
                    <p>Happy analyzing!<br>
                    <strong>V-Mart AI Agent Team</strong></p>
                </div>
                <div class="footer">
                    <p>Developed by DSR | Inspired by LA | Powered by Gemini AI</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_body = f"""
        Welcome to V-Mart AI Agent, {full_name}!
        
        Your account has been successfully verified!
        
        Getting Started:
        - Chat with your AI assistant
        - Upload and analyze data files
        - Configure data paths
        - Get AI-driven decision support
        
        Happy analyzing!
        V-Mart AI Agent Team
        """

        return self.send_email(to_email, subject, html_body, text_body)
