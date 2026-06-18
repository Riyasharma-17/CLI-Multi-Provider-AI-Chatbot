# Day 3 — Multi-Provider Architecture & Real-World API Challenges

## Goal

Transform the chatbot from a Groq-only application into a provider-agnostic chatbot capable of supporting multiple LLM providers.

---

# Why Multi-Provider Support?

Until now, the architecture looked like:

User

↓

Groq

↓

Response

This meant the entire application depended on one provider.

A better architecture is:

User

↓

Choose Provider

↙        ↘

Groq     Gemini

↘        ↙

Response

This makes the chatbot extensible and future-proof.

---

# Provider Selection Menu

Added:

```text
[1] Groq
[2] Gemini
```

User choice gets stored in:

```python
provider = "groq"
```

or

```python
provider = "gemini"
```

Using strings instead of numbers makes the code self-documenting and easier to extend later.

Future providers can easily be added:

* OpenAI
* Claude
* DeepSeek

without redesigning the chatbot.

---

# Understanding Provider Abstraction

Instead of creating separate chatbot logic for every provider:

```text
Groq Chatbot
Gemini Chatbot
OpenAI Chatbot
```

the same chatbot now works with different backends.

Common flow:

User Input

↓

Provider

↓

LLM

↓

bot_reply

↓

Print Reply

↓

Store History

The rest of the application doesn't care which provider generated the response.

This is called **abstraction**.

---

# The Importance of Common Variables

Introduced:

```python
bot_reply
```

instead of:

```python
groq_reply
gemini_reply
```

This unified variable allows:

* Printing replies
* Saving assistant messages
* Logging conversations

without duplicating code.

Both providers eventually produce:

```python
bot_reply
```

which simplifies the entire application.

---

# Understanding SDK Differences

Although Groq and Gemini solve the same problem, their APIs are structured differently.

## Groq

Groq follows OpenAI-compatible syntax:

```python
client.chat.completions.create()
```

Model name is specified during every request:

```python
model="llama-3.1-8b-instant"
```

This allows switching models dynamically.

---

## Gemini

Gemini creates a model object:

```python
genai.GenerativeModel()
```

The model name is attached to the object itself.

Later requests simply use:

```python
generate_content()
```

This demonstrates that different providers expose different interfaces even though they perform the same task.

---

# Why Objects Are Created Once

Created:

* `client` for Groq
* `gemini_model` for Gemini

only once at startup.

Reason:

These objects are reusable.

Recreating them inside every loop would waste resources and slow down the application.

---

# Why Groq Memory Worked But Gemini Forgot

Groq naturally accepts:

```python
messages = [...]
```

which contains:

* system messages
* user messages
* assistant replies

Therefore the model sees the entire conversation history.

Gemini initially received only:

```python
user_input
```

which means every question looked independent.

Memory failed because previous conversations were never sent.

---

# Simulating Memory for Gemini

To mimic conversation history, messages were converted into one giant string:

```text
system: ...
user: ...
assistant: ...
user: ...
```

and then passed to Gemini.

Conceptually:

messages list

↓

Convert to text

↓

Single Prompt

↓

Gemini

↓

Response

This highlighted one of the biggest differences between provider APIs.

---

# Real-World API Problems

For the first time, external issues appeared.

Several errors occurred:

### Model Not Found

```
404 model not found
```

This showed that model names and SDK versions matter.

---

### Deprecated SDK Warning

Google warned that:

```python
google.generativeai
```

is deprecated.

A migration to:

```python
google.genai
```

will eventually be needed.

This demonstrated how APIs evolve over time.

---

### Quota Exhausted

Encountered:

```
429 ResourceExhausted
```

meaning:

* API key worked.
* Authentication succeeded.
* Server was reachable.
* Free quota was unavailable.

This wasn't a coding bug.

It was an infrastructure limitation.

---

# Important Engineering Lesson

Not every error means your code is wrong.

Real AI engineering involves:

* Authentication issues
* Quotas
* Rate limits
* SDK deprecations
* Model version changes
* Provider-specific behavior

Debugging external systems is part of the job.

---

# Architecture Achieved

Current architecture:

```text
User

↓

Provider Selection

↓

Groq / Gemini

↓

LLM Response

↓

bot_reply

↓

Print Response

↓

Store Assistant Message

↓

Continue Conversation
```

The chatbot has evolved from being provider-specific into a flexible architecture capable of supporting multiple AI services.

---

# Key Concepts Learned

### Provider Abstraction

Different backends, same chatbot.

### Reusable Objects

Create expensive objects once.

### Common Interface

Both providers produce `bot_reply`.

### API Design Differences

Groq and Gemini expose different syntaxes.

### Memory Simulation

Conversation history must be supplied manually.

### SDK Evolution

Libraries change over time.

### Infrastructure Errors

Not every failure is caused by code.

---

# End of Day 4

Current chatbot capabilities:

✅ Conversation memory

✅ System prompts

✅ /quit

✅ /clear

✅ Provider selection

✅ Provider abstraction

✅ Common response interface

⚠️ Gemini blocked by quota limitations

The project now resembles a real AI application rather than a single API script.

Next step:

Structured Outputs and JSON Mode.
