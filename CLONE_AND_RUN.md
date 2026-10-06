# 🚀 Git Push & Clone Guide: Move to Any Machine in 2 Steps

This repository is formatted and structured so that you can push it to GitHub from this computer, and clone it onto **any other system** (Windows, Mac, or Linux) and run it with a single command.

---

## 💻 Machine 1 (THIS Computer): Push to GitHub

Run these commands in PowerShell or Terminal on this machine:

```powershell
# 1. (Optional) Set branch name to main
git branch -M main

# 2. Add your GitHub repository as remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 3. Push all code to GitHub
git push -u origin main
```

*(Note: Sensitive files like your local `.env`, credentials, generated MP4s, and `venv/` are protected by `.gitignore` and will never leak into your git repository).*

---

## 🖥️ Machine 2 (YOUR OTHER Computer): Clone & Run

On your second computer, follow these simple steps:

### 1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Run the 1-Click Setup:

#### On Windows:
- Double-click **`setup.bat`** (or run `.\setup.bat` in terminal).
- This automatically creates the virtual environment, installs all dependencies, and sets up folders.
- Then double-click **`start.bat`** to launch the Web Dashboard at `http://127.0.0.1:8000`!

#### On Mac / Linux:
```bash
chmod +x setup.sh start.sh
./setup.sh
./start.sh
```

---

## 🔑 Adding Your Keys on the New Machine

When you open the Web Dashboard at **`http://127.0.0.1:8000`** on your other machine:
1. Go to the **"API & YouTube"** tab.
2. Paste your `GEMINI_API_KEY` and click **"Save Key to .env"**.
3. (Optional) Place your `client_secrets.json` into the root folder if you want automatic YouTube uploads.

You are completely ready to generate and schedule videos!
