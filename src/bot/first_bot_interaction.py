from src.repository.vocabulary import get_or_create_user_id
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
from src.repository.vocabulary import save_user_base_and_learning_languages

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def welcome_handling(message, bot):
    """
    Function to send a welcome message to user and start the conversation to ask the user for the language they want to learn and the language they want to use as a base for the dictionary and the communication with the bot

    args:
    message: the message object from the user
    bot: the bot object to send messages to the user
    """
    chat_history = []
    user_id = get_or_create_user_id(str(message.from_user.id), message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    chat_history.append({"role": "system", "content": "We ask information about what language the user in interested in, and given the user input, you will have to extract in lower case the language code of the language selected by the user (NOT THE LANGUAGE CODE THAT THE USER IS TYPING IN!!). For example, if the user says 'English', you have to respond 'en', if the user says 'inglese', you have to respond 'en', if the user says 'spagnolo', you have to respond 'es'."})
    chat_history.append({"role": "assistant", "content": "Welcome to this language learning bot! I will guide you through the first steps to start learning with me."})
    bot.send_message(message.chat.id, chat_history[1]["content"])
    assistant_message = "1. What language do you want to learn?"
    chat_history.append({"role": "assistant", "content": assistant_message})
    bot.send_message(message.chat.id, assistant_message)
    bot.register_next_step_handler(message, lambda msg: _extract_learning_language_code(msg, bot, chat_history, user_id))


def _extract_learning_language_code(user_message, bot, chat_history, user_id):
    """
    Function to extract the language code of the language the user wants to learn

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    chat_history: the array with chat history, containing system message, assistant messages and user messages
    user_id: the id of the user in the database
    """
    chat_history.append({"role": "user", "content": user_message.text})
    learning_language_code = extracat_language_code_with_llm(user_message.text)
    if learning_language_code is None:
        assistant_message = "I'm sorry, I didn't understand the language you want to learn. Let's start over"
        chat_history.append({"role": "assistant", "content": assistant_message})
        bot.send_message(user_message.chat.id, assistant_message)
        assistant_message = "1. What language do you want to learn?"
        chat_history.append({"role": "assistant", "content": assistant_message})
        bot.send_message(user_message.chat.id, assistant_message)
        bot.register_next_step_handler(user_message, lambda msg: _extract_learning_language_code(msg, bot, chat_history, user_id))
    else:
        chat_history.append({"role": "assistant", "content": learning_language_code})
        assistant_message = f"2. What language you want to use as a base for your dictionary and our communications?"
        chat_history.append({"role": "assistant", "content": assistant_message})
        bot.send_message(user_message.chat.id, assistant_message)
        bot.register_next_step_handler(user_message, lambda msg: _extract_base_language_code_and_save(msg, bot, chat_history, learning_language_code, user_id))


def _extract_base_language_code_and_save(user_message, bot, chat_history, learning_language_code, user_id):
    """
    Function to extract the language code of the language the user wants to use as a base for the dictionary and the communication with the bot and save the learning and base language codes of the user in the database

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    chat_history: the array with chat history, containing system message, assistant messages and user messages
    learning_language_code: the language code of the language the user wants to learn
    user_id: the id of the user in the database
    """
    chat_history.append({"role": "user", "content": user_message.text})
    base_language_code = extracat_language_code_with_llm(user_message.text)
    if base_language_code is None:
        assistant_message = "I'm sorry, I didn't understand the language you want to use as a base. Let's start over"
        chat_history.append({"role": "assistant", "content": assistant_message})
        bot.send_message(user_message.chat.id, assistant_message)
        assistant_message = "2. What language you want to use as a base for your dictionary and our communications?"
        chat_history.append({"role": "assistant", "content": assistant_message})
        bot.send_message(user_message.chat.id, assistant_message)
        bot.register_next_step_handler(user_message, lambda msg: _extract_base_language_code_and_save(msg, bot, chat_history, learning_language_code, user_id))
    
    else:
        chat_history.append({"role": "assistant", "content": base_language_code})
        assistant_message = f"Great! You just created your dictionary <b>{base_language_code}-{learning_language_code}</b> and <b>{learning_language_code}-{base_language_code}</b>"
        chat_history.append({"role": "assistant", "content": assistant_message})
        bot.send_message(user_message.chat.id, assistant_message, parse_mode='HTML')
        save_user_base_and_learning_languages(user_id, base_language_code, learning_language_code)
        assistant_message = "Now you can start adding words to your dictionary by typing /add, or see the list of available commands through /help"
        chat_history.append({"role": "assistant", "content": assistant_message})
        bot.send_message(user_message.chat.id, assistant_message, parse_mode='HTML')


def extracat_language_code_with_llm(user_input: str) -> str | None:
    """
    Function to extract the language code from the user message. the user message should be the name of the language they want to learn, e.g. spanish, arabo, italiano, frances, etc. 
    given the user input the llm should respond either with a language code in format ISO 639-1 or ISO 639-2, e.g. 'es' for spanish, 'ar' for arabic, 'it' for italian, 'fr' for french, etc., or respond  with error message, informing the user tbat tbere was a mistake
    then create an if else. if the result from the llm is a language code, then you can go on with the conversation and ask the user for the base language. if the result is an error message, then you should ask the user to repeat the language they want to learn
        
    args:
    user_message: the message object from the user

    returns:
    language_code: the language code of the language from user_input

    """
    system_message = "We ask information about what language the user in interested in, and given the user input, you will have to extract in lower case the language code of the language selected by the user (NOT THE LANGUAGE CODE THAT THE USER IS TYPING IN!!). For example, if the user says 'English', you have to respond 'en', if the user says 'inglese', you have to respond 'en', if the user says 'spagnolo', you have to respond 'es'. In case the user message is not containing infromation around a language (for example they wrote a random word or sentence unrelated), respond with 'None'"
    messages = []
    messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    learning_language_code = response.choices[0].message.content
    if learning_language_code == "None":
        return None
    return learning_language_code