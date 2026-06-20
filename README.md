# CLI Multi-Provider AI Chatbot

> A command-line chatbot that talks to Groq, Gemini, or OpenRouter through one unified interface — switch providers without touching application logic.

---

## What This Is

Most beginner chatbot projects hardcode a single API call and stop there. This one is built around a harder, more useful question: what happens when you need to support more than one LLM provider, and they don't agree on how to do anything?

Groq follows the OpenAI-compatible message format. Gemini doesn't. Each has different SDKs, different ways of handling conversation history, different error behavior, and different quota systems. This project builds a common interface across all three — so the application layer never needs to know which provider is actually answering.

The result is a working CLI chatbot with memory, customizable system prompts, structured JSON output, and runtime provider switching.

---

## The Problem

If you build a chatbot around one provider's SDK, you've built a chatbot that breaks the moment that provider hits a rate limit, deprecates a model, or goes down. Real systems need to be provider-agnostic.

The harder problem: providers don't share a common API shape.

- Groq exposes an OpenAI-compatible `messages` list (`system` / `user` / `assistant` roles)
- Gemini does not — conversation history has to be serialized differently
- Each SDK has its own client setup, error types, and response structure

This project solves that by designing a common interface and writing a dedicated adapter per provider behind it — a small-scale version of the abstraction pattern real systems use to stay vendor-independent.

---

## How It Works

```
                    ┌─────────────────┐
                    │   CLI Input     │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Command Router     │  ← /quit, /clear, /json
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Conversation State  │  ← messages list (system/user/assistant)
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Provider Selector   │  ← chosen at startup
                  └──────────┬───────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌───────────┐  ┌───────────┐  ┌──────────────┐
       │   Groq    │  │  Gemini   │  │  OpenRouter   │
       │ Provider  │  │ Provider  │  │   Provider    │
       └─────┬─────┘  └─────┬─────┘  └──────┬────────┘
             │              │               │
             └──────────────┼───────────────┘
                             ▼
                  ┌─────────────────────┐
                  │   Common Response    │  ← normalized output, regardless of provider
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  JSON Mode Handler   │  ← optional structured parsing
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Output to CLI      │
                  └─────────────────────┘
```

Each provider module implements the same contract: take conversation history in, return a normalized response out. The rest of the application never branches on which provider is active.

---

## Project Structure

```
cli-multi-provider-chatbot/
│
├── main.py                    # Application controller — orchestrates the chat loop
│
├── providers/
│   ├── groq_provider.py       # Groq API adapter (OpenAI-compatible)
│   ├── gemini_provider.py     # Gemini API adapter (transcript-based memory)
│   └── openrouter_provider.py # OpenRouter API adapter
│
├── utils/
│   ├── json_utils.py          # JSON parsing, validation, pretty-printing
│   ├── system_utils.py        # System prompt construction
│   ├── command_utils.py       # /quit, /clear command handling
│   ├── json_mode_utils.py     # JSON mode detection and routing
│   └── provider_utils.py      # Provider selection logic
│
├── .env                        # API keys (not committed)
├── requirements.txt
└── README.md
```

`main.py` does not know how Gemini formats a prompt. `groq_provider.py` does not know what JSON mode is. Each module owns exactly one responsibility — which is what made it possible to add a third provider (OpenRouter) without touching the first two.

---

## Tech Stack

| Component | Choice | Why |
|---|---|---|
| LLM Providers | Groq, Gemini, OpenRouter | All offer usable free tiers — good for comparing API design without cost pressure |
| Provider interface | Custom adapter pattern | No existing abstraction fit three structurally different APIs cleanly |
| Structured output | Prompt-engineered JSON + `json.loads()` | LLMs don't guarantee valid JSON — defensive parsing required |
| Env management | `python-dotenv` | Standard practice for API key security |
| Architecture | Modular (`providers/`, `utils/`) | Built after the monolithic version became hard to extend |

LangChain was deliberately not used. The goal was to understand what a provider abstraction layer actually has to handle — message formatting, memory serialization, error normalization — before relying on a framework to hide it.

---

## Key Engineering Decisions

### Provider Abstraction Before Adding a Third Provider

