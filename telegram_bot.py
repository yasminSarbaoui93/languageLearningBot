import os
import telebot
from dotenv import load_dotenv
from randomTerms import send_random_word
from conversation import callOpenAI
from addWord import add_word
from removeWord import remove_word

# Load the environment variables
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

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
    send_random_word(bot, message)


@bot.message_handler(commands=["conversation"])
def conversation_handler(message):
    callOpenAI(message, bot, True)

@bot.message_handler(commands=["add"])
def add_handler(message):
    add_word(message, bot) #call function to add a new word to the dictionary

@bot.message_handler(commands=["remove"])
def remove_handler(message):
    remove_word(message, bot) #call function to add a new word to the dictionary


# Message handler for all other messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print("Message received:" + message.text)
    bot.reply_to(message, message.text)


print("Bot is running")
bot.polling()
