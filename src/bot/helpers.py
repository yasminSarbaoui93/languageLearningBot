from services.llm_service import translate_to_language



def send_bot_response(bot, user_message, chat_history: list, language_code: str, bot_message: str, word_to_append_to_translation = None) -> list:
    """
    Function to respond to the user with a message in the language the user is a selected language, with possibiliy to append a word to the translation of the message that is not to be translated

    args:
    bot: the bot object to send the message
    user_message: the message object from the user, needed to know the chat where to send the message
    chat_history: the conversation history array
    language_code: the language code of the language to translate the message to
    bot_message: the message to send to the user
    (Optional) word_to_append_to_translation: the word to append to the translation of the message, if any

    returns:
    chat_history: the updated conversation history
    """
    bot_message = translate_to_language(language_code, bot_message)
    if word_to_append_to_translation is None:
        word_to_append_to_translation = ""
    bot_message = f"{bot_message} {word_to_append_to_translation}"
    chat_history.append({"role": "assistant", "content": bot_message})  
    bot.send_message(user_message.chat.id, bot_message, parse_mode='HTML')
    return chat_history