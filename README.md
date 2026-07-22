# CLI Multi-Provider AI Chatbot

A chatbot that talks to Groq, Gemini, and OpenRouter through one unified interface — built as a CLI first, then a REST API, then wrapped with LangChain, then given a Gradio UI. Each phase added without rewriting what came before.

>A production-style multi-provider AI chatbot supporting Groq, Gemini, and OpenRouter through a unified FastAPI backend with LangChain orchestration and a Gradio frontend.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-green)](https://fastapi.tiangolo.com)
[![Gradio](https://img.shields.io/badge/Gradio-UI-orange)](https://multi-provider-ai-chatbot-ui.onrender.com)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue)](https://docker.com)
[![Render](https://img.shields.io/badge/Render-Live-purple)](https://cli-multi-provider-ai-chatbot.onrender.com/docs)
[![Tests](https://img.shields.io/badge/Tests-10%20passed-brightgreen)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

**[Live UI](https://multi-provider-ai-chatbot-ui.onrender.com) · [Live API](https://cli-multi-provider-ai-chatbot.onrender.com) · [Swagger Docs](https://cli-multi-provider-ai-chatbot.onrender.com/docs)**

---

## What Was Built

| Phase | What | Stack |
|---|---|---|
| 1 | CLI chatbot — memory, system prompts, JSON mode | Python, Groq, Gemini, OpenRouter |
| 2 | REST API — same logic, HTTP interface | FastAPI, Pydantic, Streaming |
| 3 | LangChain integration — chains, memory, output parsers | LangChain, LCEL |
| 4 | Gradio frontend — chat UI, provider selector, temperature | Gradio |
| 5 | Containerized + deployed — two services, one repo | Docker, Render |


---

## Live Demo

**Try the UI (no setup):**
👉 [multi-provider-ai-chatbot-ui.onrender.com](https://multi-provider-ai-chatbot-ui.onrender.com)

**Or hit the API directly:**
```bash
curl -X POST https://cli-multi-provider-ai-chatbot.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is RAG?", "provider": "groq"}'
```
## Features

- Multi-provider support (Groq, Gemini, OpenRouter)
- Unified FastAPI API
- LangChain integration
- Adjustable temperature
- Streaming responses
- Conversation history
- Dockerized deployment
- Independent Gradio frontend

**Sample response:**
```json
{
  "provider": "groq",
  "response": "RAG (Retrieval-Augmented Generation) retrieves relevant documents from a knowledge base and passes them as context to an LLM before generating an answer — improving accuracy without retraining the model.",
  "tokens_used": 142
}
```

---

## Architecture

```
                    ┌─────────────────────┐
                    │     Gradio UI        │  provider selector · temperature · chat
                    └──────────┬──────────┘
                               │ HTTP
                               ▼
          ┌────────────────────────────────────┐
          │           FastAPI Backend           │  /chat · /history · /stream-demo
          │     Pydantic · CORS · Streaming     │
          └──────────────┬─────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────────┐
          │         LangChain Chain           │
          │  Prompt → LLM → OutputParser      │
          │  ConversationBufferMemory         │
          └──────────────┬───────────────────┘
                         │
                         ▼
          ┌──────────────────────────────────┐
          │        Provider Adapter          │  common interface
          ├───────────┬──────────┬───────────┤
          │   Groq    │  Gemini  │ OpenRouter │
          └───────────┴──────────┴───────────┘
                         │
                         ▼
              Normal / StreamingResponse
```

**Deployment: one repo, two Render services**

```
GitHub Repo
    ├── / (root)          →  Render Service 1: FastAPI Backend
    └── /gradio_ui        →  Render Service 2: Gradio Frontend
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/chat` | Chat — normal or streaming (`stream: true`) |
| `GET` | `/history` | Current conversation history |
| `DELETE` | `/history` | Clear history, preserve system prompt |
| `GET` | `/stream-demo` | Streaming demo |

---

## Project Structure

```
├── app.py                      # FastAPI backend
├── main.py                     # CLI entry point
│
├── providers/
│   ├── groq_provider.py        # OpenAI-compatible adapter
│   ├── gemini_provider.py      # Transcript-based memory adapter
│   └── openrouter_provider.py
│
├── models/
│   └── chat_models.py          # Pydantic models
│
├── utils/
│   ├── json_utils.py           # Defensive JSON parsing
│   ├── system_utils.py
│   ├── command_utils.py
│   ├── json_mode_utils.py
│   └── provider_utils.py
│
├── gradio_ui/
│   ├── app.py                  # Gradio frontend — calls FastAPI via HTTP
│   └── requirements.txt
│
├── tests/
│   ├── test_api.py
│   ├── test_json_utils.py
│   ├── test_groq_provider.py
│   ├── test_gemini_provider.py
│   └── test_openrouter_provider.py
│
├── Dockerfile
├── requirements.txt
└── .env
```

---

## Tech Stack

| | Tool | Why |
|---|---|---|
| **LLMs** | Groq · Gemini · OpenRouter | Three structurally different APIs on free tier |
| **Orchestration** | LangChain + LCEL | Built without it first — added after understanding what it replaces |
| **Backend** | FastAPI | Async, Pydantic, streaming, Swagger UI |
| **Frontend** | Gradio | Lightweight chat UI — deployed independently from backend |
| **Testing** | pytest + unittest.mock | Runs without real API calls or network |
| **Deploy** | Docker + Render | One repo, two services, auto-deploy on push |

---

## Key Decisions

**Built the adapter pattern before adding LangChain.**
Wrote message formatting, memory serialization, and provider normalization from scratch first. LangChain was added after — so its abstractions are understood, not just used.

**Gradio calls FastAPI over HTTP, not as an import.**
The frontend and backend are decoupled — Gradio is a separate Render service that makes HTTP requests to the API. Swapping the frontend for React or any other UI requires zero backend changes.

**One `/chat` endpoint for normal and streaming.**
Single endpoint with a `stream` flag. Simpler surface, backward compatible.

**Refactored before extending.**
`main.py` was doing everything by Day 5. Split into `providers/` and `utils/` before adding the third provider. The third provider took an hour because of it.

**Defensive JSON parsing everywhere.**
LLMs don't guarantee valid JSON when you ask for it. Every parse is `try/except`, every key access is `.get()`. Tests cover the failure paths.

---

## Testing

```
10 passed
```

| What | Coverage |
|---|---|
| JSON utils | Valid, malformed, plain text |
| Groq / Gemini / OpenRouter | Success + failure paths |
| FastAPI endpoints | POST · GET · DELETE |

All provider tests use `unittest.mock` — no network, no API keys, runs anywhere.

---

## Demos

![CLI Demo](clibot.gif)
*Provider selection · system prompts · memory · JSON mode*

![FastAPI Demo](cli_fastapi.gif)
*Swagger UI · streaming · history endpoints*

---

## Run Locally

```bash
git clone https://github.com/Riyasharma-17/CLI-Multi-Provider-AI-Chatbot
cd CLI-Multi-Provider-AI-Chatbot
pip install -r requirements.txt
```

```env
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
OPENROUTER_API_KEY=your_key
```

```bash
# CLI
python main.py

# FastAPI backend
uvicorn app:app --reload
# → http://localhost:8000/docs

# Gradio frontend (separate terminal)
cd gradio_ui
pip install -r requirements.txt
python app.py
# → http://localhost:7860

# Tests
pytest
```

**Docker:**
```bash
docker build -t cli-chatbot .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key cli-chatbot
```

---

## What I Learned

- LangChain's value is obvious only after building what it replaces
- Decoupling frontend and backend means each can be deployed, scaled, and replaced independently
- `return` vs `yield` in Python is the difference between blocking and streaming responses
- Infrastructure failures and code bugs look identical — isolate the layer before debugging
- The same provider code powered a CLI, a REST API, a LangChain chain, and a Gradio UI without modification — that's what separation of concerns actually looks like

---

## Roadmap

- [x] Multi-provider CLI
- [x] FastAPI backend
- [x] LangChain integration
- [x] Streaming responses
- [x] Gradio frontend
- [x] Docker + Render deployment (two services)
- [x] 10 passing tests
- [ ] Persistent history (SQLite)
- [ ] Retry + exponential backoff
- [ ] Streaming for Gemini + OpenRouter
- [ ] Configurable JSON schemas

---

*Started as a CLI. Became an API. Got a UI. Deployed to production. Built to understand the full stack of an LLM application — not just the model call.*