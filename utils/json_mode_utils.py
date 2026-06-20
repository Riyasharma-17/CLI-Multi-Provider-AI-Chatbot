def check_json_mode(user_input):
    json_mode = False

    if user_input.startswith("/json"):
        json_mode = True
        user_input = user_input.replace("/json", "", 1).strip()

    return json_mode, user_input