The first version hardcoded Groq calls directly into the main loop. Adding Gemini meant duplicating the loop with provider-specific branches, which immediately became unmaintainable. The fix was defining a common interface (`chat_with_provider(messages) → response`) before adding OpenRouter, so the third provider took a fraction of the effort the second one did.

### Memory Simulation for Non-Compatible APIs

Groq accepts a `messages` list directly. Gemini does not work the same way — conversation history had to be serialized into a single transcript string per call. This meant building a translation layer between the application's internal message format and what each provider's SDK actually expects.

### Defensive JSON Parsing

Prompting a model to "return JSON" does not guarantee valid JSON. Malformed output, missing fields, and inconsistent formatting all happened during testing. The fix was wrapping all parsing in `try/except` around `json.loads()`, using `.get()` instead of direct key access, and never letting a bad response crash the conversation loop.

### Refactor Before Feature Creep

By Day 5, `main.py` had grown into a single file handling routing, provider logic, JSON parsing, and command handling at once. Refactoring into `providers/` and `utils/` happened before adding OpenRouter — adding a third provider to the monolithic version would have made the file close to unreadable.

---

## Challenges

**Providers fail differently, and the application has to survive all of them.**

Gemini's free tier hit quota limits during development. Initially this looked like a code bug. It wasn't. Distinguishing an infrastructure failure (rate limit, deprecated model name) from an actual logic error required reading error messages carefully and testing providers independently rather than assuming the most recent code change broke something.

This shaped the exception handling strategy: provider failures are caught and reported, not allowed to crash the whole application.

**Conversation memory isn't a universal concept across APIs.**

"Memory" in this project means resending the full conversation on every call. Groq supports this natively through its message list. Gemini required manually reconstructing a transcript on every turn — a reminder that "the model remembers" is an illusion the application maintains, not something the API does on its own.

---

## What I Learned

- **Abstraction earns its cost only when you actually need it twice.** The interface design for two providers looked over-engineered until the third provider took an hour instead of a day.
- **LLM APIs are not interchangeable**, even when they solve the same problem. Message formats, memory handling, and error types all differ — switching providers is real integration work, not a config change.
- **Defensive programming matters more with LLM output than typical APIs.** A REST API has a schema. An LLM asked for JSON is making a best effort. Code has to assume the response might be wrong.
- **Refactor when the file becomes hard to extend, not when it becomes hard to read.** The monolith was still readable at Day 4 — it was extending it that became painful, which was the actual signal to modularize.
- **Infrastructure problems and code problems look identical from the outside.** A quota error and a logic bug can produce the same symptom. Isolating the provider in question before debugging the application saved time.

---

## Limitations

This is a learning project, and a few gaps are intentional scope cuts rather than oversights:

- **No streaming responses** — replies are returned in full, not token-by-token
- **No persistent storage** — conversation history resets when the program exits
- **No automated tests** — provider adapters were verified manually
- **No retry/backoff logic** — a failed call requires the user to retry manually
- **Single JSON schema** — structured output mode uses a fixed `topic` / `summary` shape, not a configurable one

---

## Future Improvements

- [ ] Add streaming output for real-time response display
- [ ] Persist conversation history to disk (JSON or SQLite) between sessions
- [ ] Add retry logic with exponential backoff for transient API failures
- [ ] Support configurable JSON schemas instead of a single fixed structure
- [ ] Add unit tests for each provider adapter using mocked API responses
- [ ] Token usage tracking across all three providers, not just Groq

---

## Running Locally

```bash
git clone https://github.com/Riyasharma-17/CLI-Multi-Provider-AI-Chatbot
cd CLI-Multi-Provider-AI-Chatbot
pip install -r requirements.txt
```

Create a `.env` file with whichever provider keys you have:
```
GROQ_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
```

Run it:
```bash
python main.py
```

You'll be prompted to choose a provider, then optionally set a custom system prompt. Commands available mid-conversation:

| Command | Effect |
|---|---|
| `/quit` | Exit the chatbot |
| `/clear` | Reset conversation history (system prompt preserved) |
| `/json` | Toggle structured JSON output mode |

---

*Built to understand what a real provider-agnostic AI integration actually requires — message formatting, memory handling, and failure isolation — before relying on a framework to abstract it away.*