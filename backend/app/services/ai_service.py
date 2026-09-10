"""
ai_service.py - The AI brain of materia-AI.

Takes a dish (name, ingredients, tone) and asks Google's Gemini API to
generate professional, appetizing menu descriptions in both Spanish
and English. Returns them as a structured response.
"""

import json
from google import genai

from app.config import settings
from app.schemas import MenuItemRequest, MenuDescriptionResponse

# One shared client, authenticated with the key from config.
client = genai.Client(api_key=settings.gemini_api_key)


def _build_prompt(item: MenuItemRequest) -> str:
    """Builds the instruction we send to the AI.

    Good prompt design is what separates generic output from copy that
    actually sells. We ask for strict JSON so the response is easy to
    parse reliably.
    """
    return (
        f"You are an expert restaurant copywriter.\n"
        f"Write an {item.tone}, professional menu description for this dish.\n\n"
        f"Dish name: {item.name}\n"
        f"Ingredients / notes: {item.ingredients}\n\n"
        f"Requirements:\n"
        f"- One description in natural Spanish (2 sentences max).\n"
        f"- One description in natural English (2 sentences max).\n"
        f"- Make it appetizing, not generic. Evoke the senses.\n"
        f"- Do NOT invent ingredients that aren't implied.\n\n"
        f"Respond ONLY with valid JSON, no extra text, in this exact shape:\n"
        f'{{"description_es": "...", "description_en": "..."}}'
    )


def generate_description(item: MenuItemRequest) -> MenuDescriptionResponse:
    """Calls the AI and returns bilingual menu descriptions."""

    prompt = _build_prompt(item)

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )
    except Exception as error:
        # Anything that fails here is a connection/API problem —
        # network issues, quota limits, auth errors, etc.
        raise ConnectionError(f"Could not reach the AI provider: {error}") from error

    # The AI's reply comes back as text; we expect JSON inside it.
    raw_text = response.text.strip()

    # Parse the JSON. If the AI ever wraps it in markdown fences,
    # strip them defensively before parsing.
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(cleaned)
        description_es = data["description_es"]
        description_en = data["description_en"]
    except (json.JSONDecodeError, KeyError) as error:
        # The model responded, but not in the shape we asked for.
        raise ValueError(f"AI returned an unexpected format: {error}") from error

    return MenuDescriptionResponse(
        name=item.name,
        description_es=description_es,
        description_en=description_en,
    )
