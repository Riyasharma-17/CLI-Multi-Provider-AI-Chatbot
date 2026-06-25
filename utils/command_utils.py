def handle_command(user_input, system_message,few_shot_examples):

    if user_input == "/quit":
        print("GoodBye!")
        return True,None
    
    if user_input == "/clear":

        print("Conversation history cleared!")

        messages = [system_message]

        messages.extend(
            few_shot_examples
        )

    return False, messages #Continue normally.