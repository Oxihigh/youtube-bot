import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# API Keys & Credentials
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
YOUTUBE_CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secrets.json")
YOUTUBE_TOKEN_FILE = os.getenv("YOUTUBE_TOKEN_FILE", "token.json")

# Channel & Video Configuration
DEFAULT_NICHE = os.getenv("DEFAULT_NICHE", "Psychology Facts")
DEFAULT_VOICE = os.getenv("DEFAULT_VOICE", "en-US-ChristopherNeural")
DEFAULT_VISUAL_STYLE = os.getenv("DEFAULT_VISUAL_STYLE", "cinematic_dark")
AUTO_UPLOAD_DEFAULT = os.getenv("AUTO_UPLOAD_DEFAULT", "false").lower() in ("true", "1", "yes")
PRIVACY_STATUS = os.getenv("PRIVACY_STATUS", "private")  # private, unlisted, public

# Video Dimensions for YouTube Shorts (9:16 Vertical)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30
MAX_SHORT_DURATION = 58  # Max 58s for Shorts to ensure loopable & under 60s limit

# Available Niches with pre-tuned viral prompts
NICHES = {
    "Psychology Facts": {
        "description": "Mind-bending psychological tricks, human behavior secrets, body language, and dark psychology.",
        "tone": "mysterious, urgent, deeply insightful",
        "default_style": "cinematic_dark"
    },
    "Dark History": {
        "description": "Bizarre, chilling, and overlooked historical events, ancient rulers, and eerie secrets.",
        "tone": "suspenseful, storytelling, dramatic",
        "default_style": "vintage_documentary"
    },
    "Mind-Blowing Science": {
        "description": "Crazy physics paradoxes, cosmos mysteries, quantum mechanics, and futuristic biology.",
        "tone": "wonder, fast-paced, mind-expanding",
        "default_style": "photorealistic"
    },
    "Stoicism & Philosophy": {
        "description": "Timeless life rules, brutal truth philosophy, Marcus Aurelius quotes, and self-mastery.",
        "tone": "stoic, grounded, commanding, inspiring",
        "default_style": "cinematic_dark"
    },
    "Tech & AI Secrets": {
        "description": "Shocking AI advancements, futuristic robotics, tech conspiracy/realities, and future predictions.",
        "tone": "high energy, futuristic, urgent",
        "default_style": "cyberpunk_neon"
    },
    "Unsolved Mysteries": {
        "description": "Enigmatic disappearances, coded messages, Bermuda triangle, and eerie historical enigmas.",
        "tone": "haunting, investigative, cliffhanger",
        "default_style": "cinematic_dark"
    }
}

# Free Neural Voices (Microsoft Edge-TTS)
VOICE_PRESETS = {
    "en-US-ChristopherNeural": {"label": "Christopher (Authoritative, Deep, Intense - Best for Shorts)", "gender": "Male"},
    "en-US-GuyNeural": {"label": "Guy (Narrative, Engaging, Dynamic)", "gender": "Male"},
    "en-US-AndrewNeural": {"label": "Andrew (Confident, Modern Podcaster)", "gender": "Male"},
    "en-US-BrianNeural": {"label": "Brian (British, Intellectual & Scholarly)", "gender": "Male"},
    "en-US-AvaNeural": {"label": "Ava (Expressive, Crisp, Modern)", "gender": "Female"},
    "en-US-EmmaNeural": {"label": "Emma (Dramatic, Storyteller)", "gender": "Female"}
}

# Image Generation Prompt Style Enhancers
VISUAL_STYLES = {
    "cinematic_dark": "cinematic dark moody atmospheric lighting, hyper-realistic 8k, unreal engine 5 render, dramatic contrast, high production value, photorealistic vertical composition 9:16",
    "vintage_documentary": "vintage archival documentary photograph, rich grainy film texture, moody sepia tones, authentic historical aesthetic, detailed 9:16",
    "cyberpunk_neon": "futuristic cyberpunk aesthetic, vivid neon glow, volumetric fog, octane render, ultra-detailed reflections, 9:16 vertical composition",
    "photorealistic": "shot on 35mm lens, award-winning photography, natural cinematic lighting, highly detailed texture, raw photo style, 9:16 vertical",
    "dark_fantasy": "dark fantasy concept art, intricate eerie details, dramatic chiaroscuro lighting, painted texture, epic scale, 9:16 vertical"
}
