
# Day 10 Progress

## Completed

* Implemented `GET /history` endpoint to expose the chatbot's conversation history through the API
* Reused the existing in-memory `messages` list from the CLI chatbot instead of creating a new storage mechanism
* Learned how server-side state allows conversations to persist across multiple HTTP requests
* Implemented `DELETE /history` endpoint to reset the chatbot conversation
* Used `messages.clear()` to remove all previous messages while preserving the initial system prompt
* Understood why the system prompt must always remain as the first message after clearing history
* Verified the complete conversation lifecycle by testing:

  * Sending multiple chat messages
  * Retrieving conversation history
  * Clearing history
  * Confirming the chatbot no longer remembered previous conversations
* Added **CORS Middleware** to prepare the backend for future frontend integration
* Learned how browsers enforce Cross-Origin Resource Sharing (CORS) and why APIs must explicitly allow trusted origins
* Configured development-friendly CORS settings using wildcard origins, methods, and headers
* Understood how middleware processes every incoming request before it reaches the API endpoints

---

# Key Concepts Learned

* GET Requests
* DELETE Requests
* RESTful API Design
* Server-side State
* In-memory Conversation Storage
* Conversation Lifecycle
* `messages.clear()`
* Global Variables vs Local Variables
* Cross-Origin Resource Sharing (CORS)
* Middleware
* Browser Security Policies
* API Accessibility
* Request Flow Through Middleware

---

# Current Status

✅ FastAPI backend now supports complete conversation management.

Implemented API endpoints:

* `POST /chat` → Send user messages to the chatbot
* `GET /history` → Retrieve the complete conversation history
* `DELETE /history` → Reset the conversation while preserving system instructions

✅ Backend is now prepared for future React, Next.js, or other frontend applications through CORS configuration.

---

# What Changed Mentally

While building the CLI chatbot, conversation memory only existed inside a running Python program.

Now I understand that a backend server can also maintain state by keeping shared data in memory.

Instead of interacting through terminal commands like:

```text
/clear
```

the same functionality is now exposed through proper REST API endpoints:

```text
DELETE /history
```

This helped me understand that **different interfaces can reuse the exact same business logic**. The implementation of clearing history did not change—only the way clients interact with it changed.

Another important realization was how **HTTP methods represent intent**:

* `POST` creates or processes new data.
* `GET` retrieves existing data without modifying it.
* `DELETE` removes existing data.

This made REST APIs feel much more structured compared to simply writing Python functions.

I also learned why browsers sometimes block requests even when the backend is working correctly.

Before today, I assumed CORS was a FastAPI feature.

Now I understand that **CORS is actually enforced by the browser**, while the backend simply declares which origins are allowed to communicate with it.

Finally, I learned that **middleware acts like a checkpoint** for every request entering the application. Instead of placing repeated logic inside every endpoint, middleware allows common behavior—such as CORS handling—to be applied once and automatically affect all routes.

---

# Next Steps

* Implement proper API error handling using `HTTPException`
* Handle provider failures and invalid requests gracefully
* Return meaningful HTTP status codes instead of generic server errors
* Write pytest tests for FastAPI endpoints
* Refactor into a production-style FastAPI project structure
* Complete backend polishing and publish the finished API on GitHub
