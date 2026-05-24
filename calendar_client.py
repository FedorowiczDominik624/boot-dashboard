from pathlib import Path
import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

SCRIPT_DIR = Path(__file__).parent
CREDENTIALS_FILE = SCRIPT_DIR / "credentials.json"
TOKEN_FILE = SCRIPT_DIR / "token.json"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_credentials() -> Credentials:
    """Return valid Google Calendar credentials, refreshing or running OAuth as needed"""
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                sys.exit(
                    f"ERROR: {CREDENTIALS_FILE}  not found \n"
                    "Complete the Google Console Setup located at the top of page\n"
                    "and place credentials.json in this file"
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return creds

def get_todays_events() -> list[dict]:
    """Return today's events from the primary Google Calendar

    Each dict has shape:
        {"Start": "16:00", "end": "1800", 'summary': "Python Study"}

    All-day events use the string "all-day" for both start and end.
    Return an empty list if no events today.
    """
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    today_start = datetime.now(jst).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    today_start_iso = today_start.isoformat()
    today_end_iso = today_end.isoformat()

    result = service.events().list(
        calendarId="primary",
        timeMin=today_start_iso,
        timeMax=today_end_iso,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = []

    for event in result["items"]:
        start_field = event["start"]
        if start_field.get("dateTime"):
            start = start_field["dateTime"][11:16]
        else:
            start = "all-day"
        end_field = event["end"]
        if end_field.get("dateTime"):
            end = end_field["dateTime"][11:16]
        else:
            end = "all-day"
        summary = event.get("summary", "(no title)")
        events.append({"start": start, "end": end, "summary": summary})
    return events


    #print(result)

if __name__ == "__main__":
    print(get_todays_events())
    