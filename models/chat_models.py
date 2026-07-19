from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    provider: str = "groq"
    temperature: float = 0.7
    stream: bool = False


class ChatResponse(BaseModel):
    reply: str
    provider: str
    input_tokens: int
    output_tokens: int