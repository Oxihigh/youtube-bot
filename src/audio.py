import os
import shutil
import subprocess
import requests
from pathlib import Path
from typing import Optional
from src.utils import MUSIC_DIR, TEMP_DIR, get_ffmpeg_path

# Curated royalty-free / CC0 ambient background tracks for Shorts
DEFAULT_MUSIC_URLS = {
    "dark_suspense": "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3", # Ambient suspense
    "dramatic_cinematic": "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3", # Cinematic piano/strings
    "chill_lofi": "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3" # Lofi beats
}

def ensure_background_music(mood: str = "dark_suspense") -> Optional[str]:
    """
    Ensures at least one royalty-free background music track exists in assets/music.
    Downloads from trusted CC0 source if not already cached.
    """
    MUSIC_DIR.mkdir(parents=True, exist_ok=True)
    target_path = MUSIC_DIR / f"{mood}.mp3"

    if target_path.exists() and target_path.stat().st_size > 10000:
        return str(target_path)

    # Check any existing mp3 in folder
    existing = list(MUSIC_DIR.glob("*.mp3"))
    if existing:
        return str(existing[0])

    # Attempt to download default track
    url = DEFAULT_MUSIC_URLS.get(mood, list(DEFAULT_MUSIC_URLS.values())[0])
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200 and len(resp.content) > 10000:
            with open(target_path, "wb") as f:
                f.write(resp.content)
            return str(target_path)
    except Exception as e:
        print(f"[Audio] Music download notice: {e}. Generating silent/ambient audio buffer.")

    return None


def mix_voice_and_music(
    voiceover_path: str,
    output_mixed_path: str,
    music_mood: str = "dark_suspense",
    music_volume: float = 0.12,
    voice_volume: float = 1.0
) -> str:
    """
    Mixes voiceover with background music using FFmpeg amix filter.
    Music is auto-looped to match voiceover duration and ducked to low volume.
    """
    ffmpeg = get_ffmpeg_path()
    bg_music = ensure_background_music(music_mood)

    if not bg_music or not os.path.isfile(bg_music):
        # If no background music is available, just copy voiceover
        shutil.copyfile(voiceover_path, output_mixed_path)
        return output_mixed_path

    # Filter graph: loop music, lower music volume to 12%, voiceover at 100%, mix together
    filter_complex = (
        f"[0:a]volume={voice_volume}[voice];"
        f"[1:a]aloop=loop=-1:size=2e+09,volume={music_volume}[music];"
        f"[voice][music]amix=inputs=2:duration=first:dropout_transition=2[out]"
    )

    cmd = [
        ffmpeg,
        "-y",
        "-i", voiceover_path,
        "-i", bg_music,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        output_mixed_path
    ]

    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return output_mixed_path
    except Exception as e:
        print(f"[Audio] Mix warning: {e}. Falling back to plain voiceover.")
        shutil.copyfile(voiceover_path, output_mixed_path)
        return output_mixed_path
