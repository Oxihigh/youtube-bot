import os
import shutil
import subprocess
import sys
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
MUSIC_DIR = ASSETS_DIR / "music"
FONTS_DIR = ASSETS_DIR / "fonts"
TEMP_DIR = BASE_DIR / "temp"

for d in [OUTPUT_DIR, ASSETS_DIR, MUSIC_DIR, FONTS_DIR, TEMP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

_CACHED_FFMPEG_PATH = None

def get_ffmpeg_path() -> str:
    """
    Locates ffmpeg executable reliably across Windows environments,
    checking PATH, imageio_ffmpeg, and WinGet Gyan.FFmpeg installation directories.
    """
    global _CACHED_FFMPEG_PATH
    if _CACHED_FFMPEG_PATH and os.path.isfile(_CACHED_FFMPEG_PATH):
        return _CACHED_FFMPEG_PATH

    # 1. Check direct PATH
    found = shutil.which("ffmpeg")
    if found:
        _CACHED_FFMPEG_PATH = found
        return found

    # 2. Check imageio_ffmpeg
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.isfile(exe):
            _CACHED_FFMPEG_PATH = exe
            return exe
    except Exception:
        pass

    # 3. Check Windows WinGet Gyan.FFmpeg typical locations
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        winget_links = Path(local_app_data) / "Microsoft" / "WinGet" / "Links" / "ffmpeg.exe"
        if winget_links.is_file():
            _CACHED_FFMPEG_PATH = str(winget_links)
            return str(winget_links)

        # Search inside WinGet packages folder
        winget_pkgs = Path(local_app_data) / "Microsoft" / "WinGet" / "Packages"
        if winget_pkgs.exists():
            for exe in winget_pkgs.glob("**/ffmpeg.exe"):
                if exe.is_file():
                    _CACHED_FFMPEG_PATH = str(exe)
                    return str(exe)

    # Fallback to plain "ffmpeg"
    return "ffmpeg"


def get_audio_duration(audio_path: str) -> float:
    """Returns duration in seconds using ffprobe or mutagen fallback."""
    try:
        from mutagen.mp3 import MP3
        audio = MP3(audio_path)
        return float(audio.info.length)
    except Exception:
        pass

    ffmpeg = get_ffmpeg_path()
    ffprobe = ffmpeg.replace("ffmpeg.exe", "ffprobe.exe") if ffmpeg.endswith(".exe") else "ffprobe"
    if not os.path.isfile(ffprobe):
        ffprobe = shutil.which("ffprobe") or "ffprobe"

    cmd = [
        ffprobe,
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        return 50.0  # Safe default for YouTube Shorts


def sanitize_filename(name: str) -> str:
    """Clean filename of invalid characters."""
    keepcharacters = (' ', '.', '_', '-')
    return "".join(c for c in name if c.isalnum() or c in keepcharacters).rstrip().strip()
