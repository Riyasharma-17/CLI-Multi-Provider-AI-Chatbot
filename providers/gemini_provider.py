# providers/gemini_provider.py

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv(override=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

gemini_model = genai.GenerativeModel(
    "gemini-2.0-flash"
)


def chat_with_gemini(messages):

    conversation = ""

    for message in messages:
        conversation += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    try:
        response = gemini_model.generate_content(
            conversation
        )

        bot_reply = response.text

        # Gemini token usage unavailable for now
        input_tokens = 0
        output_tokens = 0

        return (
            bot_reply,
            input_tokens,
            output_tokens
        )

    except Exception as e:

        return (
            f"Gemini Error: {e}",
            0,
            0
        )