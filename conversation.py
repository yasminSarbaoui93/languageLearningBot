# This file contains the functions that are used to start a conversation with the user and get responses from OpenAI
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


terms_data = os.path.join(os.getcwd(), "TermsList.csv")
german_words = open(terms_data, "r", encoding="utf-8").read()
userConversation = []
userConversation.append({"role": "system", "content": "You are a bot that helps students to learn German. You need to have simple conversations, with short sentences, using only present tense. You will mainly use terms from the germanWords dictionary, as these are the words the student knows. \nHere is the list of the terms translated from Italian to German: " + german_words})


def callOpenAI(message, bot):
    if len(userConversation) == 0:
        assistantMessage = bot.reply_to(
            message, f"Hallo, ich kann dir hilfe zu Deutch spreche! 🇩🇪"
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



def llmresponse(messaggio, client, bot):
    if messaggio.text == "end":
        bot.reply_to(messaggio, "Conversation ended")
        return
    else:
        userConversation.append({"role": "user", "content": messaggio.text})
        response = client.chat.completions.create(model="gpt-4o", messages=userConversation)

        userConversation.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        bot.reply_to(messaggio, response.choices[0].message.content)
        callOpenAI(messaggio, bot)



# function to create a conversation thread
# funcition to check if the thread already exists or not
# fix the handler function in order to not end the thread unless end button arrives


# def callOpenAI(user_message)
#     try:
#         response = openai.completions.create(
#             model="gpt-4o"
#             messages=[{"role": "user", "content": user_message}]
#             temperature=0.7
#             max_tokens=150
#         )
#         return response.choices[0].text.strip()
#     except Exception as e:
#         return f"An error occurred: {e}"


# stream = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "Say this is a test"}],
#     stream=True,
# )
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")
