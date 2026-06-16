from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv(override=True)

groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Explain recursion in one sentence."}]
)

print(response.choices[0].message.content)
print("\nToken Usage:")
print("Input Tokens:", response.usage.prompt_tokens)
print("Output Tokens:", response.usage.completion_tokens)