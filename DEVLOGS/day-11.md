📒 Day 11 Documentation (Streaming Responses)
Day 11 — Implementing Real-Time Streaming Responses
Objective

Today's goal was to upgrade the chatbot from a traditional request-response API into a real-time streaming API, similar to how ChatGPT, Claude, and Gemini display text as it is generated.

Instead of waiting for the complete answer before responding, the backend now streams tokens one by one while still preserving conversation memory.

What I Learned
1. Blocking vs Streaming

Initially, my chatbot followed the standard request-response pattern.

User
    ↓
API Request
    ↓
LLM generates full response
    ↓
Return complete reply

Although simple, users had to wait until the entire answer was generated.

Streaming changes only when the client receives data—not how fast the LLM thinks.

User
    ↓
LLM generates tokens
    ↓
Token
Token
Token
    ↓
Client receives text immediately

This significantly improves the perceived responsiveness of the application.

2. Async Generators

I learned why streaming cannot be implemented using a normal return.

A normal function finishes execution immediately after returning.

Generators behave differently—they produce one value, pause execution, and resume from the same point when requested again.

Using an async generator allows FastAPI to continuously send newly generated tokens without blocking the server.

3. FastAPI StreamingResponse

Before integrating the LLM, I created a simple /stream-demo endpoint to understand FastAPI's streaming mechanism independently.

This isolated experiment helped verify that the framework could stream responses correctly before introducing provider-specific logic.

4. Groq Streaming

Instead of requesting the complete response at once, I enabled:

stream=True

Groq now returns an iterator that produces small response chunks rather than one final string.

This required changing the processing flow from handling a single response object to iterating over streamed chunks.

5. Integrating Streaming into /chat

Rather than creating a separate /chat-stream endpoint, I extended the existing /chat API.

A new field:

stream: bool = False

was added to the request model.

The endpoint now supports two behaviors:

stream = False → Existing JSON response.
stream = True → Live token streaming.

This preserved backward compatibility while keeping the API clean and maintainable.

6. Conversation Memory Challenge

The biggest architectural challenge was maintaining conversation history during streaming.

Streaming delivers partial chunks:

Py
thon
 is
 awesome

Saving every chunk individually would corrupt the conversation history.

Instead, I accumulated every token into a temporary variable (full_reply) while simultaneously streaming those tokens to the client.

After streaming completed, only the final assembled response was stored in the conversation history.

This preserves clean chat history while still providing real-time output.

Key Technical Concepts Learned
Blocking vs Streaming APIs
Async generators
yield vs return
FastAPI StreamingResponse
Groq stream=True
Iterator-based streaming
Conversation state management during streaming
Backward-compatible API design
Early-return branching inside API endpoints
Final Outcome

The chatbot now supports both standard and streaming conversations using the same /chat endpoint.

Streaming responses appear progressively while the backend safely reconstructs and stores the complete assistant reply, ensuring future conversation context remains accurate.

This implementation closely mirrors the architecture used by modern AI chat applications while keeping the project modular and easy to extend.