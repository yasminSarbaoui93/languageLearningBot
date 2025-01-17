import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import telebot
from dotenv import load_dotenv
from bot.random_word import send_random_word
from src.bot.conversation import initializeConversation
from bot.add_word_to_vocabulary import add_word_to_dictionary
from bot.delete_word_from_vocabulary import remove_word
from bot.first_bot_interaction import welcome_handling

# Load the environment variables
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN is not set")
bot = telebot.TeleBot(API_TOKEN)


# Create a message handler for the /start and /help commands
@bot.message_handler(commands=["start"])
def send_welcome(message):
    welcome_handling(message, bot)

# Create a message handler for the /start and /help commands
@bot.message_handler(commands=["help"])
def send_help(message):
    bot.reply_to(message, "These are the available commands:\n/info - Get information about the bot\n/bye - Say goodbye to the bot\n/random - Get a random word to translate\n/conversation - Start a conversation with the bot\n/add - Add a word to the dictionary\n/remove - Remove a word from the dictionary\n/start - Change the language of the bot\n/help - Get a list of available commands")
    

# Create a message handler for the /info command
@bot.message_handler(commands=["info"])
def send_info(message):
    bot.reply_to(message, "This is a telegram bot created with python")


# Create a message handler for the /bye command
@bot.message_handler(commands=["bye"])
def send_goodbye(message):
    bot.reply_to(message, "Goodbye! Have a nice day")


# Create a message handler for the /random command
@bot.message_handler(commands=["random"])
def handle_random_word(message):
    send_random_word(bot, message)


# Create a message handler for the /conversation command
@bot.message_handler(commands=["conversation"])
def conversation_handler(message):
    initializeConversation(message, bot, True)    


# Create a message handler for the /add command
@bot.message_handler(commands=["add"])
def add_handler(message):
    add_word_to_dictionary(message, bot)


# Create a message handler for the /remove command
@bot.message_handler(commands=["remove"])
def remove_handler(message):
    remove_word(message, bot)


# Message handler for all other messages - by now it only repeats the message that the user sent
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print("Message received:" + message.text)
    bot.reply_to(message, message.text)


print("Bot is running")
bot.polling()
