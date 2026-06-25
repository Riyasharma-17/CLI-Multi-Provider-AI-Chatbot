# Prompt Evaluation Log

This document records prompt experiments performed during the development of the CLI Multi-Provider AI Chatbot. The goal is to make prompt changes intentional, measurable, and reproducible rather than relying on trial and error.

---

# Experiment 1 — Baseline System Prompt

### Goal

Evaluate the chatbot's default behavior without any role or formatting instructions.

### System Prompt

```
You are a helpful assistant.
```

### User Question

```
Explain recursion.
```

### Result

The model produced a generic textbook-style explanation.

### Observation

* Correct answer
* Neutral tone
* No examples
* No specific teaching style

### Decision

The default prompt is suitable for general-purpose conversations but lacks personality or domain-specific guidance.

---

# Experiment 2 — Role Prompt

### Goal

Observe how changing only the system prompt affects the assistant's behavior.

### System Prompt

```
You are a pirate. End every answer with Arrr!
```

### User Question

```
Explain recursion.
```

### Result

The assistant answered correctly while consistently adopting the pirate persona.

### Observation

* Knowledge remained unchanged.
* Only the response style and personality changed.

### Decision

System prompts effectively control the assistant's behavior without changing its underlying knowledge.

---

# Experiment 3 — JSON Output Prompt

### Goal

Generate structured responses instead of free-form text.

### Prompt Addition

```
Return ONLY valid JSON.

{
    "topic": "...",
    "summary": "..."
}
```

### User Question

```
Explain Python.
```

### Result

The model returned structured JSON suitable for machine processing.

### Observation

Occasionally, malformed JSON was generated.

### Decision

Added defensive parsing using `json.loads()` wrapped inside a `try-except` block to safely handle invalid outputs.

---

# Experiment 4 — Temperature Comparison

### Goal

Evaluate how temperature affects response generation.

### Question

```
What is Python in one line?
```

### Temperature 0.1

Produced a concise, deterministic response.

### Temperature 0.9

Produced a slightly more descriptive response.

### Observation

The difference was relatively small because the question had a single factual answer. Temperature has a much greater impact on open-ended or creative tasks.

### Decision

Use lower temperatures for factual assistants and higher temperatures for creative applications.
