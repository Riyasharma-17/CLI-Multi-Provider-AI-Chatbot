# CLI Multi-Provider AI Chatbot

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-green)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue)](https://docker.com)
[![Render](https://img.shields.io/badge/Render-Live-purple)](https://cli-multi-provider-ai-chatbot.onrender.com/docs)
[![Tests](https://img.shields.io/badge/Tests-10%20passed-brightgreen)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

> Multi-provider AI chatbot — CLI → FastAPI → Deployed. Groq, Gemini, and OpenRouter behind one interface. Built without frameworks first, then with LangChain to understand the difference.

**[Live API](https://cli-multi-provider-ai-chatbot.onrender.com) · [Swagger Docs](https://cli-multi-provider-ai-chatbot.onrender.com/docs)**

---

## What Was Built

| Phase | What | Stack |
|---|---|---|
| 1 | CLI chatbot — memory, system prompts, JSON mode | Python, Groq, Gemini, OpenRouter |
| 2 | REST API — same logic, HTTP interface | FastAPI, Pydantic, Streaming |
| 3 | LangChain integration — chains, memory, output parsers | LangChain, LCEL |
| 4 | Containerized + deployed | Docker, Render |

Each phase built on the previous one without rewriting what already worked.

---

## Live Demo

```bash
# Try it now
curl -X POST https://cli-multi-provider-ai-chatbot.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is RAG?", "provider": "groq"}'
```

Or open the [Swagger UI](https://cli-multi-provider-ai-chatbot.onrender.com/docs) — no setup needed.

---

## Architecture

```
CLI Input / HTTP Request
         │
         ▼
  ┌─────────────┐
  │   Router    │  /chat · /history · /stream-demo
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │  LangChain  │  ChatPromptTemplate → LLM → StrOutputParser
  │    Chain    │  ConversationBufferMemory
  └──────┬──────┘
         │
         ▼
  ┌─────────────────────────────┐
  │      Provider Adapter       │  common interface — swap without touching app logic
  ├──────────┬──────────┬───────┤
  │   Groq   │  Gemini  │  OR   │  OpenRouter
  └──────────┴──────────┴───────┘
         │
         ▼
  Normal Response / StreamingResponse
```

The provider layer predates LangChain in this project — it was written from scratch first, which is why the LangChain integration sits *above* it rather than replacing it.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/chat` | Chat — normal or streaming (`stream: true`) |
| `GET` | `/history` | Current conversation history |
| `DELETE` | `/history` | Clear history, preserve system prompt |
| `GET` | `/stream-demo` | Streaming response demo |

---

## Project Structure

```
├── app.py                    # FastAPI — routes, streaming, CORS
├── main.py                   # CLI entry point
│
├── providers/
│   ├── groq_provider.py      # OpenAI-compatible adapter
│   ├── gemini_provider.py    # Transcript-based memory adapter
│   └── openrouter_provider.py
│
├── models/
│   └── chat_models.py        # Pydantic request/response models
│
├── utils/
│   ├── json_utils.py         # Defensive JSON parsing
│   ├── system_utils.py       # System prompt construction
│   ├── command_utils.py      # /quit /clear
│   ├── json_mode_utils.py
│   └── provider_utils.py
│
├── tests/                    # pytest — 10 passing
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
| **LLMs** | Groq · Gemini · OpenRouter | Three structurally different APIs — free tier |
| **Orchestration** | LangChain + LCEL | Chains, memory, output parsers — learned by building without it first |
| **Backend** | FastAPI | Async, Pydantic validation, streaming, auto docs |
| **Testing** | pytest + unittest.mock | Provider tests run without real API calls |
| **Deploy** | Docker + Render | Containerized, auto-deploys on push |

---

## Key Decisions

**Built the adapter pattern before adding LangChain.**
Understanding what LangChain abstracts required building it manually first — message formatting, memory serialization, provider normalization. LangChain now sits above the provider layer, not instead of it.

**One `/chat` endpoint for normal and streaming.**
Single endpoint with a `stream` flag instead of two separate routes. Simpler API surface, backward compatible.

**Refactored before adding the third provider.**
`main.py` was doing everything by Day 5. Splitting into `providers/` and `utils/` before adding OpenRouter meant the third provider took an hour. Abstraction pays on the third use, not the second.

**Defensive JSON parsing everywhere.**
Prompting for JSON doesn't guarantee JSON. Every parse is wrapped in `try/except`, every key access uses `.get()`. Tests verify the failure paths, not just the happy path.

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
# .env
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
OPENROUTER_API_KEY=your_key
```

```bash
python main.py          # CLI
uvicorn app:app --reload  # API → localhost:8000/docs
pytest                  # Tests
```

**Docker:**
```bash
docker build -t cli-chatbot .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key cli-chatbot
```

---

## What I Learned

- LangChain's value is obvious only after building what it replaces
- Provider APIs are not interchangeable — memory, message format, and errors all differ per SDK
- `return` vs `yield` in Python determines whether a response streams or blocks
- Infrastructure failures and code bugs look identical until you isolate the layer
- Separation of concerns is what allowed the same provider code to power a CLI, a REST API, and a LangChain chain without modification

---

## Roadmap

- [x] Multi-provider CLI
- [x] FastAPI backend
- [x] LangChain integration
- [x] Streaming responses
- [x] Docker + Render deployment
- [x] 10 passing tests
- [ ] Persistent history (SQLite)
- [ ] Retry + exponential backoff
- [ ] Streaming for Gemini + OpenRouter
- [ ] Configurable JSON schemas

---

*Started as a CLI. Became an API. Deployed to production. Built to understand the full stack of an LLM application — not just the model call.*