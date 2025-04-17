import os
import uuid

import openai
import requests

# Initialize OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY", "")


def generate_persona(name: str, background: str):
    """
    Generate a persona description using OpenAI.
    Returns (persona_id, description).
    """
    prompt = (
        f"Create a detailed AI persona for a character named {name} "
        f"with the following background: {background}."
    )
    resp = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7,
    )
    description = resp.choices[0].text.strip()
    persona_id = str(uuid.uuid4())
    # TODO: Persist persona metadata if needed
    return persona_id, description


def generate_image(prompt: str, persona_id: str = ""):
    """
    Generate an avatar image via Stable Diffusion endpoint.
    """
    sd_url = os.getenv("STABLE_DIFFUSION_URL")
    sd_key = os.getenv("STABLE_DIFFUSION_API_KEY")
    if not sd_url:
        raise RuntimeError("STABLE_DIFFUSION_URL is not set")
    headers = {"Authorization": f"Bearer {sd_key}"} if sd_key else {}
    payload = {"prompt": prompt}
    resp = requests.post(sd_url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data.get("image_url", "")


def generate_tts(text: str, voice: str = "default"):
    """
    Generate speech audio via TTS service.
    """
    tts_url = os.getenv("TTS_API_URL")
    tts_key = os.getenv("TTS_API_KEY")
    if not tts_url:
        raise RuntimeError("TTS_API_URL is not set")
    headers = {"Authorization": f"Bearer {tts_key}"} if tts_key else {}
    payload = {"text": text, "voice": voice}
    resp = requests.post(tts_url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data.get("audio_url", "")