"""
Auto Emailer for V-Mart Personal AI Agent
"""

import json
import os
from datetime import datetime
from typing import List, Optional


class AutoEmailer:
    def __init__(self, gmail_connector, config_file: str = "email_templates.json"):
        """
        Initializes the Auto Emailer.

        Args:
            gmail_connector: Instance of GmailConnector
            config_file (str): Path to email templates configuration
        """
        self.gmail = gmail_connector
        self.config_file = config_file
        self.templates = self._load_templates()

    def _load_templates(self) -> dict:
        """
        Loads email templates from configuration file.

        Returns:
            Dictionary of email templates
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        return {}

    def _save_templates(self):
        """
        Saves email templates to configuration file.
        """
        with open(self.config_file, "w") as f:
            json.dump(self.templates, f, indent=2)

    def add_template(self, name: str, subject: str, body: str):
        """
        Adds an email template.

        Args:
            name (str): Template name
            subject (str): Email subject
            body (str): Email body template
        """
        self.templates[name] = {"subject": subject, "body": body}
        self._save_templates()

    def send_from_template(
        self,
        template_name: str,
        recipients: List[str],
        variables: Optional[dict] = None,
    ) -> List[dict]:
        """
        Sends emails using a template.

        Args:
            template_name (str): Name of the template to use
            recipients (List[str]): List of recipient email addresses
            variables (dict): Variables to replace in template

        Returns:
            List of send results
        """
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")

        template = self.templates[template_name]
        subject = template["subject"]
        body = template["body"]

        # Replace variables in template
        if variables:
            for key, value in variables.items():
                subject = subject.replace(f"{{{key}}}", str(value))
                body = body.replace(f"{{{key}}}", str(value))

        results = []
        for recipient in recipients:
            result = self.gmail.send_message(recipient, subject, body)
            results.append(
                {
                    "recipient": recipient,
                    "status": "sent" if result else "failed",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return results

    def send_bulk_email(
        self, recipients: List[str], subject: str, body: str, personalize: bool = False
    ) -> List[dict]:
        """
        Sends bulk emails to multiple recipients.

        Args:
            recipients (List[str]): List of recipient email addresses
            subject (str): Email subject
            body (str): Email body
            personalize (bool): Whether to personalize emails

        Returns:
            List of send results
        """
        results = []
        for recipient in recipients:
            email_body = body
            email_subject = subject

            if personalize:
                # Extract name from email for personalization
                name = recipient.split("@")[0].replace(".", " ").title()
                email_body = f"Dear {name},\n\n{body}"

            result = self.gmail.send_message(recipient, email_subject, email_body)
            results.append(
                {
                    "recipient": recipient,
                    "status": "sent" if result else "failed",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return results

    def schedule_email(
        self,
        scheduler,
        recipients: List[str],
        subject: str,
        body: str,
        schedule_time: str,
        schedule_type: str = "daily",
    ):
        """
        Schedules an email to be sent automatically.

        Args:
            scheduler: Instance of TaskScheduler
            recipients (List[str]): List of recipient email addresses
            subject (str): Email subject
            body (str): Email body
            schedule_time (str): Time to send (HH:MM format)
            schedule_type (str): Type of schedule (daily, weekly)
        """

        def send_scheduled():
            self.send_bulk_email(recipients, subject, body)

        if schedule_type == "daily":
            scheduler.add_daily_task(
                schedule_time, send_scheduled, name=f"email_{subject[:20]}"
            )

        return True
