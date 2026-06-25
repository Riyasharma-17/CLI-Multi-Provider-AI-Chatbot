## Day 5 Progress

### Completed

* Reviewed the project from an engineering perspective after receiving external feedback
* Identified that "defensive programming" claims were not backed by tests
* Introduced `pytest` and created a dedicated `tests/` folder
* Learned how to capture terminal output using `capsys`
* Wrote tests for normal text responses, valid JSON, and malformed JSON handling
* Added exception handling to provider adapters to prevent API failures from crashing the chatbot
* Learned mocking with `unittest.mock`
* Simulated successful and failed API calls without making real network requests
* Added automated tests for Groq, Gemini, and OpenRouter providers
* Achieved **9 passing tests** covering both success and failure scenarios
* Replaced manual verification with reproducible automated testing
* Pinned dependency versions in `requirements.txt` for reproducibility
* Learned the difference between direct dependencies and transitive dependencies
* Added a terminal demo GIF to the README
* Improved project documentation to reflect testing, reliability, and version pinning
* Updated limitations and future improvements based on the project's current state
* Prepared the repository for public sharing and LinkedIn showcase

### Key Concepts Learned

* Unit Testing
* Pytest
* Output Capturing (`capsys`)
* Mocking (`unittest.mock`)
* Dependency Injection Through Patching
* Success Path vs Failure Path Testing
* Defensive Programming Verification
* Reproducibility
* Version Pinning
* Direct vs Transitive Dependencies
* Reliability Engineering
* Documentation as Part of Engineering
* Demo-Driven Project Presentation

### Current Status

✅ Multi-provider chatbot architecture complete.

✅ Automated tests added.

✅ 9 tests passing.

✅ Provider failures handled gracefully.

✅ Dependencies version-pinned.

✅ Demo GIF embedded in README.

✅ Project documentation and reliability significantly improved.

### What Changed Mentally

Initially, the project focused on features:

> "Can it work?"

After mentor feedback, the focus shifted to:

> "Can I prove that it works?"

This changed the project from a feature-driven chatbot into a more reliable and reproducible software engineering project.


