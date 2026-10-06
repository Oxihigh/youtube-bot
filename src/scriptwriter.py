import os
import json
from typing import Dict, Any, List
from src.config import GEMINI_API_KEY, NICHES, VISUAL_STYLES

# Curated high-retention fallback scripts with scene breakdowns
CURATED_SCRIPTS = {
    "The Dark Psychology Trick People Use to Manipulate You": {
        "title": "The Dark Psychology Trick Everyone Falls For 🧠 #shorts",
        "description": "Have you ever noticed someone pause before answering you? Watch out for this subtle manipulation technique. Subscribe for daily psychological revelations!\n\n#psychology #mindset #manipulation #darkpsychology #shorts #facts",
        "tags": ["psychology", "dark psychology", "human behavior", "body language", "shorts", "viral facts"],
        "scenes": [
            {
                "scene_num": 1,
                "text": "If someone pauses before answering your question, they aren't thinking. They're testing you.",
                "image_prompt": "mysterious person silhouette in dramatic shadowy room with single beam of light, intense intense stare, cinematic lighting"
            },
            {
                "scene_num": 2,
                "text": "This psychological tactic is known as the pregnant pause. Manipulators use deliberate silence to make you feel uncomfortable.",
                "image_prompt": "close-up of an enigmatic face in cinematic low-key lighting, clock ticking in the background, tense atmosphere"
            },
            {
                "scene_num": 3,
                "text": "Because human psychology hates unanswered tension, your instinct will be to fill the void by over-explaining or apologizing.",
                "image_prompt": "surreal artistic representation of tangled thoughts and glowing neurons inside a glass brain, dark moody aesthetic"
            },
            {
                "scene_num": 4,
                "text": "The moment you speak first, you surrender the psychological upper hand and reveal your insecurities.",
                "image_prompt": "chess board with dark glowing pieces, a king falling in slow motion, dramatic cinematic shadows"
            },
            {
                "scene_num": 5,
                "text": "Next time someone tries this on you, look them dead in the eye, smile slightly, and remain completely silent.",
                "image_prompt": "calm confident figure standing strong against a swirling tempest of shadows, golden rim light, stoic expression"
            },
            {
                "scene_num": 6,
                "text": "Because in the game of power, silence is the ultimate weapon.",
                "image_prompt": "an ancient golden hourglass with glowing sand falling against deep obsidian background, epic cinematic 8k"
            }
        ]
    },
    "default": {
        "title": "The Brutal Rule Most People Learn Too Late ⚡ #shorts",
        "description": "Marcus Aurelius and ancient stoics discovered this truth centuries ago. Once you see it, you can never unsee it.\n\n#stoicism #motivation #wisdom #philosophy #shorts",
        "tags": ["stoicism", "philosophy", "wisdom", "mindset", "shorts", "life lessons"],
        "scenes": [
            {
                "scene_num": 1,
                "text": "Marcus Aurelius woke up every morning and told himself one brutal sentence that changed everything.",
                "image_prompt": "ancient marble statue of Roman Emperor Marcus Aurelius lit by flickering torchlight, moody dark atmosphere"
            },
            {
                "scene_num": 2,
                "text": "He wrote: Today I will meet the meddling, the ungrateful, the arrogant, and the dishonest.",
                "image_prompt": "silhouette of Roman emperor looking over the ancient city of Rome at dusk, dramatic stormy sky, cinematic epic scale"
            },
            {
                "scene_num": 3,
                "text": "He wasn't being pessimistic. He was mentally inoculating himself against human betrayal before his day even started.",
                "image_prompt": "glowing ancient scroll with glowing Latin inscriptions surrounded by dark obsidian armor, cinematic rim light"
            },
            {
                "scene_num": 4,
                "text": "When you expect people to be flawless, you become fragile. When you expect the storm, you become the lighthouse.",
                "image_prompt": "towering stone lighthouse enduring crashing violent ocean waves during midnight storm, glowing beacon beam, cinematic"
            },
            {
                "scene_num": 5,
                "text": "Never let another person's ignorance disturb the stillness of your soul.",
                "image_prompt": "calm stoic warrior in meditation surrounded by glowing golden embers, stillness amidst chaos, masterpiece 8k"
            }
        ]
    }
}


