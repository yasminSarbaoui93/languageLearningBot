from src.repository.vocabulary import get_or_create_user
from src.repository.vocabulary import save_user_base_and_learning_languages
from services.llm_service import extracat_language_code_with_llm
from bot.helpers import send_bot_response


def welcome_handling(user_message, bot):
    """
    Function to send a welcome message to user and start the conversation to ask the user for the language they want to learn and the language they want to use as a base for the dictionary and the communication with the bot

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    """
    chat_history = []
    user = get_or_create_user(str(user_message.from_user.id), user_message.from_user.username, user_message.from_user.first_name, user_message.from_user.last_name)
    user_id = user.id
    base_language_code = user.base_language
    chat_history.append({"role": "system", "content": "We ask information about what language the user in interested in, and given the user input, you will have to extract in lower case the language code of the language selected by the user (NOT THE LANGUAGE CODE THAT THE USER IS TYPING IN!!). For example, if the user says 'English', you have to respond 'en', if the user says 'inglese', you have to respond 'en', if the user says 'spagnolo', you have to respond 'es'."})
    bot_message = "welcome to this language learning bot! I will guide you through the first steps to start learning with me.\n1. What language do you want to learn?"
    chat_history = send_bot_response(bot, user_message, chat_history, base_language_code, bot_message)
    bot.register_next_step_handler(user_message, lambda msg: _extract_learning_language_code(msg, bot, chat_history, user))


def _extract_learning_language_code(user_message, bot, chat_history, user):
    """
    Function to extract the language code of the language the user wants to learn

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    chat_history: the array with chat history, containing system message, assistant messages and user messages
    user_id: the id of the user in the database
    """
    user_id = user.id
    base_language_code = user.base_language
    chat_history.append({"role": "user", "content": user_message.text})
    learning_language_code = extracat_language_code_with_llm(user_message.text)
    if learning_language_code is None:
        bot_message = "I'm sorry, I didn't understand the language you want to learn. Let's start over\n1. What language do you want to learn?"
        chat_history = send_bot_response(bot, user_message, chat_history, base_language_code, bot_message)
        bot.register_next_step_handler(user_message, lambda msg: _extract_learning_language_code(msg, bot, chat_history, user_id))
    else:
        bot_message = "2.What language you want to use as a base for your dictionary and our communications?"
        chat_history = send_bot_response(bot, user_message, chat_history, base_language_code, bot_message)
        bot.register_next_step_handler(user_message, lambda msg: _extract_base_language_code_and_save(msg, bot, chat_history, learning_language_code, user))


def _extract_base_language_code_and_save(user_message, bot, chat_history, learning_language_code, user):
    """
    Function to extract the language code of the language the user wants to use as a base for the dictionary and the communication with the bot and save the learning and base language codes of the user in the database

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    chat_history: the array with chat history, containing system message, assistant messages and user messages
    learning_language_code: the language code of the language the user wants to learn
    user_id: the id of the user in the database
    """
    user_id = user.id
    chat_history.append({"role": "user", "content": user_message.text})
    base_language_code = user.base_language
    base_language_code_from_user_message = extracat_language_code_with_llm(user_message.text)
   
    if base_language_code_from_user_message is None:
        bot_message = "I'm sorry, I didn't understand the language you want to use as a base. Let's start over\n2. What language you want to use as a base for your dictionary and our communications?"
        chat_history = send_bot_response(bot, user_message, chat_history, base_language_code, bot_message)
        bot.register_next_step_handler(user_message, lambda msg: _extract_base_language_code_and_save(msg, bot, chat_history, learning_language_code, user))
    
    else:
        base_language_code = base_language_code_from_user_message
        bot_message = f"Great! You just created your dictionary <b>{base_language_code}-{learning_language_code}</b> and <b>{learning_language_code}-{base_language_code}</b>"
        chat_history = send_bot_response(bot, user_message, chat_history, base_language_code, bot_message)
        save_user_base_and_learning_languages(user_id, base_language_code, learning_language_code)

        bot_message = "Now you can start adding words to your dictionary by typing /add, or see the list of available commands through /help"
        chat_history = send_bot_response(bot, user_message, chat_history, base_language_code, bot_message)