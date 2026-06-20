def handle_command(user_input, system_message):

    if user_input == "/quit":
        print("GoodBye!")
        return True,None
    
    if user_input == "/clear":
        print("Conversation history cleared!")
        return False, [system_message] #here false cuz u dont want loop to quit
    
    return False, None #Continue normally.