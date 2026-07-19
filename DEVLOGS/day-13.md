# Day 13 – LangChain Integration & Model Abstraction

## Goal

Integrate LangChain into the existing FastAPI chatbot without breaking the clean architecture already built.

Instead of using LangChain just for the sake of it, understand **where it adds value** and **where manual implementation is actually better**.

---

# Phase 1 – Understanding LangChain Memory

## Problem

Initially, the plan was to replace our manual `messages` list with LangChain Memory.

Current chatbot:

User
↓
messages[]
↓
Groq API
↓
Assistant Reply

---

## Research

After learning the latest LangChain architecture, we found that:

- `ConversationBufferMemory` is deprecated.
- LangChain now recommends `RunnableWithMessageHistory` or LangGraph.
- Our current manual memory is already clean and maintainable.

---

## Decision

We intentionally **did not migrate memory**.

Reason:

- Simpler
- Easier to debug
- No unnecessary framework dependency
- Fits the scope of this chatbot

### Engineering Lesson

Use a framework only when it reduces complexity.

Do not replace working code just because a framework provides another abstraction.

---

# Phase 2 – LangChain Output Pipeline

Instead of calling Groq SDK directly:

```
FastAPI
    ↓
Groq SDK
```

We introduced LangChain.

```
FastAPI
      ↓
ChatPromptTemplate
      ↓
ChatGroq
      ↓
StrOutputParser
      ↓
String Response
```

---

# Components Used

## 1. ChatPromptTemplate

Purpose:

Creates structured prompts instead of manually building strings.

Before:

```python
prompt = "Explain Docker"
```

After:

```python
ChatPromptTemplate.from_messages(...)
```

Benefit:

- Cleaner prompts
- Easier to maintain
- Reusable

---

## 2. ChatGroq

Acts as LangChain's wrapper around Groq.

Instead of using Groq SDK directly, LangChain exposes a common LLM interface.

Example:

```python
llm.invoke(...)
```

---

## 3. StrOutputParser

LLMs return AIMessage objects.

Parser converts:

AIMessage

↓

Plain Python String

So our FastAPI endpoint simply receives:

```python
str
```

instead of handling message objects.

---

# LCEL Chain

Everything is connected using LangChain Expression Language.

```
Prompt
    |
    V
LLM
    |
    V
Parser
```

Code:

```python
chain = prompt | llm | parser
```

This pipeline is called an LCEL Chain.

---

# Phase 3 – Model Abstraction

Problem:

Every provider has different SDKs.

Groq:

```
chat.completions.create()
```

Gemini:

```
generate_content()
```

OpenAI:

Different SDK

Learning every SDK becomes difficult.

---

## Solution

Create one function:

```python
get_llm(provider)
```

Example:

```python
llm = get_llm("groq")
```

or

```python
llm = get_llm("openrouter")
```

Everything else remains unchanged.

This demonstrates LangChain's provider abstraction.

---

# Why get_llm()?

Instead of writing:

```
if provider == ...
```

throughout the project,

all provider selection happens in one place.

Benefits:

- Cleaner code
- Easy future expansion
- Single Responsibility Principle

---

# Phase 4 – Integrating into FastAPI

Earlier:

```
app.py
      ↓
chat_with_groq()
```

Now:

```
app.py
      ↓
get_ai_response()
      ↓
LangChain
```

FastAPI no longer talks directly to Groq.

It talks to LangChain.

LangChain decides which model to use.

---

# Important Design Decision

Streaming still uses the old Groq provider.

Reason:

LangChain streaming integration was outside the scope of this project.

No need to rewrite already working code.

---

# Challenges Faced

## 1. Invalid API Key

Reason:

Wrong Groq API key.

Fix:

Updated `.env`

---

## 2. Gemini Model Errors

Encountered:

- 404 Model Not Found
- 429 Quota Exceeded

Observation:

Problem was Google's API quota/model availability.

Not LangChain.

Decision:

Continue using Groq.

Keep OpenRouter as future expansion.

---

## 3. GitHub Actions Failure

Error:

```
ModuleNotFoundError:
langchain_core
```

Reason:

LangChain packages missing from `requirements.txt`.

Later discovered another issue:

`requirements.txt` was saved in UTF-16.

GitHub Actions couldn't read it correctly.

Fix:

- Save file as UTF-8
- Update requirements
- Push again

CI passed successfully.

---

# Final Architecture

```
Client
    │
    ▼
FastAPI
    │
    ▼
LangChain Service
    │
 ┌──┴─────────────┐
 │ PromptTemplate │
 │ ChatGroq       │
 │ OutputParser   │
 └──┬─────────────┘
    ▼
LLM Response
```

---

# Key Learnings

✔ LCEL

✔ Prompt Templates

✔ Output Parsers

✔ Chat Models

✔ Provider Abstraction

✔ Engineering Trade-offs

✔ GitHub Actions Debugging

✔ Clean Architecture

---

# Biggest Takeaway

Frameworks are tools, not goals.

Using LangChain everywhere does not automatically make a project better.

Good engineering is choosing the simplest solution that solves the problem while keeping the architecture clean.