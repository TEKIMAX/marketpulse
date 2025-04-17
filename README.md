# AI Avatar Video API

An open-source FastAPI service to generate AI personas, avatar images, speech audio, and talking avatar videos (similar to Synthesia).

## Features
- Generate persona descriptions via OpenAI
- Create avatar images via Stable Diffusion
- Produce speech audio via a TTS service
- Generate lip-synced avatar videos via an external video API

## Quickstart
```bash
# Clone the repo
git clone <repo-url>
cd avatar-api

# Copy example env and set your keys
cp .env.example .env
nano .env

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Configuration
Create a `.env` file (see `.env.example`):
```env
OPENAI_API_KEY=your_openai_api_key
STABLE_DIFFUSION_URL=https://your.sd.endpoint
STABLE_DIFFUSION_API_KEY=your_sd_api_key
TTS_API_URL=https://your.tts.endpoint
TTS_API_KEY=your_tts_api_key
VIDEO_API_URL=https://your.video.service/api/generate
VIDEO_API_KEY=your_video_service_key
```

## API Endpoints

### Health Check
- **GET /**  
- Response: `{ "message": "AI Avatar API is running" }`

### Generate Persona
- **POST /api/persona**  
- **Body:** `{ "name": "Alice", "background": "AI researcher" }`  
- **Response:** `{ "persona_id": "uuid", "description": "..." }`

### Generate Avatar Image
- **POST /api/avatar/image**  
- **Body:** `{ "prompt": "Portrait of a friendly AI avatar", "persona_id": "uuid" }`  
- **Response:** `{ "image_url": "https://..." }`

### Generate Speech Audio
- **POST /api/tts**  
- **Body:** `{ "text": "Hello, I'm your AI avatar!", "voice": "default" }`  
- **Response:** `{ "audio_url": "https://..." }`

### Generate Avatar Video
- **POST /api/avatar/video**  
- **Body:** `{ "persona_id": "uuid", "text": "Welcome to our demo", "voice": "default" }`  
- **Response:** `{ "video_url": "https://..." }`

## Troubleshooting
- Ensure all environment variables are set correctly.  
- Check external service URLs and API keys.  

## License
MIT