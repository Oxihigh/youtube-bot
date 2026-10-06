import argparse
import sys
import time
import schedule
import uvicorn

# Ensure UTF-8 output on Windows consoles for emojis in titles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.config import DEFAULT_NICHE, DEFAULT_VOICE, DEFAULT_VISUAL_STYLE
from src.pipeline import run_full_pipeline

def parse_args():
    parser = argparse.ArgumentParser(description="AutoShorts AI - Autonomous Faceless YouTube Engine")
    parser.add_argument("--web", action="store_true", help="Launch the interactive Web Studio dashboard")
    parser.add_argument("--generate", action="store_true", help="Generate a YouTube Short via CLI")
    parser.add_argument("--niche", type=str, default=DEFAULT_NICHE, help="Target niche (e.g., 'Psychology Facts')")
    parser.add_argument("--prompt", type=str, default="", help="Custom topic prompt (optional)")
    parser.add_argument("--voice", type=str, default=DEFAULT_VOICE, help="Edge-TTS voice identifier")
    parser.add_argument("--style", type=str, default=DEFAULT_VISUAL_STYLE, help="Visual aesthetic preset")
    parser.add_argument("--auto-upload", action="store_true", help="Directly upload to YouTube channel")
    parser.add_argument("--cron", action="store_true", help="Run in recurring autopilot cron mode")
    parser.add_argument("--frequency", type=str, default="daily", choices=["daily", "hourly", "test"], help="Cron frequency")
    parser.add_argument("--port", type=int, default=8000, help="Web dashboard port")
    return parser.parse_args()


def scheduled_job(niche: str, voice: str, style: str, auto_upload: bool):
    print(f"\n[Autopilot Cron] Triggering scheduled Short generation for '{niche}' at {time.strftime('%Y-%m-%d %H:%M:%S')}...")
    try:
        res = run_full_pipeline(
            niche=niche,
            prompt="",
            voice=voice,
            visual_style=style,
            auto_upload=auto_upload
        )
        print(f"[Autopilot Cron] Success! Video created: {res.get('filename')}")
    except Exception as e:
        print(f"[Autopilot Cron] Error generating video: {e}")


def run_cron(args):
    print(f"======================================================")
    print(f" AutoShorts AI Autopilot Scheduler Activated")
    print(f" Frequency: {args.frequency.upper()} | Niche: {args.niche}")
    print(f" Auto-Upload: {'Enabled' if args.auto_upload else 'Disabled'}")
    print(f" Press Ctrl+C to terminate.")
    print(f"======================================================\n")

    if args.frequency == "daily":
        schedule.every().day.at("14:00").do(scheduled_job, args.niche, args.voice, args.style, args.auto_upload)
    elif args.frequency == "hourly":
        schedule.every().hour.do(scheduled_job, args.niche, args.voice, args.style, args.auto_upload)
    elif args.frequency == "test":
        schedule.every(2).minutes.do(scheduled_job, args.niche, args.voice, args.style, args.auto_upload)

    # Run one immediately on startup
    scheduled_job(args.niche, args.voice, args.style, args.auto_upload)

    while True:
        schedule.run_pending()
        time.sleep(1)


def main():
    args = parse_args()

    if args.generate:
        print(f"[*] Starting 1-click generation for niche: '{args.niche}'...")
        res = run_full_pipeline(
            niche=args.niche,
            prompt=args.prompt,
            voice=args.voice,
            visual_style=args.style,
            auto_upload=args.auto_upload
        )
        print(f"\n[+] Generation Finished!")
        print(f"    Title: {res.get('title')}")
        print(f"    Video: {res.get('video_path')}")
        print(f"    Duration: {res.get('duration')}s")
        print(f"    Upload Status: {res.get('upload_status', {}).get('status')}")
        return

    if args.cron:
        run_cron(args)
        return

    # Default: launch Web Dashboard
    print("======================================================")
    print(" AutoShorts AI - Launching Web Studio Dashboard")
    print(f" URL: http://127.0.0.1:{args.port}")
    print("======================================================\n")
    uvicorn.run("app:app", host="127.0.0.1", port=args.port, reload=True)


if __name__ == "__main__":
    main()