def generate_script(
    topic_data: Dict[str, Any],
    niche: str = "Psychology Facts",
    style_key: str = "cinematic_dark"
) -> Dict[str, Any]:
    """
    Generates high-retention 45-55s YouTube Shorts script with:
    - Scene breakdown (text + visual prompts)
    - Full voiceover text
    - YouTube SEO Title, Description, and Tags
    """
    title_idea = topic_data.get("title_idea", "Viral Fact")
    hook = topic_data.get("hook", "")
    angle = topic_data.get("angle", "")
    niche_info = NICHES.get(niche, NICHES["Psychology Facts"])
    tone = niche_info["tone"]
    visual_style_prompt = VISUAL_STYLES.get(style_key, VISUAL_STYLES["cinematic_dark"])

    if GEMINI_API_KEY and GEMINI_API_KEY.strip():
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=GEMINI_API_KEY)

            system_instruction = (
                f"You are the world's #1 viral YouTube Shorts scriptwriter with billions of views. "
                f"You specialize in high-retention storytelling, curiosity loops, and high-CTR SEO. "
                f"Niche: {niche}. Tone: {tone}. "
                f"Visual Style: {visual_style_prompt}. "
                f"Script MUST be between 100 to 140 spoken words total (around 45-55 seconds spoken pace). "
                f"Split the script into 5 to 7 visual scenes. Each scene has 1-2 punchy sentences and a vivid image prompt."
            )

            prompt = (
                f"Write a viral YouTube Shorts script for the following topic:\n"
                f"Title Concept: {title_idea}\n"
                f"Opening Hook: {hook}\n"
                f"Core Angle: {angle}\n\n"
                f"REQUIREMENTS:\n"
                f"1. Start with an intense curiosity hook in Scene 1 (0-3s).\n"
                f"2. Maintain suspense with rapid information beats every 5-7 seconds.\n"
                f"3. Ending should be punchy, memorable, and loop back seamlessly to the beginning if possible.\n"
                f"4. For each scene, create an image prompt formatted for Pollinations/Flux AI image generation: "
                f"focus on subjects, cinematic lighting, moody atmosphere, NO text inside image, vertical aspect ratio 9:16.\n"
                f"5. Provide YouTube Title (under 60 chars with 1 emoji & #shorts), YouTube Description (compelling + hashtags), and 6-10 Tags.\n\n"
                f"Return ONLY valid JSON matching this schema:\n"
                f"{{\n"
                f'  "title": "Viral YouTube Shorts Title 🧠 #shorts",\n'
                f'  "description": "Engaging description text\\n\\n#hashtags",\n'
                f'  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],\n'
                f'  "scenes": [\n'
                f'    {{\n'
                f'      "scene_num": 1,\n'
                f'      "text": "Spoken sentence for scene 1",\n'
                f'      "image_prompt": "Cinematic visual description without text or logos"\n'
                f'    }}\n'
                f'  ]\n'
                f"}}"
            )

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.8
                )
            )

            data = json.loads(response.text)
            if "scenes" in data and len(data["scenes"]) >= 3:
                # Append style modifiers to each image prompt
                for sc in data["scenes"]:
                    base_prompt = sc.get("image_prompt", "")
                    sc["image_prompt"] = f"{base_prompt}, {visual_style_prompt}"
                data["full_script"] = " ".join(sc["text"] for sc in data["scenes"])
                return data

        except Exception as e:
            print(f"[Scriptwriter] Gemini API notice: {e}. Using curated high-retention script fallback.")

    # Fallback to curated script
    template = CURATED_SCRIPTS.get(title_idea, CURATED_SCRIPTS["default"]).copy()
    # Format prompts with chosen visual style
    scenes = []
    for sc in template["scenes"]:
        sc_copy = sc.copy()
        sc_copy["image_prompt"] = f"{sc_copy['image_prompt']}, {visual_style_prompt}"
        scenes.append(sc_copy)

    template["scenes"] = scenes
    template["full_script"] = " ".join(sc["text"] for sc in scenes)
    return template
