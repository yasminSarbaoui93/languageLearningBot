import os
import random
import telebot
from dotenv import load_dotenv
from telegram_bot import send_random_word
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

#Function that gets the translation of a word taken from the dictionary
# def get_translation(word):
#     translation = german_words.get(word)
#     return translation

#Function that checks if the user response is correct or not
# def check_response(message, translation):
#     print("User response: " + message.text)
#     if message.text == translation:
#         bot.reply_to(message, "Correct! ✅")
#     else:
#         bot.reply_to(message, "Incorrect! ❌")

# Function that asks the user to translate a random word from the dictionary
@bot.message_handler(commands=['random'])
# def send_random_word(message):
#     random_word = random.choice(list(german_words.keys()))
#     translation = get_translation(random_word)
#     print("Random word: " + random_word)
#     bot.reply_to(message, f"Translate this word: {random_word}")
#     #bot.register_next_step_handler(message, check_response(translation))
#     bot.register_next_step_handler(message, lambda msg: check_response(msg, translation)) #Check better lambda function?
def handle_random_word(message):
    send_random_word(bot, message)

# Message handler for all other messages    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print("Message received:" + message.text)
    bot.reply_to(message, message.text)



print("Bot is running")
bot.polling()