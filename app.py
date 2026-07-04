from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from providers.groq_provider import chat_with_groq
from models.chat_models import ChatRequest, ChatResponse


messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant"
    }
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    messages.append(
        {
            "role": "user",
            "content": request.message
        }
    )

    try:
        bot_reply, input_tokens, output_tokens = chat_with_groq(
            messages,
            request.temperature
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unable to contact AI provider. Please try again later."
        )

    messages.append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )

    return ChatResponse(
        reply=bot_reply,
        provider="groq",
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )


@app.get("/history")
def get_history():

    return messages


@app.delete("/history")
def clear_history():

    messages.clear()

    messages.append(
        {
            "role": "system",
            "content": "You are a helpful assistant"
        }
    )

    return {
        "message": "History cleared successfully."
    }