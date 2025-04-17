import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.ai import generate_persona, generate_image, generate_tts
from app.video import generate_video

app = FastAPI(
    title="AI Avatar Video API",
    version="0.1.0",
    description="Generate AI personas, avatars, speech, and talking avatar videos."
)

# CORS middleware
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health():
    return {"message": "AI Avatar API is running"}


class PersonaRequest(BaseModel):
    name: str
    background: str


class PersonaResponse(BaseModel):
    persona_id: str
    description: str


@app.post("/api/persona", response_model=PersonaResponse)
async def create_persona(req: PersonaRequest):
    try:
        pid, desc = generate_persona(req.name, req.background)
        return PersonaResponse(persona_id=pid, description=desc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ImageRequest(BaseModel):
    prompt: str
    persona_id: str = ""


class ImageResponse(BaseModel):
    image_url: str


@app.post("/api/avatar/image", response_model=ImageResponse)
async def create_image(req: ImageRequest):
    try:
        url = generate_image(req.prompt, req.persona_id)
        return ImageResponse(image_url=url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TTSRequest(BaseModel):
    text: str
    voice: str = "default"


class TTSResponse(BaseModel):
    audio_url: str


@app.post("/api/tts", response_model=TTSResponse)
async def tts_speak(req: TTSRequest):
    try:
        url = generate_tts(req.text, req.voice)
        return TTSResponse(audio_url=url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class VideoRequest(BaseModel):
    persona_id: str
    text: str
    voice: str = "default"


class VideoResponse(BaseModel):
    video_url: str


@app.post("/api/avatar/video", response_model=VideoResponse)
async def avatar_video(req: VideoRequest):
    try:
        url = generate_video(req.persona_id, req.text, req.voice)
        return VideoResponse(video_url=url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))