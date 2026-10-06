# 🎬 AutoShorts AI — Fully Autonomous Faceless YouTube Channel Engine

AutoShorts AI is an end-to-end autonomous pipeline designed to research, script, narrate, visualize, edit, subtitle, and publish high-retention **YouTube Shorts** (vertical 9:16) with 100% automation.

---

## ⚡ What Gets Automated (Step 1 to Final Step)

```
[1. Trend Research] ➔ [2. Script & SEO] ➔ [3. Neural Voiceover] ➔ [4. AI 9:16 Visuals]
         │
         ▼
[5. Dynamic Subtitles] ➔ [6. Audio Mixing] ➔ [7. FFmpeg Rendering] ➔ [8. YouTube Publishing]
```

1. **Step 1: Viral Topic & Trend Research** (`src/researcher.py`):
   - Uses **Google Gemini 2.5 Flash** (with instant curated fallback engine) to discover viral angles with high curiosity hooks tailored to your chosen niche.
2. **Step 2: Scriptwriting & SEO Optimization** (`src/scriptwriter.py`):
   - Generates high-retention 40-55s YouTube Shorts scripts (0-3s hook, curiosity loops, loopable ending).
   - Generates high CTR YouTube Titles (with emojis & `#shorts`), full description, and high-volume search tags.
3. **Step 3: Neural Voiceover Synthesis** (`src/voiceover.py`):
   - High-fidelity **Edge-TTS neural voices** (Christopher, Guy, Andrew, Brian, Ava, Emma) completely free.
   - Extracts word-level timestamps for synced karaoke subtitles.
4. **Step 4: AI Visuals Generation** (`src/visuals.py`):
   - Generates 9:16 vertical images matching each scene with cinematic lighting and custom art styles (Cinematic Dark, Vintage Doc, Cyberpunk Neon, Photorealistic).
5. **Step 5: Dynamic Karaoke Subtitles** (`src/captions.py`):
   - Produces styled Advanced SubStation Alpha (`.ass`) subtitles with high-contrast text, yellow highlights, and thick black stroke.
6. **Step 6: Background Music & Audio Ducking** (`src/audio.py`):
   - Automatically layers royalty-free ambient music ducked at ~12% volume for maximum voice clarity.
7. **Step 7: Video Assembly & Rendering** (`src/composer.py`):
   - Fast, reliable FFmpeg assembly producing crisp 1080x1920 30fps vertical MP4 videos ready for Shorts.
8. **Step 8: YouTube Publishing & Scheduling** (`src/publisher.py`):
   - YouTube Data API v3 OAuth2 upload with automated tags, description, privacy mode (`private`, `unlisted`, `public`), and scheduling.

---

## 🚀 Quick Start Guide

### 1. Launch the Web Studio Dashboard
```bash
.\venv\Scripts\python main.py
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser:
- **Studio Tab:** 1-Click interactive generation with live progress tracker and 9:16 preview video player.
- **Gallery Tab:** Stream and download all rendered Shorts.
- **Autopilot Tab:** Set recurring daily cron schedules.
- **Settings Tab:** Save your Gemini API key and configure YouTube OAuth.

---

### 2. Run via Command Line (1-Click Generation)
Generate a short directly from terminal:
```bash
# Psychology Facts short
.\venv\Scripts\python main.py --generate --niche "Psychology Facts"

# Stoicism short with custom topic
.\venv\Scripts\python main.py --generate --niche "Stoicism & Philosophy" --prompt "Why silence is your greatest power"

# Dark History short with specific voice
.\venv\Scripts\python main.py --generate --niche "Dark History" --voice "en-US-ChristopherNeural"
```

---

### 3. Set Up Autopilot (Hands-Free Scheduled Production)
To automatically create and publish videos on a daily schedule in the background:
```bash
.\venv\Scripts\python main.py --cron --frequency daily --niche "Psychology Facts" --auto-upload
```

---

## 🔑 Configuration & API Keys

All configuration is managed in `.env`:

```ini
# Gemini API Key (Free key: https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_api_key_here

# Channel Defaults
DEFAULT_NICHE=Psychology Facts
DEFAULT_VOICE=en-US-ChristopherNeural
DEFAULT_VISUAL_STYLE=cinematic_dark
AUTO_UPLOAD_DEFAULT=false
PRIVACY_STATUS=private
```

### YouTube Data API v3 Setup (For Automatic Uploads):
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable **YouTube Data API v3**.
3. Under **Credentials**, create an **OAuth 2.0 Client ID** (Application Type: *Desktop App*).
4. Download the JSON file and save it as `client_secrets.json` in this folder.
5. On the first upload, a browser window will open to authenticate your channel once. Credentials are saved locally to `token.json` for all future automated runs.

---

## 📁 Project Structure

```
faceless/
├── app.py                # FastAPI Web Studio Server
├── main.py               # CLI & Autopilot Runner
├── requirements.txt      # Python dependencies
├── .env                  # Environment secrets & configuration
├── src/
│   ├── researcher.py     # Viral topic & trend research engine
│   ├── scriptwriter.py   # Script, scene prompts & SEO generator
│   ├── voiceover.py      # Edge-TTS voice synthesis & word timestamps
│   ├── visuals.py        # 9:16 vertical AI image generation
│   ├── captions.py       # Styled kinetic karaoke ASS subtitles
│   ├── audio.py          # Background music manager & mixer
│   ├── composer.py       # FFmpeg video assembler & burner
│   ├── publisher.py      # YouTube Data API v3 uploader
│   └── pipeline.py       # 8-step pipeline coordinator
├── web/
│   ├── static/           # Dark-mode CSS & vanilla JS
│   └── templates/        # Responsive HTML5 studio
├── output/               # Rendered final 1080x1920 MP4 Shorts
└── temp/                 # Intermediate audio, image clips, subtitles
```
