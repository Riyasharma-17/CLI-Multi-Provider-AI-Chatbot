def load_examples():
    messages = []

    with open("examples.txt", "r") as file:
        text = file.read()

    examples = text.split("---")

    for example in examples:

        if not example.strip():
            continue

        question, answer = example.split("A:")

        question = (
            question
            .replace("Q:", "")
            .strip()
        )

        answer = answer.strip()

        messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    return messages


# Read file
# ↓
# Convert into messages
# ↓
# Return
