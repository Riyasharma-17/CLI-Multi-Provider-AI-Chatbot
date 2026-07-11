from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv(override=True)

groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)


def chat_with_groq(messages, temperature):

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
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
            f"Groq Error: {e}",
            0,
            0
        )
    
def chat_with_groq_stream(messages,temperature):
    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages=messages,
        temperature=temperature,
        stream=True
    )

    return response


#Extracts text from Groq's response object.