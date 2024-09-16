import os
import random
from litellm import OpenAI
import telebot
from dotenv import load_dotenv
from randomTerms import send_random_word
import openai

# Load the environment variables
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Dictionary of german words with their english translations
german_words = {
    "hello": "hallo",
    "goodbye": "auf wiedersehen",
    "thanks": "danke",
    "please": "bitte",
}


# Create a message handler for the /start and /help commands
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Welcome! type /info to get more information")


# Create a message handler for the /info command
@bot.message_handler(commands=["info"])
def send_info(message):
    bot.reply_to(message, "This is a telegram bot created with python")


# Create a message handler for the /bye command
@bot.message_handler(commands=["bye"])
def send_info(message):
    bot.reply_to(message, "Goodbye! Have a nice day")


@bot.message_handler(commands=["random"])
def handle_random_word(message):
    send_random_word(bot, message, german_words)



openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

@bot.message_handler(commands=["conversation"])
def callOpenAI(user_message):
    bot.reply_to(user_message, f"Hallo, ich kann dir hilfe zu Deutch spreche! 🇩🇪")
    response = client.chat.completions.create(

        model="gpt-4o",
        messages=[
            {"role": "user", "content": user_message.text},
        ]
    )
    llmresponse = response.choices[0].message.content
    print(llmresponse)

    #what happens here is that the LLM is receiving as a user message the /conversation command, so I need to add a waiting command in order to accept from the second message on
    #this is also the reason why it goes to the polling then
    bot.register_next_step_handler(user_message, response.choices[0].message.content)
    #return response.choices[0].text.strip()


# Message handler for all other messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print("Message received:" + message.text)
    bot.reply_to(message, message.text)


print("Bot is running")
bot.polling()
