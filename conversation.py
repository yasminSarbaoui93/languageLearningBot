# This file contains the functions that are used to start a conversation with the user and get responses from OpenAI
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd
from vocabulary import get_all_words

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


#extract all words of a dictionary - for now i have it locally
user_id = os.getenv("USER_ID")
all_words = get_all_words(user_id)


#create an array that gets only the german terms from all_words, meaning that are in [0][1], [1][1], [2][1] etc
german_words = []
for i in range(len(all_words)):
    german_words.append(str(all_words[i][1]))
    
german_words = str(german_words)

#initialize conversation locl memory with system message
userConversation = []

def callOpenAI(message, bot, newConversation):
    #conversation starter from the bot. When calling this function, if there was no interaction yet then the bot will send a welcome message, otherwise it will respond to the user query
    try:
        if newConversation:
            userConversation = []
            userConversation.append({"role": "system", "content": "You are a bot that helps students to learn German. You need to have simple conversations, with short sentences, using only present tense. You will mainly use terms from the dictionary in the TermsList file, as these are the words the student knows. \nHere is the list of the terms: " + german_words})
            assistantMessage = bot.reply_to(
                message, f"Hallo, ich kann dir hilfe zu Deutch spreche! 🇩🇪" + '\n' + "Remember you can end the conversation anytime by typig `end`"
            )
            userConversation.append({"role": "assistant", "content": assistantMessage.text})
            bot.register_next_step_handler(
                message, lambda msg: llmresponse(msg, client, bot)
            )
        else:
            bot.register_next_step_handler(
                message, lambda msg: llmresponse(msg, client, bot)
            )
        return userConversation
    except Exception as e:
        return f"An error occurred: {e}"


def llmresponse(userMessage, client, bot):
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
        callOpenAI(userMessage, bot, False)


