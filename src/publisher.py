import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
from src.config import (
    BASE_DIR,
    YOUTUBE_CLIENT_SECRETS_FILE,
    YOUTUBE_TOKEN_FILE,
    PRIVACY_STATUS
)

def get_youtube_service():
    """
    Authenticates and returns YouTube Data API v3 service.
    Uses local token.json if cached, otherwise starts OAuth flow.
    """
    secrets_path = BASE_DIR / YOUTUBE_CLIENT_SECRETS_FILE
    token_path = BASE_DIR / YOUTUBE_TOKEN_FILE

    if not secrets_path.exists():
        return None

    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        creds = None

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(secrets_path), scopes)
                creds = flow.run_local_server(port=0)

            with open(token_path, "w") as token:
                token.write(creds.to_json())

        return build("youtube", "v3", credentials=creds)
    except Exception as e:
        print(f"[Publisher] YouTube Auth Notice: {e}")
        return None


def upload_to_youtube(
    video_path: str,
    title: str,
    description: str,
    tags: list,
    privacy_status: str = PRIVACY_STATUS,
    category_id: str = "27"  # 27 = Education, 28 = Science & Tech
) -> Dict[str, Any]:
    """
    Uploads video to YouTube via YouTube Data API v3.
    """
    if not os.path.isfile(video_path):
        return {"status": "error", "message": f"Video file not found at {video_path}"}

    youtube = get_youtube_service()
    if not youtube:
        return {
            "status": "ready_for_upload",
            "message": "Video is generated and ready! To enable direct auto-upload, place 'client_secrets.json' in your project root.",
            "video_path": video_path,
            "metadata": {
                "title": title,
                "description": description,
                "tags": tags,
                "privacy": privacy_status
            }
        }

    try:
        from googleapiclient.http import MediaFileUpload

        body = {
            "snippet": {
                "title": title[:100],
                "description": description[:5000],
                "tags": tags[:30],
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"[Publisher] Uploaded {int(status.progress() * 100)}%")

        video_id = response.get("id")
        video_url = f"https://youtube.com/shorts/{video_id}"
        print(f"[Publisher] Upload successful! URL: {video_url}")

        return {
            "status": "uploaded",
            "video_id": video_id,
            "url": video_url,
            "title": title
        }
    except Exception as e:
        print(f"[Publisher] Upload failed: {e}")
        return {"status": "error", "message": str(e), "video_path": video_path}
