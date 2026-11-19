"""Talks to the AI provider (Google Gemini's OpenAI-compatible endpoint)."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()  # reads GEMINI_API_KEY from the .env file

API_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
DEFAULT_MODEL = "gemini-2.5-flash"  # change in .env with IKWUJE_MODEL if needed
SYSTEM_PROMPT = (
    "You are Ikwuje, a friendly and helpful AI assistant. "
    "Give clear, concise answers."
)


class AIError(Exception):
    """Raised with a friendly message when the AI call fails."""


def get_reply(messages):
    """Send the chat history to the AI and return its reply text."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise AIError("No GEMINI_API_KEY found. Add it to your .env file.")

    model = os.getenv("IKWUJE_MODEL", DEFAULT_MODEL)
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise AIError("The request timed out. Try again.")
    except requests.exceptions.HTTPError as error:
        status = error.response.status_code
        if status == 429:
            raise AIError("Rate limit reached (free tier). Wait a bit and retry.")
        if status in (400, 401, 403, 404):
            raise AIError(f"The API rejected the request ({status}). Check your key and model name.")
        raise AIError(f"The AI server had a problem ({status}).")
    except requests.exceptions.RequestException:
        raise AIError("Could not connect. Check your internet.")

    try:
        return response.json()["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError, AttributeError, ValueError):
        raise AIError("The AI sent back something unexpected.")
