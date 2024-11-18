responses = {
    "hello": "Hi! How can I help you today?",
    "how are you": "I'm doing great, thank you! How about you?",
    "bye": "Goodbye! Have a great day!",
    "thanks": "You're welcome! Let me know if you need anything else.",
}


def get_bot_response(user_message):
    user_message = user_message.lower()
    for key in responses:
        if key in user_message:
            return responses[key]
        
    return "Sorry, I didn't understand that. Could you please rephrase?"