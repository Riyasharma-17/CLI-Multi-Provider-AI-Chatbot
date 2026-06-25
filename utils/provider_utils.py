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
    
def choose_temperature():
    while True:

        try:
            temperature = float(
                input("Enter temperature (Recommended: 0.2 for factual, 0.8 for creative):")
            )

            if 0.0 <= temperature <= 1.0:
                return temperature
            
            print("Temperature must be between 0.0 and 1.0.")

        except ValueError:
            print("Please enter a valid number.")
