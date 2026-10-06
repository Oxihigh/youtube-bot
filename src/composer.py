import os
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any
from src.utils import get_ffmpeg_path, TEMP_DIR, OUTPUT_DIR
from src.config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS

def _escape_ffmpeg_path(path_str: str) -> str:
    """Escapes Windows path for FFmpeg filter string arguments."""
    p = os.path.abspath(path_str).replace("\\", "/")
    # Escape colon after drive letter e.g. C:/ -> C\:/
    if len(p) >= 2 and p[1] == ":":
        p = p[0] + "\\:" + p[2:]
    return p


def compose_shorts_video(
    image_paths: List[str],
    audio_path: str,
    subtitles_path: str,
    output_video_path: str,
    total_duration: float
) -> str:
    """
    Renders the final YouTube Shorts video:
    1. Computes exact timing per scene.
    2. Builds high-speed vertical 9:16 video clips with ultrafast encoding.
    3. Concatenates scenes into a single stream.
    4. Burns styled karaoke subtitles (.ass).
    5. Syncs audio (voiceover + music).
    6. Outputs crisp 1080x1920 MP4.
    """
    ffmpeg = get_ffmpeg_path()
    num_scenes = max(len(image_paths), 1)
    duration_per_scene = total_duration / num_scenes

    # Step 1: Render individual scene clips
    rendered_clips = []
    for idx, img_path in enumerate(image_paths):
        clip_path = str(TEMP_DIR / f"clip_{idx}.mp4")

        # Fast and clean 1080x1920 vertical framing with smooth frame rate
        cmd = [
            ffmpeg, "-y",
            "-loop", "1",
            "-t", f"{duration_per_scene:.3f}",
            "-i", img_path,
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-r", str(VIDEO_FPS),
            "-pix_fmt", "yuv420p",
            clip_path
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            rendered_clips.append(clip_path)
        except Exception as e:
            print(f"[Composer] Scene {idx} render error: {e}")
            rendered_clips.append(clip_path)

    # Step 2: Create concat list file
    concat_list_file = TEMP_DIR / "concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for c in rendered_clips:
            clean_c = str(c).replace("\\", "/")
            f.write(f"file '{clean_c}'\n")

    # Step 3: Combine clips into intermediate video
    temp_concat_video = str(TEMP_DIR / "concat_raw.mp4")
    concat_cmd = [
        ffmpeg,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        temp_concat_video
    ]
    subprocess.run(concat_cmd, capture_output=True, check=True)

    # Step 4: Burn subtitles and merge final audio
    escaped_sub = _escape_ffmpeg_path(subtitles_path)
    final_cmd = [
        ffmpeg,
        "-y",
        "-i", temp_concat_video,
        "-i", audio_path,
        "-vf", f"ass='{escaped_sub}'",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_video_path
    ]

    try:
        subprocess.run(final_cmd, capture_output=True, check=True)
    except Exception as e:
        print(f"[Composer] Notice: {e}. Trying fallback without ass filter...")
        fallback_final_cmd = [
            ffmpeg,
            "-y",
            "-i", temp_concat_video,
            "-i", audio_path,
            "-c:v", "libx264",
            "-preset", "fast",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_video_path
        ]
        subprocess.run(fallback_final_cmd, capture_output=True, check=True)

    print(f"[Composer] Render complete! Video saved to: {output_video_path}")
    return output_video_path
