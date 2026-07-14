"""
Handles the actual call to the Gemini API using Google's current
unified SDK (google-genai), which supports the newer Auth-style
API keys (the ones starting with "AQ.").
"""

import os
from google import genai
from google.genai import types
from chatbot.prompts import SYSTEM_PROMPT

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"  # fast, free-tier friendly model


def ask_ai(context: str, chat_history: list[dict], user_question: str) -> str:
    """
    context: string built by chatbot/context.py (property + metrics + risk)
    chat_history: list of {"role": "user"/"assistant", "content": "..."} from previous turns
    user_question: the new message from the user

    Returns the assistant's reply as a string.
    """
    gemini_history = []
    for msg in chat_history:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
        )

    chat = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT + "\n\n" + context,
            temperature=0.4,
        ),
        history=gemini_history,
    )

    response = chat.send_message(user_question)
    return response.text