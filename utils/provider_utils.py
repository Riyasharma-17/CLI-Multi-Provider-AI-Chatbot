def choose_provider():

    print("Choose Provider:")
    print("[1] Groq")
    print("[2] Gemini")
    print("[3] OpenRouter")
    
    choice = input("Enter choice: ")

    if choice == "1":
        return "groq"

    elif choice == "2":
        return "gemini"
    
    elif choice == "3":
        return "openrouter"
    
    else:
        print("Invalid choice.")
        raise SystemExit