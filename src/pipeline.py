import os
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from src.config import (
    DEFAULT_NICHE,
    DEFAULT_VOICE,
    DEFAULT_VISUAL_STYLE,
    AUTO_UPLOAD_DEFAULT,
    PRIVACY_STATUS
)
from src.utils import OUTPUT_DIR, TEMP_DIR, sanitize_filename
from src.researcher import research_topic
from src.scriptwriter import generate_script
from src.voiceover import generate_voiceover
from src.visuals import generate_all_scene_images
from src.captions import generate_styled_ass_subtitles
from src.audio import mix_voice_and_music
from src.composer import compose_shorts_video
from src.publisher import upload_to_youtube

HISTORY_FILE = OUTPUT_DIR / "history.json"

def _load_history():
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def _save_history(record: Dict[str, Any]):
    history = _load_history()
    history.insert(0, record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def run_full_pipeline(
    niche: str = DEFAULT_NICHE,
    prompt: str = "",
    voice: str = DEFAULT_VOICE,
    visual_style: str = DEFAULT_VISUAL_STYLE,
    auto_upload: bool = AUTO_UPLOAD_DEFAULT,
    progress_callback: Optional[Callable[[str, int], None]] = None
) -> Dict[str, Any]:
    """
    Executes the entire end-to-end autonomous YouTube Shorts pipeline:
    Step 1: Topic Research & Trend Discovery
    Step 2: Scriptwriting & Visual Prompting + SEO Optimization
    Step 3: Neural Voiceover Synthesis
    Step 4: AI 9:16 Vertical Image Generation
    Step 5: Styled Dynamic Subtitles
    Step 6: Background Music Mixing
    Step 7: Video Assembly & Ken Burns Motion Rendering
    Step 8: YouTube Upload / Scheduling
    """
    session_id = f"short_{int(time.time())}"

    def notify(msg: str, pct: int):
        print(f"[{pct}%] {msg}")
        if progress_callback:
            progress_callback(msg, pct)

    notify("Step 1/8: Researching viral trending topic...", 10)
    topic_data = research_topic(niche=niche, user_prompt=prompt)

    notify("Step 2/8: Writing high-retention script & SEO metadata...", 25)
    script_data = generate_script(topic_data=topic_data, niche=niche, style_key=visual_style)

    notify("Step 3/8: Synthesizing neural voiceover...", 40)
    full_text = script_data.get("full_script", "")
    voice_res = generate_voiceover(
        text=full_text,
        voice=voice,
        filename_prefix=f"{session_id}_voice"
    )
    audio_path = voice_res["audio_path"]
    duration = voice_res["duration"]
    word_timings = voice_res["word_timings"]

    notify("Step 4/8: Generating AI 9:16 vertical scene visuals...", 55)
    scenes = script_data.get("scenes", [])
    image_paths = generate_all_scene_images(scenes, session_id=session_id)

    notify("Step 5/8: Crafting dynamic viral karaoke subtitles...", 70)
    sub_path = str(TEMP_DIR / f"{session_id}_subs.ass")
    generate_styled_ass_subtitles(word_timings, sub_path)

    notify("Step 6/8: Mixing background music with speech ducking...", 80)
    mixed_audio_path = str(TEMP_DIR / f"{session_id}_mixed.mp3")
    mix_voice_and_music(voiceover_path=audio_path, output_mixed_path=mixed_audio_path)

    notify("Step 7/8: Assembling video with Ken Burns motion & rendering...", 90)
    clean_title = sanitize_filename(script_data.get("title", session_id))[:40]
    output_filename = f"{clean_title}_{session_id}.mp4"
    final_video_path = str(OUTPUT_DIR / output_filename)
    
    compose_shorts_video(
        image_paths=image_paths,
        audio_path=mixed_audio_path,
        subtitles_path=sub_path,
        output_video_path=final_video_path,
        total_duration=duration
    )

    upload_result = None
    if auto_upload:
        notify("Step 8/8: Publishing to YouTube...", 98)
        upload_result = upload_to_youtube(
            video_path=final_video_path,
            title=script_data.get("title", clean_title),
            description=script_data.get("description", ""),
            tags=script_data.get("tags", []),
            privacy_status=PRIVACY_STATUS
        )
    else:
        notify("Step 8/8: Video ready for YouTube upload!", 100)
        upload_result = {
            "status": "ready_for_upload",
            "message": "Video rendered and ready to publish."
        }

    # Record history
    record = {
        "id": session_id,
        "title": script_data.get("title", clean_title),
        "description": script_data.get("description", ""),
        "tags": script_data.get("tags", []),
        "niche": niche,
        "voice": voice,
        "duration": round(duration, 1),
        "video_path": final_video_path,
        "filename": output_filename,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "upload_status": upload_result
    }
    _save_history(record)

    return record
