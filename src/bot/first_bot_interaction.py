from src.repository.vocabulary import get_or_create_user_id
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
from src.repository.vocabulary import add_base_and_learning_language_to_user

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def welcome_handling(message, bot):
    chat_history = []
    user_id = get_or_create_user_id(str(message.from_user.id), message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    chat_history.append({"role": "system", "content": "We ask information about what language the user in interested in, and given the user input, you will have to extract in lower case the language code of the language selected by the user (NOT THE LANGUAGE CODE THAT THE USER IS TYPING IN!!). For example, if the user says 'English', you have to respond 'en', if the user says 'inglese', you have to respond 'en', if the user says 'spagnolo', you have to respond 'es'."})
    chat_history.append({"role": "assistant", "content": "Welcome to this language learning bot! I will guide you through the first steps to start learning with me."})
    chat_history.append({"role": "assistant", "content": "1. What language do you want to learn?"})
    bot.send_message(message.chat.id, chat_history[1]["content"])
    bot.send_message(message.chat.id, chat_history[2]["content"])
    bot.register_next_step_handler(message, lambda msg: _transform_into_language_code(msg, bot, chat_history, user_id))


def _transform_into_language_code(user_message, bot, chat_history, user_id):
    #implement this function to transform the language into a language code (e.g. "english" -> "en")
    chat_history.append({"role": "user", "content": user_message.text})
    response = client.chat.completions.create(model="gpt-4o", messages=chat_history)
    chat_history.append({"role": "assistant", "content": response.choices[0].message.content})
    learning_language_code = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": f"2. What language you want to use as a base for your dictionary and our communications?"})
    bot.send_message(user_message.chat.id, chat_history[5]["content"])
    bot.register_next_step_handler(user_message, lambda msg: _transform_into_language_code_base(msg, bot, chat_history, learning_language_code, user_id))


def _transform_into_language_code_base(user_message, bot, chat_history, learning_language_code, user_id):
    chat_history.append({"role": "user", "content": user_message.text})
    response = client.chat.completions.create(model="gpt-4o", messages=chat_history)
    chat_history.append({"role": "assistant", "content": response.choices[0].message.content})
    base_language_code = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": f"Great! You just created your dictionary <b>{base_language_code}-{learning_language_code}</b> and <b>{learning_language_code}-{base_language_code}</b>"})
    bot.send_message(user_message.chat.id, chat_history[8]["content"], parse_mode='HTML')
    add_base_and_learning_language_to_user(user_id, base_language_code, learning_language_code)
    chat_history.append({"role": "assistant", "content": "Now you can start adding words to your dictionary by typing /add, or see the list of available commands through /help"})


def extracat_learning_language_code_with_llm(user_message):
    """
    Function to extract the learning language code from the user message. the user message should be the name of the language they want to learn, e.g. spanish, arabo, italiano, frances, etc. 
    given the user input the llm should respond either with a language code in format ISO 639-1 or ISO 639-2, e.g. 'es' for spanish, 'ar' for arabic, 'it' for italian, 'fr' for french, etc., or respond  with error message, informing the user tbat tbere was a mistake
    then create an if else. if the result from the llm is a language code, then you can go on with the conversation and ask the user for the base language. if the result is an error message, then you should ask the user to repeat the language they want to learn
        
    args:
    user_message: the message object from the user

    returns:
    learning_language_code: the language code of the language the user wants to learn

    """
    system_message = "We ask information about what language the user in interested in, and given the user input, you will have to extract in lower case the language code of the language selected by the user (NOT THE LANGUAGE CODE THAT THE USER IS TYPING IN!!). For example, if the user says 'English', you have to respond 'en', if the user says 'inglese', you have to respond 'en', if the user says 'spagnolo', you have to respond 'es'. In case the user message is not containing infromation around a language (for example they wrote a random word or sentence unrelated), respond asking the user to repeat the language they want to learn."
    messages = [{"role": "system", "content": system_message}, {"role": "assistant", "content": "What language do you want to learn?"}, {"role": "user", "content": user_message.text}]
    response = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user", "content": user_message.text}])
    learning_language_code = response.choices[0].message.content
    return learning_language_code
