# Day 1 — From Python Script to First AI API Call

## Goal

Build the foundation of a CLI AI chatbot and successfully make the first API call to an LLM.

---

# What We Built

At the beginning of the day, the project was just an empty folder.

By the end of the day:

```text
Python Program
      ↓
Groq SDK
      ↓
Llama 3.1 8B
      ↓
AI Response
```

The application can now send a prompt to a real AI model and receive a response.

---

# Project Structure

Created a professional project structure:

```text
cli-qa-bot/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── main.py
└── README.md
```

Purpose of each file:

* `.env` → stores secret API keys
* `.env.example` → template for other developers
* `.gitignore` → prevents secrets from reaching GitHub
* `requirements.txt` → stores project dependencies
* `main.py` → application entry point
* `README.md` → project documentation

---

# Virtual Environment

Created a Python virtual environment:

```bash
python -m venv venv
```

Why?

Without virtual environments:

```text
All projects
     ↓
Share same packages
     ↓
Version conflicts
```

With virtual environments:

```text
Project A → Own packages
Project B → Own packages
```

Each project becomes isolated.

---

# Installing Dependencies

Installed:

```text
groq
google-generativeai
python-dotenv
```

What they do:

### groq

Allows Python to communicate with Groq's API.

### google-generativeai

Will later allow communication with Gemini.

### python-dotenv

Loads environment variables from a `.env` file.

---

# API Keys and Security

Learned why API keys should never be hardcoded.

Bad:

```python
api_key = "gsk_xxxxx"
```

Problems:

* Can be leaked accidentally
* Can be pushed to GitHub
* Anyone can use your API account

Correct:

```python
api_key = os.getenv("GROQ_API_KEY")
```

Store secrets in:

```text
.env
```

instead of source code.

---

# Loading Environment Variables

Used:

```python
load_dotenv()
```

to load values from:

```text
.env
```

Then accessed them using:

```python
os.getenv("GROQ_API_KEY")
```

Flow:

```text
.env
   ↓
load_dotenv()
   ↓
Environment Variables
   ↓
os.getenv()
```

---

# First Real AI API Call

Created a Groq client:

```python
client = Groq(api_key=groq_api_key)
```

Then sent a request:

```python
response = client.chat.completions.create(...)
```

Request Flow:

```text
User Prompt
      ↓
Groq API
      ↓
Llama 3.1 8B
      ↓
Generated Response
```

This was the first successful interaction with a real LLM.

---

# Understanding Messages

Even a single prompt is sent as:

```python
messages = [
    {
        "role": "user",
        "content": "..."
    }
]
```

Why a list?

Because later a conversation will contain:

```text
System Message
User Message
Assistant Reply
User Message
Assistant Reply
```

All stored in sequence.

---

# Debugging Adventure

The biggest lesson of Day 1 was debugging.

Initially:

```text
Hardcoded API Key → Works
.env API Key → Fails
```

This looked confusing because both keys appeared correct.

Investigation process:

```text
Check code
      ↓
Check SDK
      ↓
Check API key format
      ↓
Compare values
      ↓
Find root cause
```

Eventually discovered:

```python
load_dotenv(override=True)
```

was required.

Reason:

An older environment variable already existed somewhere on the system.

Without:

```python
load_dotenv()
```

the old value remained.

With:

```python
load_dotenv(override=True)
```

the value from `.env` replaced the old one.

Result:

```text
Correct Key Loaded
       ↓
Authentication Success
       ↓
API Call Works
```

---

# GitHub Security Lesson

While pushing code:

GitHub blocked the push.

Reason:

A real API key had accidentally been committed.

GitHub Push Protection detected:

```text
Groq API Key
```

inside the repository and refused the push.

Lesson learned:

```text
Never commit secrets.
```

Security tools exist for a reason.

---

# Key Concepts Learned

### Virtual Environments

Project isolation.

### Environment Variables

Secure secret management.

### SDKs

Libraries that communicate with external services.

### APIs

A way for software to communicate with other software.

### LLM Requests

Prompt → Model → Response.

### Authentication

API keys prove who is making requests.

### Debugging

Never guess.

Verify assumptions with evidence.

---

# End of Day 1

Current capability:

```text
Python
   ↓
Groq API
   ↓
Llama 3.1
   ↓
Response Returned
```

The foundation of the chatbot is complete.

Next step:

```text
Conversation Loop
      ↓
Chat Memory
      ↓
Real CLI Chatbot
```
