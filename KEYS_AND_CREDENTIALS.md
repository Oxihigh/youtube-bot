# 🔑 API Keys & Credentials Guide for AutoShorts AI

This document provides a breakdown of all API keys, credentials, and requirements needed to run the autonomous faceless YouTube channel application.

---

## 📋 Quick Summary Table

| Key / Credential | Required? | Cost | Purpose | Where to Get |
|---|---|---|---|---|
| **Google Gemini API Key** | **Recommended** | **100% Free** | Topic research, 50s scriptwriting, visual prompts, SEO metadata | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| **YouTube OAuth (`client_secrets.json`)** | **Optional** | **100% Free** | Automatic 1-click YouTube uploads & video scheduling | [Google Cloud Console](https://console.cloud.google.com/) |
| **Microsoft Edge-TTS** | *Built-in* | **100% Free** | Neural voiceover & word timestamps | **No Key Needed** |
| **Pollinations.ai / Flux** | *Built-in* | **100% Free** | 9:16 vertical AI image generation | **No Key Needed** |
| **FFmpeg Engine** | *Installed* | **100% Free** | Video rendering, audio mixing & subtitle burning | **No Key Needed** |

---

## 1. Google Gemini API Key (`GEMINI_API_KEY`)

### Purpose:
Powers the AI intelligence of the channel:
- Viral topic discovery & audience hooks
- 40–55s high-retention scriptwriting (curiosity loops, cliffhangers, loopable endings)
- Visual scene prompts generation
- YouTube SEO (CTR-optimized titles, descriptions, and ranking tags)

> [!NOTE]
> If you do **not** provide a Gemini API key, the system still runs using its built-in offline viral topic and script engine.

### How to Get It (Takes ~30 seconds):
1. Go to **[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)**
2. Sign in with your Google account.
3. Click **"Create API key"** (or **"Get API key"**).
4. Copy the generated key (looks like `AIzaSy...`).

### How to Add It:
**Option A (Web Dashboard):**
- Open [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Navigate to the **"API & YouTube"** tab
- Paste your key and click **"Save Key to .env"**

**Option B (Direct `.env` file):**
- Open the `.env` file in the project root and paste:
```env
GEMINI_API_KEY=AIzaSyYourGeneratedKeyHere
```

---

## 2. YouTube Data API v3 (`client_secrets.json`)

### Purpose:
Allows the application to upload and schedule videos directly to your YouTube channel without opening YouTube Studio manually.

> [!NOTE]
> This is **optional**. If omitted, videos are fully rendered and saved in the `/output` folder, where you can preview or manually upload them whenever you want.

### Quota & Cost:
- **Free Quota:** Google Cloud provides **10,000 units/day** for free.
- Each video upload consumes ~1,600 units, allowing **up to 6 automated uploads per day** completely free.

### How to Get It (Step-by-Step):

#### Step 1: Create a Google Cloud Project
1. Go to the **[Google Cloud Console](https://console.cloud.google.com/)**.
2. Click the project dropdown in the top bar and select **"New Project"**.
3. Name it `AutoShorts-YouTube` and click **"Create"**.

#### Step 2: Enable the YouTube Data API v3
1. In the search bar at the top, search for **"YouTube Data API v3"**.
2. Click on it and press **"Enable"**.

#### Step 3: Configure OAuth Consent Screen
1. In the left navigation menu, go to **APIs & Services** &rarr; **OAuth consent screen**.
2. Select **External** and click **Create**.
3. Fill in:
   - **App name:** `AutoShorts AI`
   - **User support email:** (your Gmail)
   - **Developer contact email:** (your Gmail)
4. Click **Save and Continue** through Scopes.
5. In **Test users**, click **"+ Add Users"** and enter your Google account email address (the one that owns your YouTube channel).
6. Click **Save and Continue**.

#### Step 4: Create OAuth 2.0 Credentials
1. Go to **APIs & Services** &rarr; **Credentials**.
2. Click **"+ Create Credentials"** &rarr; **OAuth client ID**.
3. Select **Application type**: **Desktop app**.
4. Set the name to `AutoShorts Uploader` and click **Create**.
5. Click **"Download JSON"** on the credential popup.

#### Step 5: Place the File in the Project
1. Rename the downloaded file to exactly:
   ```
   client_secrets.json
   ```
2. Move it into your project folder:
   ```
   c:\Users\oxihi\Desktop\bareddy\faceless\client_secrets.json
   ```
3. On your first upload attempt, a browser window will open asking you to grant permission once. The system will save a `token.json` file so all future runs are 100% headless and automatic.

---

## 3. Services That Require NO Keys

You do **NOT** need any API key or subscription for the following components:

- **Microsoft Edge-TTS:** Unlimited neural voices included for free via `edge-tts`.
- **Pollinations.ai / Flux:** Free high-resolution 9:16 AI image generation without authentication.
- **FFmpeg Engine:** Installed locally; handles all video compilation, audio ducking, and subtitle rendering.
- **Background Music:** CC0 royalty-free tracks bundled and cached automatically in `assets/music/`.

---

## 4. Current Configuration Status Check

You can verify your key statuses at any time by visiting:
- **Web Dashboard:** [http://127.0.0.1:8000](http://127.0.0.1:8000) &rarr; Status indicators in the sidebar and Settings tab.
- **API Status Endpoint:** [http://127.0.0.1:8000/api/status](http://127.0.0.1:8000/api/status)
