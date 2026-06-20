def create_system_message():

    print("\nEnter system prompt.")
    print("(Press Enter for default assistant.)")

    system_prompt = input("> ")

    if not system_prompt:
        system_prompt = "You are a helpful assistant."

    return {
        "role": "system",
        "content": system_prompt
    }