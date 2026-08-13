"""
Fetch unread emails using the Gmail API.

Setup:
1. pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
2. Go to https://console.cloud.google.com/ → create a project → enable Gmail API
3. Create OAuth 2.0 credentials (Desktop app) → download as credentials.json
4. Place credentials.json in the same directory as this script
"""

import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDENTIALS_FILE = "client_secret.json"
TOKEN_FILE = "token.json"


def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def get_body(payload):
    """Extract plain text body from message payload."""
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")
    return "(no plain text body)"


def fetch_unread_emails(max_results=10):
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        q="is:unread",
        maxResults=max_results,
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        print("No unread emails found.")
        return

    print(f"Found {len(messages)} unread email(s):\n")
    print("=" * 60)

    for msg_ref in messages:
        msg = service.users().messages().get(
            userId="me",
            id=msg_ref["id"],
            format="full",
        ).execute()

        headers = msg["payload"].get("headers", [])
        subject = get_header(headers, "Subject")
        sender  = get_header(headers, "From")
        date    = get_header(headers, "Date")
        body    = get_body(msg["payload"])

        print(f"From:    {sender}")
        print(f"Date:    {date}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body[:500]}{'...' if len(body) > 500 else ''}")
        print("=" * 60)


if __name__ == "__main__":
    fetch_unread_emails(max_results=10)
