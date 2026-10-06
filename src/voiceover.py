import asyncio
import os
import edge_tts
from pathlib import Path
from typing import Dict, Any, List, Tuple
from src.config import DEFAULT_VOICE, VOICE_PRESETS
from src.utils import TEMP_DIR, get_audio_duration

async def _synthesize_edge_tts(
    text: str,
    voice: str,
    output_audio_path: str,
    rate: str = "+0%",
    pitch: str = "+0Hz"
) -> List[Dict[str, Any]]:
    """
    Synthesizes speech using Microsoft Edge-TTS and collects word-boundary timing events.
    """
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    words = []

    # Stream out audio chunks and parse WordBoundary metadata
    with open(output_audio_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                # offset and duration in 100-nanosecond units (10^-7 seconds)
                start_sec = chunk["offset"] / 10_000_000
                duration_sec = chunk["duration"] / 10_000_000
                words.append({
                    "word": chunk["text"],
                    "start": start_sec,
                    "end": start_sec + duration_sec
                })

    return words


def generate_voiceover(
    text: str,
    voice: str = DEFAULT_VOICE,
    filename_prefix: str = "voiceover",
    rate: str = "+0%",
    pitch: str = "+0Hz"
) -> Dict[str, Any]:
    """
    Synchronous wrapper to generate voiceover MP3 and return metadata.
    """
    if voice not in VOICE_PRESETS:
        voice = DEFAULT_VOICE

    audio_filename = f"{filename_prefix}.mp3"
    audio_path = str(TEMP_DIR / audio_filename)

    # Run async TTS
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        words = loop.run_until_complete(_synthesize_edge_tts(text, voice, audio_path, rate, pitch))
    finally:
        loop.close()

    duration = get_audio_duration(audio_path)

    return {
        "audio_path": audio_path,
        "duration": duration,
        "voice": voice,
        "word_timings": words
    }
