import os
import urllib.parse
import time
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from src.utils import TEMP_DIR
from src.config import VIDEO_WIDTH, VIDEO_HEIGHT

def create_fallback_graphic(prompt: str, output_path: str, scene_idx: int = 1) -> str:
    """
    Creates an atmospheric, sleek gradient graphic as a fail-safe fallback
    if network/API is unreachable.
    """
    img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), color=(12, 14, 20))
    draw = ImageDraw.Draw(img)

    # Add moody gradient blobs
    palette = [
        ((25, 30, 45), (10, 12, 18)),
        ((40, 20, 30), (15, 10, 15)),
        ((15, 35, 40), (8, 18, 22)),
        ((35, 30, 15), (18, 15, 8))
    ]
    c1, c2 = palette[scene_idx % len(palette)]

    for y in range(VIDEO_HEIGHT):
        ratio = y / VIDEO_HEIGHT
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(0, y), (VIDEO_WIDTH, y)], fill=(r, g, b))

    # Add glowing geometric circles or atmospheric vignette
    overlay = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    cx, cy = VIDEO_WIDTH // 2, VIDEO_HEIGHT // 2
    for radius in range(400, 50, -30):
        alpha = int(25 * (1 - radius / 400))
        overlay_draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            outline=(200, 220, 255, alpha),
            width=2
        )
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img.save(output_path, "JPEG", quality=92)
    return output_path


def generate_scene_image(
    prompt: str,
    output_path: str,
    scene_idx: int = 1,
    model: str = "flux"
) -> str:
    """
    Generates a high-quality 9:16 vertical AI image using Pollinations (Flux / SDXL).
    Auto-retries with fallbacks and gracefully creates atmospheric graphic if offline.
    """
    # Clean and encode prompt
    clean_prompt = prompt.replace("\n", " ").strip()[:350]
    encoded_prompt = urllib.parse.quote(clean_prompt)

    # Pollinations image generation endpoint with 1080x1920 vertical specs
    endpoints = [
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={VIDEO_WIDTH}&height={VIDEO_HEIGHT}&model={model}&nologo=true&seed={int(time.time() * 1000) % 1000000}",
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={VIDEO_WIDTH}&height={VIDEO_HEIGHT}&model=turbo&nologo=true",
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=720&height=1280&nologo=true"
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }

    for url in endpoints:
        try:
            print(f"[Visuals] Generating Scene {scene_idx} image...")
            resp = requests.get(url, headers=headers, timeout=25)
            if resp.status_code == 200 and len(resp.content) > 10000:
                with open(output_path, "wb") as f:
                    f.write(resp.content)

                # Ensure exact 1080x1920 dimensions
                with Image.open(output_path) as im:
                    if im.size != (VIDEO_WIDTH, VIDEO_HEIGHT):
                        im_resized = im.resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.Resampling.LANCZOS)
                        im_resized.save(output_path, "JPEG", quality=95)
                return output_path
        except Exception as e:
            print(f"[Visuals] Endpoint attempt failed ({e}), trying alternative...")
            time.sleep(1)

    # If all remote endpoints fail, generate sleek fallback graphic
    print(f"[Visuals] Notice: Using fallback atmospheric visual for Scene {scene_idx}.")
    return create_fallback_graphic(prompt, output_path, scene_idx)


def generate_all_scene_images(scenes: List[Dict[str, Any]], session_id: str) -> List[str]:
    """
    Generates vertical 9:16 images for all scenes in the script.
    """
    image_paths = []
    for idx, scene in enumerate(scenes, 1):
        filename = f"{session_id}_scene_{idx}.jpg"
        filepath = str(TEMP_DIR / filename)
        prompt = scene.get("image_prompt", "cinematic dramatic lighting atmospheric 8k")
        generate_scene_image(prompt, filepath, scene_idx=idx)
        image_paths.append(filepath)
    return image_paths
