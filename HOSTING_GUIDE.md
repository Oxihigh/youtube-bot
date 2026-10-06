# 🌐 Free & Ultra-Cheap Hosting Guide for AutoShorts AI

This guide shows you the best ways to host the AutoShorts AI autopilot pipeline so your channel produces and publishes videos 24/7 without keeping your computer on.

---

## 🏆 Comparison of Hosting Options

| Hosting Option | Cost | Best For | Pros | Cons |
|---|---|---|---|---|
| **1. GitHub Actions (Recommended)** | **$0 / month (100% Free)** | **Scheduled Autopilot Uploads** | No server needed, pre-installed FFmpeg, 2,000 free mins/mo, runs on cron | No permanent live Web UI (runs as scheduled batch job) |
| **2. Oracle Cloud "Always Free"** | **$0 / month (100% Free)** | **24/7 Web Dashboard + Autopilot** | Full VPS with 4 vCPUs, 24 GB RAM, 200 GB SSD forever free | Requires credit card verification during signup |
| **3. Budget Linux VPS (RackNerd / Hetzner)** | **~$1 - $3.50 / month** | **Full Independence & Speed** | High performance, instant setup, 24/7 Web Studio access | Small annual or monthly fee ($12/yr or €3.50/mo) |
| **4. Railway / Render / Koyeb** | **$0 (Free Trial) to $5/mo** | **1-Click Container Deploy** | Easy git push deployment | Free tiers may sleep after inactivity |

---

## 🥇 Option 1: GitHub Actions (100% Free Forever)

**Why this is the best choice for automated channels:**
- You do **NOT** need to pay for a server.
- GitHub provides **2,000 free build minutes every month** for private repositories (and **unlimited** for public).
- Producing a 45-second Short takes ~1.5 minutes of compute.
- **The Math for 3 Videos Every Day:**
  - 3 videos/day &times; 1.5 minutes = **4.5 minutes per day**
  - 30 days &times; 4.5 minutes = **~135 minutes per month**
  - **135 out of 2,000 minutes = only 6.7% of your free quota!**
  - This means **1 single GitHub account easily handles 3 videos every day** with 1,865 minutes left over.
  - If you use **2 GitHub accounts**, you can easily produce 6 to 10 videos per day across multiple channels for $0!

### 3x Daily Schedule Slots (Configured in [`.github/workflows/autopilot.yml`](file:///.github/workflows/autopilot.yml)):
1. **Slot 1 (08:00 UTC / Morning Peak):** *Psychology Facts*
2. **Slot 2 (14:00 UTC / Midday Peak):** *Mind-Blowing Science*
3. **Slot 3 (20:00 UTC / Evening Prime Time):** *Dark History / Stoicism*

### Setup Instructions (5 Minutes):

1. **Push your code to a private GitHub repository:**
   ```bash
   git init
   git add .
   git commit -m "feat: autoshorts engine"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Add your secrets to GitHub:**
   - Go to your repository on GitHub.
   - Click **Settings** &rarr; **Secrets and variables** &rarr; **Actions**.
   - Click **"New repository secret"** and add:
     - `GEMINI_API_KEY`: Your Gemini API key.
     - `YOUTUBE_CLIENT_SECRETS_JSON` *(Optional)*: The contents of your `client_secrets.json`.
     - `YOUTUBE_TOKEN_JSON` *(Optional)*: The contents of your authenticated `token.json`.

3. **Autopilot is already configured!**
   - The file [`.github/workflows/autopilot.yml`](file:///.github/workflows/autopilot.yml) is already created in your project.
   - It runs automatically **every day at 14:00 UTC**.
   - You can also manually trigger a video generation anytime with 1 click from the **Actions** tab on your phone or laptop.
   - Every generated MP4 is saved as a downloadable build artifact.

---

## 🥈 Option 2: Oracle Cloud Always Free VPS (100% Free Forever)

If you want the interactive **Web Studio Dashboard** accessible 24/7 from your browser, Oracle Cloud offers the most generous free tier in the cloud industry.

### What You Get for $0:
- Up to 4 ARM Ampere cores + 24 GB RAM (or 2 AMD micro instances)
- 200 GB NVMe Storage
- Static public IPv4 address

### Setup Instructions:
1. Sign up at [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/) *(requires a valid card for identity verification, but charges $0)*.
2. Create an **Ubuntu 22.04 / 24.04** VM instance.
3. SSH into your VM:
   ```bash
   ssh ubuntu@YOUR_SERVER_IP
   ```
4. Install Docker & Git:
   ```bash
   sudo apt update && sudo apt install -y docker.io docker-compose git
   sudo usermod -aG docker ubuntu
   ```
5. Clone your repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git faceless
   cd faceless
   ```
6. Start the application container:
   ```bash
   docker compose up -d
   ```
7. Open `http://YOUR_SERVER_IP:8000` in your browser. The Web Studio and background cron will run continuously 24/7.

---

## 🥉 Option 3: Ultra-Cheap Budget VPS ($1 - $3.50 / month)

If you want an affordable, no-hassle dedicated server without Oracle's strict verification:

1. **RackNerd "New Year / Black Friday" Deals:**
   - Usually **$10 to $14 PER YEAR** (~$1/month) for a 1GB/1CPU Linux VPS.
2. **Hetzner Cloud (CX22):**
   - **~€3.50 / month** for 2 vCPUs, 4GB RAM in Germany/Finland/US. Ultra-fast CPU encoding.

### Running Autopilot on any Linux VPS:
Simply start the background cron process with `nohup` or `systemd`:
```bash
# Run in background with nohup
nohup python main.py --cron --frequency daily --niche "Psychology Facts" --auto-upload > cron.log 2>&1 &
```
Or run the web studio daemon:
```bash
nohup python main.py --port 8000 > web.log 2>&1 &
```

---

## 💡 Summary Recommendation

- **For 100% Free Zero-Maintenance Hands-Free Channel:** Use **Option 1 (GitHub Actions)**. It uses 0 server resources on your machine, costs $0, and executes the daily cron reliably in GitHub's cloud.
- **For 24/7 Live Web Dashboard UI:** Use **Option 2 (Oracle Always Free)** or **Option 3 (Hetzner / RackNerd $1-$3/mo)** using the included [`docker-compose.yml`](file:///c:/Users/oxihi/Desktop/bareddy/faceless/docker-compose.yml).
