## Day 8 Progress

### Completed

* Added a configurable **Temperature Slider** to let users control response creativity at runtime
* Validated temperature input (`0.0 - 1.0`) using defensive programming with input validation
* Passed temperature through a common provider interface instead of using global variables
* Learned why function parameters create cleaner, more reusable code than shared global state
* Compared low and high temperature responses to understand how randomness affects LLM generation
* Discovered that temperature has little impact on factual questions but noticeably changes creative or open-ended responses
* Created a **PROMPT_LOG.md** file to document prompt experiments, observations, and engineering decisions
* Learned evaluation discipline by recording why prompt changes were made instead of relying on trial and error
* Implemented **Few-shot Prompting** using an external `examples.txt` file
* Separated prompt examples from application logic to keep the codebase modular and easy to maintain
* Built a reusable few-shot loader that converts text examples into chatbot message format
* Learned how to parse structured text using `split()`, `replace()`, and `strip()`
* Inserted few-shot examples between the system prompt and the user's real question
* Updated `/clear` to reset only conversation history while preserving system prompts and few-shot examples
* Strengthened the chatbot architecture by separating configuration, prompt data, and conversation state

### Key Concepts Learned

* Temperature Sampling
* Deterministic vs Creative Responses
* Runtime Configuration
* Function Parameterization
* Prompt Evaluation (Eval Discipline)
* Prompt Engineering Experiments
* Few-shot Prompting
* In-Context Learning
* Parsing Text Files
* Configuration vs Conversation State
* Separation of Concerns
* Reusable Utility Modules

### Current Status

✅ Runtime temperature control added.

✅ Prompt evaluation log introduced.

✅ Few-shot prompting supported through external text files.

✅ Conversation reset preserves chatbot configuration.

✅ Prompt data separated from application logic.

### What Changed Mentally

Earlier, prompt engineering felt like writing better instructions.

Now it feels like an engineering process:

**Design Prompt → Test → Observe → Record → Improve**

Instead of randomly tweaking prompts, every meaningful change is evaluated, documented, and backed by observations. The chatbot now behaves more like a configurable AI system rather than a simple API wrapper.

### Next Steps

* Migrate Gemini integration to the new `google.genai` SDK
* Add tests for the few-shot loader
* Support configurable JSON schemas
* Persist conversations to local storage
* Explore streaming responses
