"""
This file contains the functions to be called by the bot that are used to start a conversation with the user and get responses from OpenAI
"""
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
from src.repository.vocabulary import get_all_words

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
user_id = os.getenv("USER_ID")

# all_words = get_all_words(user_id)
# """extract all words of a dictionary - for now i have it locally"""


# german_words = []
# """array of all german words in the dictionary"""
# for i in range(len(all_words)):
#     german_words.append(str(all_words[i][1]))
# german_words = str(german_words)


userConversation = []
"""array to store the conversation history locally, initialized with a system message"""

def initializeConversation(message, bot, newConversation):
    global german_words, userConversation
    all_words = get_all_words(message.from_user.first_name, message.from_user.last_name, str(message.from_user.id), message.from_user.username)
    german_words = []
    for i in range(len(all_words)):
        german_words.append(str(all_words[i][1]))
    german_words = str(german_words)
    print(f"Dictionary from user {message.from_user.first_name} and dictionary is: containing {len(all_words)} words")
    _callOpenAI(message, bot, newConversation)



def _callOpenAI(message, bot, newConversation):
    """
    Function to start a conversation with the user and get responses from OpenAI
    
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
            userConversation.append({"role": "system", "content": "You are a bot that helps students to learn German. You need to have simple conversations, with short sentences, using only present tense. You will mainly use terms from the dictionary in the TermsList file, as these are the words the student knows. \nHere is the list of the terms: " + german_words})
            assistantMessage = bot.reply_to(
                message, f"Hallo, ich kann dir helfen zu Deutsch zu sprechen! 🇩🇪" + '\n' + "Remember you can end the conversation anytime by typig `end`"
            )
            userConversation.append({"role": "assistant", "content": assistantMessage.text})
            bot.register_next_step_handler(
                message, lambda msg: _llmresponse(msg, client, bot)
            )
        else:
            bot.register_next_step_handler(
                message, lambda msg: _llmresponse(msg, client, bot)
            )
        return userConversation
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def _llmresponse(userMessage, client, bot):
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
        _callOpenAI(userMessage, bot, False)
