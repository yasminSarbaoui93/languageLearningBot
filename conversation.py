#This file contains the functions that are used to start a conversation with the user and get a response from OpenAI

#start conversation thread
#the function call open ai will become start ioen ai conversation, this will only initialize it
#need a function to update the conversation thread with user response and system response

import openai
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
userConversation = []
# thread = client.beta.threads.create()

def callOpenAI(message, bot, client):

    if len(userConversation) == 0:
        assistantMessage = bot.reply_to(message, f"Hallo, ich kann dir hilfe zu Deutch spreche! 🇩🇪")
        userConversation.append({"role": "assistant", "content": assistantMessage.text})
        bot.register_next_step_handler(message, lambda msg: llmresponse(msg, client, bot))
        print(userConversation)
    else:
        bot.register_next_step_handler(message, lambda msg: llmresponse(msg, client, bot))
        userConversation.append({"role": "user", "content": message.text})
    return userConversation





def llmresponse(messaggio, client, bot):

    # if messaggio.text == "end":
    #     bot.reply_to(message, "Conversation ended")
    #     return
    # else:


    print("the messaggio is ----- " + messaggio.text)
    userConversation.append({"role": "user", "content": messaggio.text})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=userConversation
    )
    print(userConversation) 
    bot.reply_to(messaggio, response.choices[0].message.content) 






# function to create a conversation thread

#funcition to check if the thread already exists or not

#fix the handler function in order to not end the thread unless end button arrives



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