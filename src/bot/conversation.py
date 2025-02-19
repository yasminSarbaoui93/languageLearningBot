"""
This file contains the functions to be called by the bot that are used to start a conversation with the user and get responses from OpenAI
"""
from src.repository.vocabulary import get_all_words, get_or_create_user
from services.llm_service import llm_response, translate_to_language
from services.language_service import language_name_from_code
from bot.helpers import send_bot_response

def initializeConversation(message, bot):
    user = get_or_create_user(str(message.from_user.id), message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    user_id = user.id
    all_words = get_all_words(user_id)
    user_known_words = []
    for i in range(len(all_words)):
        user_known_words.append(str(all_words[i][1]))
    user_known_words = str(user_known_words) #might be misunderstandable the fact that in random terms i call user_known_words the list of german words + translations while here only german words
    print(f"\nDictionary from user {message.from_user.first_name} and dictionary is: containing {len(all_words)} words for all words, and {len(user_known_words)} for user known words\n")
    
    chat_history = []
    
    learning_language_code = user.learning_language
    learning_language_name = language_name_from_code(learning_language_code)
    base_language_code = user.base_language

    system_message = f"You are a bot that helps students to learn a new language. The language code ISO 639 of the language the student is learning is {learning_language_code} and this is the only language you must speak. You need to have simple conversations in the language they are learning ({learning_language_code}), with short sentences, using mostly present tense. You will mainly use terms from the user's vocabulary user_knowwn_words list, as these are the words the student knows. \nHere is the list of the terms the user knows: {user_known_words}"
    chat_history.append({"role": "system", "content": system_message})
    
    bot_message = f"Hello, I can help you to learn {learning_language_name}!"
    chat_history = send_bot_response(bot, message, chat_history, learning_language_code, bot_message)

    bot_message = f"Remember you can end the conversation anytime by typing the following:"
    chat_history = send_bot_response(bot, message, chat_history, base_language_code, bot_message, "<b>end</b>")

    _manageConversation(message, bot, chat_history, base_language_code)


def _manageConversation(message, bot, chat_history, base_language_code):
    """
    Function to start or continue a conversation with the user and get responses from OpenAI
    
    args:
    message: the message object from the user
    bot: the bot object to send the message
    newConversation: a boolean indicating if this is a new conversation or not
    chat_history: the conversation history array
    
    returns:
    chat_history: the conversation history
    """
    bot.register_next_step_handler(message, lambda msg: _get_llm_response(msg, chat_history, bot, base_language_code))


def _get_llm_response(user_message, chat_history, bot, base_language_code):
    """
    Function to get responses from OpenAI and continue the conversation

    args:
    user_message: the message object from the user. If the user message is "end", the conversation will end
    chat_history: the conversation history
    client: the OpenAI client object
    bot: the bot object to send the message
    """
    if user_message.text.lower() == "end":
        #Check if the user wanted to end the conversation with the "end", keyword.
        send_bot_response(bot, user_message, chat_history, base_language_code, "<b>Conversation ended</b>")
    else:
        chat_history.append({"role": "user", "content": user_message.text})
        ai_response = llm_response(chat_history)
        chat_history.append({"role": "assistant", "content": ai_response})
        bot.send_message(user_message.chat.id, ai_response)
        _manageConversation(user_message, bot, chat_history, base_language_code)
        print(f"\n\n{chat_history}")