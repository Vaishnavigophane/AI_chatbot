def detect_intent(user_input):
    user_input = user_input.lower()

    if "calculate" in user_input or "math" in user_input:
        return "calculator"
    elif "exit" in user_input or "quit" in user_input:
        return "exit"
    else:
        return "chat"
