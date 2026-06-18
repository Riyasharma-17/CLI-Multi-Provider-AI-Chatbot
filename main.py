from dotenv import load_dotenv
from groq import Groq
import os
import google.generativeai as genai

load_dotenv(override=True)

groq_api_key = os.getenv("GROQ_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = Groq(api_key=groq_api_key)
genai.configure(api_key=gemini_api_key)

gemini_model = genai.GenerativeModel(
    "gemini-2.0-flash"
)
print("Gemini initialized successfully.")

system_message = {
    "role": "system",
    "content": "You are a helpful assistant."
}

messages = [system_message]
print("Choose Provider:")
print("[1] Groq")
print("[2] Gemini")

choice = input("Enter choice: ")

if choice == "1":
    provider = "groq"

elif choice == "2":
    print("Gemini temporarily unavailable.")
    provider = "groq"
else:
    print("Invalid choice.")
    raise SystemExit

print("Using:" , provider)


while True:
    user_input = input("You: ")

    if user_input == "/quit":
        print("Goodbye!")
        break

    if user_input == "/clear":
        messages = [system_message]
        print("Conversation history cleared!")
        continue

    messages.append(    #here chats will get append at last one by one
        {
            "role": "user",  #role -> each role-persons may chnge.
            "content": user_input
        }
    )

    print(messages)

    
    if provider == "groq":
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        bot_reply = response.choices[0].message.content #Extracts text from Groq's response object.
    
    elif provider == "gemini":
        conversation = ""

        for message in messages:
            conversation += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        response = gemini_model.generate_content(conversation) #sends the whole transcript.

        bot_reply = response.text

    print("Bot:", bot_reply)
        


    
    messages.append(
{
    "role": "assistant",
    "content": bot_reply
}
)
    if provider == "groq":
        print("\nToken Usage:")
        print("Input Tokens:", response.usage.prompt_tokens)
        print("Output Tokens:", response.usage.completion_tokens)











#response:- Ye pura object hai jo API se aata hai jab tum client.chat.completions.create(...) call karte ho.
#Ye answers ek list (choices) mei hote hain