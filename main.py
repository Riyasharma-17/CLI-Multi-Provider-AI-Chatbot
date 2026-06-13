from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
print(repr(groq_api_key))

if not groq_api_key:
    print("Error: GROQ_API_KEY not found.")
    raise SystemExit


client = Groq(api_key=groq_api_key)

response = client.chat.completions.create( #Sends a chat completion request.
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role" : "user",
            "content" : "Explain recursion in one sentence."
        }
    ]
)

print(response.choices[0].message.content)
