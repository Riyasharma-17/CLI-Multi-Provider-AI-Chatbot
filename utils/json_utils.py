import json


def display_response(bot_reply, json_mode):

    if not json_mode:
        print("Bot:", bot_reply)
        return

    try:
        data = json.loads(bot_reply) #-> json string to py dictionary.

        pretty_json = json.dumps( #.dumps()->Python dict to json text
            data,
            indent=4 #Add spaces and line breaks
        )

        print(pretty_json)
#  print("Topic:", data.get("topic", "Not found"))  #Try to give me summary. If missing, return None.
            #  print("Summary:", data.get("summary", "Not found"))

    except json.JSONDecodeError:
        print("\nInvalid JSON received!")