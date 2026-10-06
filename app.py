import os
import uuid
import threading
import json
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.config import (
    BASE_DIR,
    NICHES,
    VOICE_PRESETS,
    VISUAL_STYLES,
    GEMINI_API_KEY,
    YOUTUBE_CLIENT_SECRETS_FILE
)
from src.utils import OUTPUT_DIR, get_ffmpeg_path
from src.pipeline import run_full_pipeline, _load_history
from src.publisher import upload_to_youtube, PRIVACY_STATUS

app = FastAPI(title="AutoShorts AI - Autonomous Faceless YouTube Engine")

# Mount static and templates
STATIC_DIR = BASE_DIR / "web" / "static"
TEMPLATES_DIR = BASE_DIR / "web" / "templates"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# In-memory job progress tracking
JOBS: Dict[str, Dict[str, Any]] = {}

class GenerateRequest(BaseModel):
    niche: str = "Psychology Facts"
    prompt: Optional[str] = ""
    voice: str = "en-US-ChristopherNeural"
    visual_style: str = "cinematic_dark"
    auto_upload: bool = False

class GeminiSettingsRequest(BaseModel):
    api_key: str


@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "niches": NICHES,
            "voices": VOICE_PRESETS,
            "styles": VISUAL_STYLES
        }
    )


@app.get("/api/status")
async def get_system_status():
    ffmpeg_exe = get_ffmpeg_path()
    secrets_file = BASE_DIR / YOUTUBE_CLIENT_SECRETS_FILE
    return {
        "ffmpeg_ready": bool(ffmpeg_exe and os.path.exists(ffmpeg_exe) or ffmpeg_exe == "ffmpeg"),
        "ffmpeg_path": ffmpeg_exe,
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY", "").strip()),
        "youtube_configured": secrets_file.exists()
    }


def _run_pipeline_worker(job_id: str, req: GenerateRequest):
    def update_cb(msg: str, pct: int):
        if job_id in JOBS:
            JOBS[job_id]["message"] = msg
            JOBS[job_id]["percentage"] = pct

    try:
        JOBS[job_id]["status"] = "running"
        record = run_full_pipeline(
            niche=req.niche,
            prompt=req.prompt or "",
            voice=req.voice,
            visual_style=req.visual_style,
            auto_upload=req.auto_upload,
            progress_callback=update_cb
        )
        JOBS[job_id]["status"] = "completed"
        JOBS[job_id]["percentage"] = 100
        JOBS[job_id]["message"] = "Video generation complete!"
        JOBS[job_id]["result"] = record
    except Exception as e:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["message"] = f"Pipeline execution error: {str(e)}"
        print(f"[Worker Error] {e}")


@app.post("/api/generate")
async def start_generation(req: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())[:8]
    JOBS[job_id] = {
        "status": "queued",
        "message": "Initializing generator...",
        "percentage": 5,
        "result": None
    }
    background_tasks.add_task(_run_pipeline_worker, job_id, req)
    return {"job_id": job_id, "status": "started"}


@app.get("/api/progress/{job_id}")
async def get_job_progress(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="Job not found")
    return JOBS[job_id]


@app.get("/api/gallery")
async def get_gallery():
    history = _load_history()
    return history


@app.get("/api/video/{filename}")
async def stream_video(filename: str):
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")
    return FileResponse(path=str(file_path), media_type="video/mp4", filename=filename)


@app.post("/api/settings/gemini")
async def save_gemini_key(req: GeminiSettingsRequest):
    key = req.api_key.strip()
    os.environ["GEMINI_API_KEY"] = key
    
    # Update .env file
    env_file = BASE_DIR / ".env"
    lines = []
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    
    key_written = False
    new_lines = []
    for line in lines:
        if line.startswith("GEMINI_API_KEY="):
            new_lines.append(f"GEMINI_API_KEY={key}\n")
            key_written = True
        else:
            new_lines.append(line)
            
    if not key_written:
        new_lines.append(f"GEMINI_API_KEY={key}\n")
        
    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
        
    return {"success": True, "message": "Gemini API key saved to .env"}


@app.post("/api/upload/{record_id}")
async def trigger_upload(record_id: str):
    history = _load_history()
    target_item = next((item for item in history if item.get("id") == record_id), None)
    if not target_item:
        raise HTTPException(status_code=404, detail="Video record not found")
        
    res = upload_to_youtube(
        video_path=target_item["video_path"],
        title=target_item["title"],
        description=target_item.get("description", ""),
        tags=target_item.get("tags", []),
        privacy_status=PRIVACY_STATUS
    )
    return res


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
