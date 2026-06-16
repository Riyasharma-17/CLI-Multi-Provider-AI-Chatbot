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
