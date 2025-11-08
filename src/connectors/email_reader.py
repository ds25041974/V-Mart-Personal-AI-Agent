"""
Email Reader
Reads email data from Gmail and Outlook including:
- Email subject, body, and headers
- Sender and recipients
- Attachments
- Labels/folders
- Read/unread status
"""

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import Dict, List, Optional, Any
import os
import pickle
import base64
import email
from email.mime.text import MIMEText


class EmailReader:
    """Read email data from Gmail"""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = credentials_path or 'credentials.json'
        self.creds = None
        self.service = None
        
    def authenticate(self) -> bool:
        """Authenticate with Gmail API"""
        token_path = 'token_gmail.pickle'
        
        # Load existing credentials
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)
        
        # Refresh or get new credentials
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    print(f"Credentials file not found: {self.credentials_path}")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)
        
        try:
            self.service = build('gmail', 'v1', credentials=self.creds)
            return True
        except Exception as e:
            print(f"Error building Gmail service: {e}")
            return False
    
    def get_recent_emails(self, max_results: int = 10, query: str = '') -> List[Dict[str, Any]]:
        """Get recent emails from Gmail"""
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            # Get list of messages
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results,
                q=query
            ).execute()
            
            messages = results.get('messages', [])
            
            emails = []
            for message in messages:
                email_data = self.get_email_details(message['id'])
                if email_data:
                    emails.append(email_data)
            
            return emails
        except HttpError as e:
            print(f"Error getting emails: {e}")
            return []
    
    def get_email_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific email"""
        if not self.service:
            return None
        
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            # Extract headers
            headers = message.get('payload', {}).get('headers', [])
            subject = self._get_header_value(headers, 'Subject')
            sender = self._get_header_value(headers, 'From')
            to = self._get_header_value(headers, 'To')
            cc = self._get_header_value(headers, 'Cc')
            date = self._get_header_value(headers, 'Date')
            
            # Extract body
            body = self._get_email_body(message.get('payload', {}))
            
            # Get snippet
            snippet = message.get('snippet', '')
            
            # Get labels
            labels = message.get('labelIds', [])
            
            # Get attachments
            attachments = self._get_attachments_info(message.get('payload', {}))
            
            return {
                'id': message_id,
                'thread_id': message.get('threadId'),
                'subject': subject,
                'from': sender,
                'to': to,
                'cc': cc,
                'date': date,
                'snippet': snippet,
                'body': body,
                'labels': labels,
                'attachments': attachments,
                'size_estimate': message.get('sizeEstimate'),
                'internal_date': message.get('internalDate')
            }
        except HttpError as e:
            print(f"Error getting email details: {e}")
            return None
    
    def _get_header_value(self, headers: List[Dict], name: str) -> str:
        """Extract header value by name"""
        for header in headers:
            if header.get('name', '').lower() == name.lower():
                return header.get('value', '')
        return ''
    
    def _get_email_body(self, payload: Dict) -> str:
        """Extract email body from payload"""
        body = ''
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    if 'data' in part.get('body', {}):
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
                elif part.get('mimeType') == 'text/html' and not body:
                    if 'data' in part.get('body', {}):
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        elif 'body' in payload and 'data' in payload['body']:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        return body
    
    def _get_attachments_info(self, payload: Dict) -> List[Dict[str, Any]]:
        """Get information about email attachments"""
        attachments = []
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('filename'):
                    attachments.append({
                        'filename': part['filename'],
                        'mime_type': part.get('mimeType'),
                        'size': part.get('body', {}).get('size', 0),
                        'attachment_id': part.get('body', {}).get('attachmentId')
                    })
        
        return attachments
    
    def search_emails(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search emails with a specific query"""
        return self.get_recent_emails(max_results=max_results, query=query)
    
    def get_unread_emails(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """Get unread emails"""
        return self.search_emails('is:unread', max_results=max_results)
    
    def get_starred_emails(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """Get starred emails"""
        return self.search_emails('is:starred', max_results=max_results)
    
    def get_emails_with_attachments(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """Get emails with attachments"""
        return self.search_emails('has:attachment', max_results=max_results)
    
    def get_labels(self) -> List[Dict[str, str]]:
        """Get all Gmail labels"""
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            
            return [{'id': label['id'], 'name': label['name']} for label in labels]
        except HttpError as e:
            print(f"Error getting labels: {e}")
            return []
