"""
This file contains the functions to be called by the bot that are used to start a conversation with the user and get responses from OpenAI
"""
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
from src.repository.vocabulary import get_all_words, get_or_create_user_id_fromtelegram

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
user_id = os.getenv("USER_ID")


userConversation = []
"""array to store the conversation history locally, initialized with a system message"""

def initializeConversation(message, bot, newConversation):
    global german_words, userConversation
    user_id = get_or_create_user_id_fromtelegram(str(message.from_user.id), message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    all_words = get_all_words(user_id)
    german_words = []
    for i in range(len(all_words)):
        german_words.append(str(all_words[i][1]))
    german_words = str(german_words)
    print(f"Dictionary from user {message.from_user.first_name} and dictionary is: containing {len(all_words)} words")
    _manageConversation(message, bot, newConversation)


def _manageConversation(message, bot, newConversation):
    """
    Function to start or continue a conversation with the user and get responses from OpenAI
    
    args:
    message: the message object from the user
    bot: the bot object to send the message
    newConversation: a boolean indicating if this is a new conversation or not
    
    returns:
    userConversation: the conversation history
    """
    try:
        if newConversation:
            userConversation = []
            userConversation.append({"role": "system", "content": f"You are a bot that helps students to learn German. You need to have simple conversations, with short sentences, using only present tense. You will mainly use terms from the dictionary in the TermsList file, as these are the words the student knows. \nHere is the list of the terms: {german_words}"})
            assistantMessage = bot.reply_to(
                message, f"Hallo, ich kann dir helfen zu Deutsch zu sprechen! 🇩🇪" + '\n' + "Remember you can end the conversation anytime by typig `end`"
            )
            userConversation.append({"role": "assistant", "content": assistantMessage.text})
            bot.register_next_step_handler(
                message, lambda msg: _get_llm_response(msg, client, bot)
            )
        else:
            bot.register_next_step_handler(
                message, lambda msg: _get_llm_response(msg, client, bot)
            )
        return userConversation
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def _get_llm_response(userMessage, client, bot):
    """
    Function to get responses from OpenAI and continue the conversation

    args:
    userMessage: the message object from the user
    client: the OpenAI client object
    bot: the bot object to send the message
    """
    if userMessage.text == "end":
        bot.reply_to(userMessage, "Conversation ended")
        return
    else:
        userConversation.append({"role": "user", "content": userMessage.text})
        response = client.chat.completions.create(model="gpt-4o", messages=userConversation)

        userConversation.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        bot.reply_to(userMessage, response.choices[0].message.content)
        _manageConversation(userMessage, bot, False)
