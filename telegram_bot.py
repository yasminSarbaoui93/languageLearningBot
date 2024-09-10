import os
import random
import telebot
from dotenv import load_dotenv
# Add excel terms

# Load the environment variables
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

german_words = {
    "hello": "hallo",
    "goodbye": "auf wiedersehen",
    "thanks": "danke",
    "please": "bitte"
}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! type /info to get more information")

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "This is a telegram bot created with python")

@bot.message_handler(commands=['bye'])
def send_info(message):
    bot.reply_to(message, "Goodbye! Have a nice day")

@bot.message_handler(commands=['random'])
def send_random_word(message):
    random_word = random.choice(list(german_words.keys()))
    print("Random word: " + random_word)
    bot.reply_to(message, f"Translate this word: {random_word}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print("Message received:" + message.text)
    bot.reply_to(message, message.text)



print("Bot is running")
bot.polling()