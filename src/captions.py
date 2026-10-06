import os
from typing import List, Dict, Any
from pathlib import Path
from src.utils import TEMP_DIR
from src.config import VIDEO_WIDTH, VIDEO_HEIGHT

def format_timestamp_ass(seconds: float) -> str:
    """Formats seconds to ASS timestamp H:MM:SS.cs"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int(round((seconds - int(seconds)) * 100))
    if centis >= 100:
        centis = 99
    return f"{hrs}:{mins:02d}:{secs:02d}.{centis:02d}"


def generate_styled_ass_subtitles(
    word_timings: List[Dict[str, Any]],
    output_ass_path: str,
    words_per_group: int = 3,
    highlight_color: str = "&H002EFCFF", # Vibrant Yellow in BGR (&HAABBGGRR)
    font_name: str = "Impact"
) -> str:
    """
    Generates an Advanced SubStation Alpha (.ass) subtitle file
    with modern viral YouTube Shorts styling (centered, thick stroke, 2-3 words per beat).
    """
    # ASS Header
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {VIDEO_WIDTH}
PlayResY: {VIDEO_HEIGHT}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ShortsViral,{font_name},72,&H00FFFFFF,{highlight_color},&H00000000,&H80000000,-1,0,0,0,100,100,1.5,0,1,5.0,2.5,2,80,80,480,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []

    if not word_timings:
        # Empty placeholder if no words provided
        with open(output_ass_path, "w", encoding="utf-8") as f:
            f.write(ass_content)
        return output_ass_path

    # Group words into short rhythmic chunks of 2 to 4 words
    i = 0
    while i < len(word_timings):
        chunk = word_timings[i : i + words_per_group]
        i += words_per_group

        start_time = format_timestamp_ass(chunk[0]["start"])
        end_time = format_timestamp_ass(chunk[-1]["end"] + 0.1)

        # Highlight key words with yellow color tag
        chunk_words = [w["word"] for w in chunk]
        if len(chunk_words) > 1:
            # Highlight first or middle word
            formatted_text = f"{{\\c{highlight_color}\\b1}}{chunk_words[0].upper()}{{\\r}} " + " ".join(chunk_words[1:]).upper()
        else:
            formatted_text = f"{{\\c{highlight_color}\\b1}}{chunk_words[0].upper()}{{\\r}}"

        events.append(f"Dialogue: 0,{start_time},{end_time},ShortsViral,,0,0,0,,{formatted_text}")

    ass_content += "\n".join(events) + "\n"

    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)

    return output_ass_path
