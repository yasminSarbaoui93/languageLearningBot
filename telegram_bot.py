import os
import random
import telebot
from dotenv import load_dotenv
from randomTerms import send_random_word

# Load the environment variables
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

#Dictionary of german words with their english translations
german_words = {
    "hello": "hallo",
    "goodbye": "auf wiedersehen",
    "thanks": "danke",
    "please": "bitte"
}

# Create a message handler for the /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! type /info to get more information")

# Create a message handler for the /info command
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "This is a telegram bot created with python")

# Create a message handler for the /bye command
@bot.message_handler(commands=['bye'])
def send_info(message):
    bot.reply_to(message, "Goodbye! Have a nice day")


@bot.message_handler(commands=['random'])
def handle_random_word(message):
    send_random_word(bot, message, german_words)

# Message handler for all other messages    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print("Message received:" + message.text)
    bot.reply_to(message, message.text)

@bot.message_handler(commands=['conversation'])
def handle_conversation(message):
    #here we will start the conversation by calling LLM
    # bot.reply_to(message, "How are you?")
    # bot.register_next_step_handler(message, handle_response)

print("Bot is running")
bot.polling()