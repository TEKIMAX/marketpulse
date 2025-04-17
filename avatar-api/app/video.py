import os
import requests


def generate_video(persona_id: str, text: str, voice: str = "default"):
    """
    Generate a talking avatar video via external video API.
    """
    video_url = os.getenv("VIDEO_API_URL")
    video_key = os.getenv("VIDEO_API_KEY")
    if not video_url:
        raise RuntimeError("VIDEO_API_URL is not set")
    headers = {"Authorization": f"Bearer {video_key}"} if video_key else {}
    payload = {"persona_id": persona_id, "text": text, "voice": voice}
    resp = requests.post(video_url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data.get("video_url", "")