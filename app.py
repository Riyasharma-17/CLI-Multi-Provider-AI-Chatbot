from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio

from models.chat_models import ChatRequest, ChatResponse

from providers.groq_provider import (
    chat_with_groq,
    chat_with_groq_stream
)


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

@app.post("/chat")
def chat(request: ChatRequest):

    messages.append(
        {
            "role": "user",
            "content": request.message
        }
    )

    if request.stream:

        stream = chat_with_groq_stream(
            messages,
            request.temperature
        )

        async def generate():

            full_reply = ""

            for chunk in stream:

                token = chunk.choices[0].delta.content

                if token:

                    full_reply += token

                    yield token

            messages.append(
                {
                    "role": "assistant",
                    "content": full_reply
                }
            )

        return StreamingResponse(
            generate(),
            media_type="text/plain"
        )

    try:

        bot_reply, input_tokens, output_tokens = chat_with_groq(
            messages,
            request.temperature
        )

    except Exception:

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

@app.get("/stream-demo")
async def stream_demo():
    async def generate():
        yield "Hello "

        await asyncio.sleep(1)
        yield "from "

        await asyncio.sleep(1)
        yield "FastAPI!"

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )
