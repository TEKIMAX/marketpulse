import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.ai import run_codex
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI(
    title="MarketPulse API",
    description="API for MarketPulse, an on-demand local market analysis toolkit.",
    version="0.1.0"
)
# CORS middleware setup
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    prompt: str


class AnalyzeResponse(BaseModel):
    analysis: str


@app.get("/", summary="Health check")
async def root():
    return {"message": "MarketPulse API is running"}


@app.post("/api/ai/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Analyze a prompt using Codex CLI and return the result.
    """
    try:
        result = run_codex(request.prompt)
        return AnalyzeResponse(analysis=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))