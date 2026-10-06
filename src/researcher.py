import os
import json
import random
from typing import Dict, Any, List
from src.config import GEMINI_API_KEY, NICHES

# Curated fallback viral topics for immediate offline / zero-key testing
CURATED_FALLBACK_TOPICS = {
    "Psychology Facts": [
        {
            "title_idea": "The Dark Psychology Trick People Use to Manipulate You",
            "hook": "If someone pauses before answering your question, they aren't thinking. They're doing this...",
            "angle": "Unconscious body language and conversational traps that people unknowingly fall into."
        },
        {
            "title_idea": "3 Psychological Signs Someone Is Secretly Jealous of You",
            "hook": "Notice how they react when you share good news? Psychology reveals what's really happening...",
            "angle": "Subconscious micro-expressions of envy and backhanded compliments."
        },
        {
            "title_idea": "Why Intelligent People Struggle to Sleep at Night",
            "hook": "If your brain refuses to shut off at 2 AM, it's not insomnia. Psychology calls this hyper-brain syndrome...",
            "angle": "Overactive cognitive processing and subconscious problem-solving during REM cycles."
        }
    ],
    "Dark History": [
        {
            "title_idea": "The Terrifying Roman Punishment Worse Than Death",
            "hook": "In ancient Rome, if you committed this one forbidden crime, you were sewn into a leather sack with 4 living creatures...",
            "angle": "Poena Cullei - ancient ritualistic capital punishment."
        },
        {
            "title_idea": "The Dancing Plague of 1518 That Struck Strasbourg",
            "hook": "In July 1518, a woman stepped into the street and started dancing. Within a month, hundreds joined until their hearts gave out...",
            "angle": "Mass psychogenic contagion and eerie medieval mystery."
        }
    ],
    "Mind-Blowing Science": [
        {
            "title_idea": "What Happens If You Fall Into a Black Hole?",
            "hook": "If you crossed the event horizon of a supermassive black hole, you wouldn't die instantly. You would see the entire universe end in seconds...",
            "angle": "Gravitational time dilation and spaghettification."
        },
        {
            "title_idea": "Quantum Entanglement: Einstein's 'Spooky Action'",
            "hook": "Two particles separated by billions of light-years can communicate instantly. Einstein hated this, but modern physics proved it's real...",
            "angle": "Quantum mechanics defying the speed of light."
        }
    ],
    "Stoicism & Philosophy": [
        {
            "title_idea": "Marcus Aurelius' Brutal Rule for Never Getting Angry",
            "hook": "Marcus Aurelius woke up every morning and told himself one brutal sentence that made him immune to insults...",
            "angle": "Stoic contemplation of human nature and emotional armor."
        },
        {
            "title_idea": "Why Most People Realize This Rule Too Late in Life",
            "hook": "Seneca wrote that we suffer more often in imagination than in reality. Here is how to kill overthinking forever...",
            "angle": "Overcoming anxiety and mastering the present moment."
        }
    ],
    "Tech & AI Secrets": [
        {
            "title_idea": "The AI Experiment Scientists Had to Shut Down",
            "hook": "In 2017, two AI chatbots created their own secret language that humans could not decipher. What they said will chill you...",
            "angle": "Emergent communication in autonomous neural networks."
        }
    ],
    "Unsolved Mysteries": [
        {
            "title_idea": "The Missing Flight 370 Riddle That Defies Physics",
            "hook": "A Boeing 777 carrying 239 passengers completely vanished from military radar. Here is the satellite ping that nobody can explain...",
            "angle": "Unsolved aviation mystery and ocean anomalies."
        }
    ]
}


def research_topic(niche: str = "Psychology Facts", user_prompt: str = "") -> Dict[str, Any]:
    """
    Researches high-retention viral topics for YouTube Shorts.
    Uses Gemini API if available, else smart curated viral engine.
    """
    niche_info = NICHES.get(niche, NICHES["Psychology Facts"])
    tone = niche_info["tone"]

    if GEMINI_API_KEY and GEMINI_API_KEY.strip():
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=GEMINI_API_KEY)

            system_instruction = (
                f"You are a master YouTube Shorts strategist with over 100M views. "
                f"Your goal is to find the most viral, curiosity-inducing topic in the '{niche}' niche. "
                f"Tone: {tone}. "
                f"The topic MUST have an irresistible hook in the first 3 seconds, high psychological curiosity, "
                f"and be perfectly suited for a 50-second fast-paced vertical video."
            )

            prompt = (
                f"Generate a viral topic idea for a YouTube Short.\n"
                f"Niche: {niche}\n"
                f"User request or focus angle (if any): '{user_prompt or 'Trending high-retention viral topic'}'.\n\n"
                f"Return ONLY a valid JSON object with the following schema:\n"
                f"{{\n"
                f'  "title_idea": "Catchy YouTube Short title with high CTR (under 60 chars)",\n'
                f'  "hook": "3-second opening hook line that stops scrolling instantly",\n'
                f'  "angle": "Core revelation or shocking twist explored in the video",\n'
                f'  "target_audience": "Who this resonates with most"\n'
                f"}}"
            )

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.85
                )
            )

            data = json.loads(response.text)
            if "title_idea" in data and "hook" in data:
                return data

        except Exception as e:
            print(f"[Researcher] Gemini API notice: {e}. Using fallback viral topic library.")

    # Fallback to curated high-engagement viral concepts
    candidates = CURATED_FALLBACK_TOPICS.get(niche, CURATED_FALLBACK_TOPICS["Psychology Facts"])
    chosen = random.choice(candidates).copy()
    if user_prompt:
        chosen["title_idea"] = f"{user_prompt[:50]} (Revealed)"
    chosen["target_audience"] = f"Curious minds interested in {niche}"
    return chosen
