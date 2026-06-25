from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key
)

MODEL_NAME = "openrouter/free"

def chat_with_openrouter(messages, temperature):
    try:
        response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature
        )

        bot_reply = response.choices[0].message.content

        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        return (
            bot_reply,
            input_tokens,
            output_tokens
        )
    
    except Exception as e:

        return (
            f"OpenRouter Error: {e}",
            0,
            0
        )