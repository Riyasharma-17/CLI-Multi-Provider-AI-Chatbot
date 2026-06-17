# CLI QA Bot

A command-line chatbot using free AI APIs.

## Day 1 Progress

### Completed

* Set up professional Python project structure
* Created and activated a virtual environment (`venv`)
* Installed required dependencies:

  * `groq`
  * `google-generativeai`
  * `python-dotenv`
* Configured secure API key management using `.env`
* Connected Python application to Groq API
* Made the first successful API call using **Llama 3.1 8B Instant**
* Retrieved and displayed AI-generated responses
* Displayed token usage information
* Configured GitHub security practices (`.gitignore`, secret management)

### Key Concepts Learned

* Virtual Environments
* Environment Variables (`.env`)
* API Authentication
* SDKs and API Clients
* LLM Request → Response Flow
* Basic AI Engineering Debugging

### Current Status

✅ Python can successfully communicate with Groq's Llama 3.1 model and receive responses.

### Next Steps

* Build interactive CLI chat loop
* Accept user input dynamically
* Maintain conversation history
* Add chatbot memory and context handling

## Day 2 Progress

### Completed

* Built an interactive CLI chat loop using `while True`
* Added graceful exit with `/quit`
* Replaced hardcoded prompts with dynamic user input
* Implemented conversation history using a `messages` list
* Stored both user and assistant messages
* Enabled context-aware conversations (chat memory)
* Added system prompts to control assistant behavior
* Tested different assistant personalities
* Implemented `/clear` to reset conversation history
* Preserved system instructions while clearing memory
* Verified multi-turn memory and context retention

### Key Concepts Learned

* Infinite Loops (`while True`)
* `break` and `continue`
* Lists and Dictionaries
* Message Roles (`system`, `user`, `assistant`)
* Conversation History
* Simulated Memory in LLMs
* System Prompts and AI Behavior
* Context Windows and Token Growth
* Stateful vs Stateless Interactions

### Current Status

✅ Chatbot supports continuous conversations with memory, system instructions, and history reset.

### Next Steps

* Add provider selection (Groq / Gemini)
* Implement Gemini integration
* Accept custom system prompts from users
* Add structured JSON mode
* Refactor code into cleaner components
* Compare Groq and Gemini API designs
