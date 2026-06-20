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

## Day 3 Progress

### Completed

* Added provider selection menu (`Groq` / `Gemini`)
* Implemented provider abstraction using a common `bot_reply` variable
* Initialized Gemini API and compared its SDK structure with Groq
* Learned differences between OpenAI-compatible syntax and Gemini syntax
* Reused API client objects instead of recreating them inside the loop
* Understood why conversation memory works differently across providers
* Simulated conversation history for Gemini by converting messages into a single prompt
* Built a provider-independent response flow
* Encountered and debugged real-world API issues
* Investigated model naming, SDK deprecation, and quota limitations
* Designed the chatbot architecture to support future providers

### Key Concepts Learned

* Provider Abstraction
* Common Interface Design
* Reusable API Clients
* OpenAI-Compatible Syntax
* Differences Between SDK Designs
* Memory Simulation in LLMs
* Prompt Construction
* API Versioning
* SDK Deprecation
* Rate Limits and Quota Errors
* Infrastructure vs Code Bugs

### Current Status

✅ Chatbot architecture now supports multiple providers through a unified interface.

⚠️ Gemini integration is temporarily blocked by external quota limitations, but the design is ready and extensible.

### Next Steps

* Implement JSON mode (`/json`)
* Generate structured outputs
* Improve error handling
* Refactor code into cleaner components
* Add token usage support for Gemini
* Polish and prepare the project for GitHub showcase

## Day 4 Progress

### Completed

* Added a special `/json` command to enable structured output mode
* Implemented prompt engineering to instruct the model to return JSON responses
* Designed a fixed JSON schema with `topic` and `summary` fields
* Learned why LLMs can generate invalid or inconsistent JSON
* Converted JSON strings into Python dictionaries using `json.loads()`
* Converted Python dictionaries back into formatted JSON using `json.dumps()`
* Added exception handling for invalid JSON responses
* Safely accessed dictionary values using `.get()`
* Handled missing keys without crashing the program
* Implemented pretty printing for human-readable JSON output
* Preserved original text responses inside conversation history
* Built the foundation for machine-readable AI outputs

### Key Concepts Learned

* Structured Outputs
* Prompt Engineering
* JSON Schema Design
* JSON Parsing (`json.loads`)
* JSON Serialization (`json.dumps`)
* Exception Handling (`try-except`)
* `JSONDecodeError`
* Dictionary Access (`[]` vs `.get()`)
* Missing Keys vs Extra Keys
* Defensive Programming
* Human-Readable vs Machine-Readable Data

### Current Status

✅ Chatbot can now generate structured JSON responses and safely process them into Python dictionaries.

### Next Steps

* Refactor code into cleaner modules
* Accept custom system prompts from users
* Improve error handling and architecture
* Add token usage support for Gemini
* Migrate to newer Gemini SDK
* Polish and prepare the project for GitHub showcase

## Day 5 Progress

### Completed

* Refactored the project into a modular architecture instead of keeping everything inside one giant `main.py`
* Created a dedicated `providers/` folder for API-specific code
* Moved Groq API logic into `groq_provider.py`
* Encapsulated API calls inside reusable functions like `chat_with_groq()`
* Removed direct dependency on the Groq client from `main.py`
* Created a `utils/` folder for reusable helper functions
* Moved JSON parsing and response formatting into `json_utils.py`
* Moved system prompt creation into `system_utils.py`
* Added support for custom system prompts entered by users at startup
* Moved command handling (`/quit`, `/clear`) into `command_utils.py`
* Moved JSON mode detection into `json_mode_utils.py`
* Moved provider selection into `provider_utils.py`
* Reduced complexity inside `main.py` and transformed it into a clean application controller
* Learned how to separate responsibilities between files
* Fixed debugging issues caused by missing `return` statements
* Improved architecture without changing chatbot behavior

### Key Concepts Learned

* Refactoring
* Separation of Concerns
* Modular Architecture
* Utility Modules
* Provider Abstraction
* Function Encapsulation
* Single Responsibility Principle
* Clean Code Practices
* Return Values vs Local Variables
* Debugging Logical Errors
* Reusability
* Maintainability

### Current Status

✅ The chatbot architecture has been successfully refactored into a modular and maintainable structure.

### Next Steps

* Add robust exception handling
* Integrate Gemini as a dedicated provider
* Support multiple LLM providers through a common interface
* Improve reliability when external APIs fail
* Continue polishing the project architecture

---

## Day 6 Progress

### Completed

* Created `gemini_provider.py` and separated Gemini-specific code from the main application
* Learned how Gemini differs from OpenAI-compatible APIs
* Simulated conversation memory for Gemini by converting messages into a transcript
* Added exception handling to prevent provider failures from crashing the chatbot
* Investigated model naming errors and API deprecation warnings
* Encountered real-world quota limitations with Gemini and learned to distinguish infrastructure problems from coding mistakes
* Created `openrouter_provider.py`
* Added OpenRouter support as a third provider
* Implemented a common provider interface across Groq, Gemini and OpenRouter
* Learned that different providers can expose different APIs while presenting the same interface to the application
* Debugged OpenRouter model availability errors
* Switched to a working free model configuration
* Successfully achieved true multi-provider support
* Verified that conversation memory and JSON mode work independently of the selected provider
* Completed the core architecture of the chatbot

### Key Concepts Learned

* Multi-Provider Architecture
* Interface Abstraction
* API Agnostic Design
* Exception Handling
* Defensive Programming
* External Service Failures
* Quota Limits and Rate Limiting
* Infrastructure vs Code Bugs
* Error Propagation
* Provider Independence
* Prompt Serialization
* Robust System Design

### Current Status

✅ The chatbot now supports multiple providers through a common interface.

✅ Core project architecture is complete.

Supported providers:

* Groq
* Gemini
* OpenRouter

Supported features:

* Memory
* System Prompts
* JSON Mode
* `/quit`
* `/clear`
* Token Usage Tracking
* Exception Handling
* Modular Architecture


