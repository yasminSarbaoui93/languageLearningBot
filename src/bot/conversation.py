"""
This file contains the functions to be called by the bot that are used to start a conversation with the user and get responses from OpenAI
"""
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
from src.repository.vocabulary import get_all_words, get_or_create_user_id_in_DB


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
chat_history = []
"""array to store the conversation history locally, initialized with a system message"""


def initializeConversation(message, bot, newConversation):
    global user_known_words, chat_history
    user_id = get_or_create_user_id_in_DB(str(message.from_user.id), message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    all_words = get_all_words(user_id)
    user_known_words = []
    for i in range(len(all_words)):
        user_known_words.append(str(all_words[i][1]))
    user_known_words = str(user_known_words) #might be misunderstandable the fact that in random terms i call user_known_words the list of german words + translations while here only german words
    print(f"\nDictionary from user {message.from_user.first_name} and dictionary is: containing {len(all_words)} words\n")
    _manageConversation(message, bot, newConversation, [])


def _manageConversation(message, bot, newConversation, chat_history):
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
    try:
        if newConversation:
            chat_history = []
            chat_history.append({"role": "system", "content": f"You are a bot that helps students to learn German. You need to have simple conversations, with short sentences, using only present tense. You will mainly use terms from the dictionary in the TermsList file, as these are the words the student knows. \nHere is the list of the terms: {user_known_words}"})
            assistantMessage = bot.reply_to(
                message, f"Hallo, ich kann dir helfen zu Deutsch zu sprechen! 🇩🇪" + '\n' + "Remember you can end the conversation anytime by typig `end`"
            )
            chat_history.append({"role": "assistant", "content": assistantMessage.text})
            bot.register_next_step_handler(
                message, lambda msg: _get_llm_response(msg, chat_history, client, bot)
            )
        else:
            bot.register_next_step_handler(
                message, lambda msg: _get_llm_response(msg, chat_history, client, bot)
            )
        return chat_history
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def _get_llm_response(user_message, chat_history, client, bot):
    """
    Function to get responses from OpenAI and continue the conversation

    args:
    user_message: the message object from the user
    chat_history: the conversation history
    client: the OpenAI client object
    bot: the bot object to send the message
    """
    if user_message.text == "end":
        bot.reply_to(user_message, "<b>Conversation ended</b>", parse_mode='HTML')
    else:
        chat_history.append({"role": "user", "content": user_message.text})
        response = client.chat.completions.create(model="gpt-4o", messages=chat_history)

        chat_history.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        bot.send_message(user_message.chat.id, response.choices[0].message.content)
        _manageConversation(user_message, bot, False, chat_history)
        print(f"\n\n{chat_history}")